import json
import time
import os
from kafka import KafkaProducer, errors

def create_producer(retries=5, delay=5):
    for attempt in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVERS")],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return producer
        except errors.NoBrokersAvailable:
            print(f"No brokers available, retrying in {delay} seconds... (attempt {attempt+1}/{retries})")
            time.sleep(delay)
    raise Exception("Could not connect to Kafka brokers.")

def send_data(producer):
    data_source = os.environ.get("DATA_SOURCE", "data/raw/yelp_academic_dataset_business.json")
    while True:
        try:
            with open(data_source, 'r') as f:
                for line in f:
                    record = json.loads(line)
                    producer.send('yelp_topic', record)
                    time.sleep(0.001)
            break
        except OSError as e:
            print(f"Error reading file: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    producer = create_producer()
    send_data(producer)