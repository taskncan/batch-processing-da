import json
import time
import os
from kafka import KafkaProducer, errors

def create_producer(retries=5, delay=5):
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print(f"[INFO] Successfully connected to Kafka on attempt {attempt}.")
            return producer
        except errors.NoBrokersAvailable as e:
            last_exception = e
            print(f"[WARNING] No brokers available, retrying in {delay} seconds... (attempt {attempt}/{retries})")
            time.sleep(delay)
    raise Exception(f"[ERROR] Could not connect to Kafka brokers after {retries} attempts. Last exception: {last_exception}")

def send_data(producer):
    data_source = os.environ.get("DATA_SOURCE", "data/raw/yelp_academic_dataset_business.json")
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            with open(data_source, 'r') as f:
                for line in f:
                    record = json.loads(line)
                    producer.send('yelp_topic', record)
                    time.sleep(0.001)
            print("[INFO] Data successfully ingested.")
            return
        except OSError as e:
            retries += 1
            print(f"[WARNING] Error reading file: {e}. Retrying in 5 seconds... (attempt {retries}/{max_retries})")
            time.sleep(5)
    raise Exception("[ERROR] Could not read data file after several retries.")

if __name__ == "__main__":
    producer = create_producer()
    send_data(producer)