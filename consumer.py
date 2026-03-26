import json
import numpy as np
# import os
import csv
from kafka import KafkaConsumer
from sklearn.ensemble import IsolationForest

FILE_NAME = "fraud_details.csv"
TOPIC_NAME = "test-topic"

# if not os.path.exists(FILE_NAME):
with open(FILE_NAME, mode="w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Transaction_ID", "Amount", "Type", "Status"])


#here im configuring the Consumer file 
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

#parameter contamination=0.1 means we are expecting 10% outliers
model = IsolationForest(contamination=0.1, random_state=42)
data_buffer = []
is_trained = False

print("--- ML-Powered Fraud Detection Engine Started ---")
print("Phase 1: Learning Patterns (Initial 50 transactions).....\n")

try:
    for message in consumer:
        tx = message.value
        amount = tx['amount']
        
        #here im converting amount in array format as per ML model (Isolation Forest) requirement
        current_val = np.array([[amount]])

        if not is_trained:
            data_buffer.append(amount)
            print(f"Buffering: {len(data_buffer)}/50", end='\r')
            
            if len(data_buffer) >= 50:
                #training the model
                X_train = np.array(data_buffer).reshape(-1, 1)
                model.fit(X_train)
                is_trained = True
                print("\n\n[SUCCESS] Model Trained! Switching to Real-Time Detection...\n")
        else:
            #im predicting 1 = Normal, -1 = Anomaly (Fraud)
            prediction = model.predict(current_val)
            
            if prediction[0] == -1:
                status = "!! Model Alert: FRAUD !!"
            else:
                status = "NORMAL"
            
            print(f"ID: {tx['transaction_id']} | Amount: {amount:<10} | Status: {status}")

            #below im appending the fraud details in the csv file
            if status == "!! Model Alert: FRAUD !!":
                with open(FILE_NAME, mode='a', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([tx['transaction_id'], amount, tx['transaction_type'], "!! MODEL ALERT !!"])

except KeyboardInterrupt:
    print("\nDetection Engine Stopped/Interrupted by User.....")