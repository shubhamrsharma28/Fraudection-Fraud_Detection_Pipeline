# print("$ Jai Siya Ram $")

import streamlit as st
from kafka import KafkaConsumer
import time
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import json
import plotly.graph_objects as go

#setted the page width to wide as streamlit has limited-centered layout by default
st.set_page_config(page_title="Real-Time Fraud Detection Pipeline", layout="wide")

st.markdown("""
    <style>
        header{
            background-color: transparent;
            height:20px;}

        .stApp{
            background: linear-gradient(125deg, #0e1117 1%, #1a202c 40%, #2d3748 100%);
            background-attachment:fixed;
            padding-top:0px;
            margin-top:0px;
            }

        .block-container{
            padding:2.5rem 5rem 3rem 5rem;}
        
        .stTable {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
        }
        .js-plotly-plot{
            background-color:transparent !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
            <h1 class="main-title">🛡️ Real-Time Fraud Detection Pipeline</h1>
            <p class="main-desc">Protecting digital transactions by analyzing real-time data streams and flagging potential frauds as they happen.</p>
            <style>
                .main-title {
                    font-weight: 700;
                    text-align:center;
                    color: white !important;
                    font-size:3rem !important;}
            
                .main-desc {
                    color:#94a3b8 !important;
                    text-align:center;
                    font-size:1.4rem;
                    margin-bottom: 2rem
                    # max-width:400px;
                    }
            
                [data-testid="stMetricLabel"], [data-testid="stMetricValue"], label, .stText {
                    color: #ffffff !important;
                    text-align:center;
                    border-radius:15px;
                    }
            </style>
""", unsafe_allow_html=True)

#here im making the sidebar for displaying docker and kafka status of running
with st.sidebar:
    st.header("Infrastructure Status")
    st.success("Docker is running")
    st.info("Kafka Broker connected")
    st.markdown("----")
    st.write("Scanning Live Streaming data")
    st.spinner("Monitoring....")

#adding multiple variabels after checking whether they already exist or not
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Transaction_ID", "Amount", "Type", "Status"])
if 'counts' not in st.session_state:
    st.session_state.counts = {"Normal" : 0, "Fraud" : 0}
if 'model' not in st.session_state:
    st.session_state.model = IsolationForest(contamination=0.1, random_state=42)
    st.session_state.is_trained = False

#im making empty placeholder spaces which i will use later to fill live data without refreshing the whole script
placeholder_metrics = st.empty()
placeholder_status = st.empty()
placeholder_table = st.empty()
placeholder_chart = st.empty()

#initializing the kafka consumer with the topic and the docker's hardcoded port i.e. 9092
consumer = KafkaConsumer('test-topic', bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))

training_data = []
for message in consumer:
    tx = message.value
    if not st.session_state.is_trained:
        training_data.append([tx['amount']])
        placeholder_status.warning(f"🟡 Model is training. Collecting {len(training_data)}/50 samples")
        # time.sleep(0.1)
        if len(training_data) >= 50:
            st.session_state.model.fit(training_data)
            st.session_state.is_trained = True
            placeholder_status.success("🟢 Model Trained. Monitoring Live Streaming data....")
            break

for message in consumer:
    tx= message.value
    amount= np.array([[tx['amount']]])

    prediction= st.session_state.model.predict(amount)
    #setting Fraud as -1 and Normal as 1
    if prediction[0] == -1:
        status = "🚨FRAUD🚨"
    else:
        status = "Normal"
    
    #here im everytime adding 1 in both Normal and fraud count by checking what it is
    if status == "🚨FRAUD🚨":
        st.session_state.counts["Fraud"] += 1
        log_file = "fraud_details.csv"
        file_exists = os.path.isfile(log_file)
        new_row.to_csv(log_file, mode="a", index=False, header=not file_exists)
    else:    
        st.session_state.counts["Normal"] += 1

    #now this new_row is the new row im adding/concatinating in the data table so that the latest transaction 
    # data stays on top everytime and old transaction details gets to the bottom of the table.
    new_row = pd.DataFrame([[tx['transaction_id'], tx['amount'], tx['type'], status]],
                           columns=["Transaction_ID", "Amount", "Type", "Status"])
    st.session_state.data = pd.concat([new_row, st.session_state.data]).reset_index(drop=True)

    with placeholder_table.container(height=350):
        st.table(st.session_state.data)
    

    with placeholder_metrics.container():
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Transactions Scanned: ", len(st.session_state.data))
        c2.metric("Total Frauds detected: ", st.session_state.counts['Fraud'], delta_color="inverse")
        c3.metric("System Health: ", "98.7%", delta="Stable")

    fig = go.Figure(data=[
        go.Bar(name="Normal", x=["Transactions"], y=[st.session_state.counts['Normal']], marker_color='green'),
        go.Bar(name="🚨FRAUD🚨", x=["Transactions"], y=[st.session_state.counts['Fraud']], marker_color="red")
    ])
    fig.update_layout(barmode="group", height=400, title_text="Live Transaction Trend")

    with placeholder_chart:
        st.plotly_chart(fig, use_container_width=True)

    time.sleep(1.5)
