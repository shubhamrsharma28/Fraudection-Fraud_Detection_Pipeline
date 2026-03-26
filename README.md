# **Real-Time Fraud Detection Pipeline (Kafka + ML) 🚀**

A high-performance ETL pipeline that detects fraudulent transactions in real-time using **Apache Kafka** for data streaming and **Isolation Forest (Machine Learning)** for anomaly detection.

## 📌 Project Overview
This project simulates a financial transaction stream and identifies suspicious activities (anomalies) without any pre-labeled data. It transitions from a simple rule-based approach to a sophisticated **Unsupervised Machine Learning** model.

## 🏗️ Architecture
1. **Producer (Extract):** Generates random transaction data and streams it to Kafka.  
2. **Kafka (Transform/Stream):** Acts as a distributed message broker (running on Docker).  
3. **Consumer (ML Analysis):**  
   - Buffers the first 50 transactions to learn the "Normal" pattern.  
   - Uses **Isolation Forest** to detect outliers in real-time.  
4. **Storage (Load):** Automatically logs all detected frauds into a local `fraud_details.csv` file.

## 🛠️ Tech Stack
- **Streaming:** Apache Kafka  
- **Infrastructure:** Docker & Docker-Compose  
- **Language:** Python 3.x  
- **Machine Learning:** Scikit-Learn (Isolation Forest)  
- **Data Handling:** Pandas, Numpy  

## 🚀 How to Run
1. **Start Kafka Environment**
```bash
   docker-compose up -d
```
2. **Install Dependencies**
```bash
   pip install -r requirements.txt
```
3. **Start Detection Engine**

Open two terminals:

- Terminal 1: 
```bash
   python producer.py
```
- Terminal 2: 
```bash
   python consumer.py
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
