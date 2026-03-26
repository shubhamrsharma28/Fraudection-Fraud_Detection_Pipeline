# Workshop Guide: Real-Time Fraud Detection Pipeline

## Introduction
This project focuses on optimizing financial data pipelines for real-time anomaly detection. In the banking sector, identifying fraudulent transactions the moment they occur is critical. Traditional batch processing often misses these windows of opportunity. This workshop demonstrates how to build a high-speed pipeline using Apache Kafka for streaming and Machine Learning for intelligent detection.

## Problem Statement
Financial institutions like Finastra handle millions of transactions per second. Manual monitoring or simple rule-based systems (like flagging everything over $5000) fail to catch sophisticated fraud patterns. We need a system that learns "normal" behavior and flags deviations instantly without human intervention.

## Tools and Technologies Used
* **Apache Kafka:** Used as the distributed backbone for streaming data between services.
* **Docker:** Used to containerize the Kafka environment for easy deployment and scalability.
* **Python:** The primary language for building the producer and ML consumer.
* **Scikit-Learn (Isolation Forest):** The engine used for unsupervised anomaly detection.

## Architecture and Workflow
The system follows a 4-step data lifecycle:
1. **Extract:** The Producer generates synthetic transaction data.
2. **Stream:** Kafka Brokers handle the high-speed data flow.
3. **Analyze:** The Consumer applies an ML model to the live stream.
4. **Report:** Anomalies are logged into a CSV file for audit trails.



## Step-by-Step Implementation

### Step 1: Setting up the Infrastructure
We use Docker to avoid manual installation of Kafka and Zookeeper. Zookeeper manages the Kafka cluster state while Kafka handles the message queues. Run the environment using:
```bash
docker-compose up -d
```
### Step 2: Preparing the Environment
Install the necessary Python libraries to interact with Kafka and run the Machine Learning model.

```bash
pip install kafka-python
```
```bash
pip install scikit-learn
```
```bash
pip install numpy
```
### Step 3: Developing the Data Producer
The producer simulates a live bank feed. It sends JSON messages containing a transaction ID, amount and type to a Kafka topic named test-topic.

```bash
python producer.py
```

### Step 4: Building the ML Consumer
This is the core of the project. The consumer performs three main tasks:

1. Why Unsupervised Learning?
In real-world fraud detection, we often do not have "labeled" data. Unsupervised learning allows the model to find patterns on its own without needing prior labels.

2. Why Isolation Forest?
We chose Isolation Forest because it is built specifically for anomaly detection. Instead of profiling normal points, it explicitly isolates outliers. Anomalies are "few and far" from the main cluster, making them easier to isolate with fewer splits in a tree structure.

3. The Implementation Logic
The consumer buffers the first 50 transactions to establish a "baseline" of normal activity. Once trained, every new transaction is scored. If the model sees a transaction that looks statistically different from the baseline, it flags it as FRAUD.

### Step 5: Auditing and Results
To ensure the project is workshop-ready, we log every flagged transaction into a local file. This serves as a "Fraud Report" for stakeholders.

StockProject/fraud_alerts.csv

## Workshop Learning Outcomes
- By completing this project, learners will understand:

- How to manage real-time data streams using Kafka and Docker.

- The transition from static rules to dynamic Machine Learning models.

- How to deploy an unsupervised model (Isolation Forest) for live anomaly detection.

- Building an end-to-end ETL pipeline that is ready for production.