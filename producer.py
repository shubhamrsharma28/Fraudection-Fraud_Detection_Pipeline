import json
import time
import random
from kafka import KafkaProducer

# Kafka Producer Configuration
#below im connecting to the Kafka broker running on Docker i.e. localhost:9092
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("--- Fraud Detection Producer Service Initialized ---")

def generate_transaction():
    """Generates a random financial transaction record."""
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'New York', 'London']
    tx_types = ['Online', 'ATM', 'Store']
    
    return {
        'transaction_id': random.randint(100000, 999999),
        'card_id': f'CARD-{random.randint(1000, 9999)}',
        'amount': round(random.uniform(10.0, 10000.0), 2),
        'location': random.choice(locations),
        'type': random.choice(tx_types),
        'timestamp': time.time()
    }
counter = 0
try:
    while True:
        #creating a transaction record
        transaction = generate_transaction()
        
        #sending all transaction data to "test-topic" which is our Topic(storage)
        producer.send('test-topic', value=transaction)
        
        counter +=1 
        if counter <=50:
            time.sleep(0.1)
        else:
            time.sleep(1.5)
        print(f"INFO: Transaction Streamed -> ID: {transaction['transaction_id']} | Amount: ${transaction['amount']}")
        
        #i set a interval of 2 seconds between sending these fake transactions to kafka
        # time.sleep(2)

except KeyboardInterrupt:
    print("\nProducer Service Stopped by User.")
except Exception as e:
    print(f"ERROR: System Failure: {e}")