import json
from kafka import KafkaConsumer

# Configuration for the Kafka Consumer
# Connecting to localhost:9092 and starting from the latest messages
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("--- Real-Time Fraud Detection Engine Started ---")
print("Monitoring incoming transactions...\n")

try:
    for message in consumer:
        transaction = message.value
        amount = transaction['amount']
        tx_id = transaction['transaction_id']
        
        # Simple Fraud Detection Logic: 
        # Any transaction above 6000 is flagged as FRAUD for investigation
        if amount > 6000:
            status = "!!! FLAG AS FRAUD !!!"
        else:
            status = "NORMAL"
            
        print(f"ID: {tx_id} | Amount: ${amount:<8} | Status: {status}")

except KeyboardInterrupt:
    print("\nINFO: Detection Engine Stopped.")
except Exception as e:
    print(f"ERROR: Analytics Failure: {e}")