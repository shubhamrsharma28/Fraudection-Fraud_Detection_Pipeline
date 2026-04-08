# **Real-Time Fraud Detection Pipeline (Kafka + ML) 🚀**

A high-performance ETL pipeline that detects fraudulent transactions in real-time using **Apache Kafka** for data streaming and **Isolation Forest (Machine Learning)** for anomaly detection.

## 📌 Project Overview
This project simulates a financial transaction stream and identifies suspicious activities (anomalies) without any pre-labeled data. It transitions from a simple rule-based approach to a sophisticated **Unsupervised Machine Learning** model.

## 🏗️ Architecture
1. [cite_start]**Producer (Extract):** Generates random transaction data and streams it to Kafka. [cite: 15]
2. [cite_start]**Kafka (Transform/Stream):** Acts as a distributed message broker (running on Docker). [cite: 16, 22]
3. **Consumer & Dashboard (ML Analysis):** - Built with **Streamlit** for a real-time visual interface.
   - [cite_start]Buffers the first 50 transactions to train the **Isolation Forest** model. [cite: 27, 40]
   - Uses **Plotly** for live transaction trend charts.
4. [cite_start]**Audit Logging (Storage):** Automatically records all flagged frauds into `fraud_details.csv`. [cite: 18, 32]

## 🛠️ Tech Stack
- **Dashboard:** Streamlit (UI), Plotly (Visualizations)
- [cite_start]**Streaming:** Apache Kafka [cite: 22]
- [cite_start]**Infrastructure:** Docker & Docker-Compose [cite: 20]
- [cite_start]**Machine Learning:** Scikit-Learn (Isolation Forest) [cite: 23]
- [cite_start]**Data Handling:** Pandas, Numpy [cite: 23]  

## 🚀 How to Run
1. **Start Kafka Environment**
- Open Terminal in your Project Folder:
```bash
   docker-compose up -d
```
2. **Install Dependencies**
```bash
   pip install -r requirements.txt
```
3. **Start Detection Pipeline**

- In same Docker terminal: 
```bash
   python producer.py
```
- In VS Code's Terminal: 
```bash
   streamlit run main.py
```

## 📊 ML Logic: Why Isolation Forest?
Unlike simple thresholding (e.g., amount > 5000), the Isolation Forest algorithm identifies anomalies based on how "isolated" a data point is from the rest of the cluster. This allows the system to detect:
- Unusually high amounts.
- Unusually low "ping" transactions (used by hackers to test cards).
- Patterns that deviate from the learned baseline.

## 🎓 Workshop-Ready Content
This project is structured to be delivered as a **4-5 hour technical workshop**.

### **Learning Outcomes:**
- **Kafka Fundamentals:** Understanding Producers, Consumers and Brokers in Docker.
- **Real-Time ETL:** Building a data pipeline that processes events as they happen.
- **Unsupervised ML:** Implementing Anomaly Detection (Isolation Forest) on live data.
- **System Monitoring:** Logging and auditing fraud alerts into structured formats.

### **Target Audience:**
- Data Science Interns / Students
- Aspiring Data Engineers
- Fintech Enthusiasts

## 📂 Project Structure
```text
StockProject/
├── .gitignore
├── consumer.py
├── docker-compose.yml
├── producer.py
├── README.md
├── requirements.txt
└── fraud_details.csv  (Generated locally)
