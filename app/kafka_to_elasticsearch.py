import json
import time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers
from requests.exceptions import ConnectionError as RequestsConnectionError
from elastic_transport import ConnectionError as ElasticConnectionError

# -------------------------------
# Configuration

KAFKA_TOPIC = "youtube_data"
KAFKA_BROKER = "localhost:9092"          
# KAFKA_BROKER = "kafka:29092"           

ES_INDEX = "youtube_data"
ES_HOST = "http://localhost:9200"        


# -------------------------------
# Connect to Elasticsearch

def connect_elasticsearch(retries=10, delay=5):
    for i in range(retries):
        try:
            print(f"🔌 Connecting to Elasticsearch ({ES_HOST})... Attempt {i+1}/{retries}")
            es = Elasticsearch([ES_HOST], verify_certs=False, request_timeout=30)
            if es.ping():
                print("Connected to Elasticsearch!")
                return es
        except (RequestsConnectionError, ElasticConnectionError) as e:
            print(f"Elasticsearch not ready yet: {e}")
        time.sleep(delay)
    raise Exception("Could not connect to Elasticsearch after multiple retries.")

# -------------------------------
# Create Kafka Consumer

def create_consumer():
    print(f"Connecting to Kafka broker at {KAFKA_BROKER} ...")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="youtube-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    print("Connected to Kafka and listening for messages...")
    return consumer

# -------------------------------
# Send data to Elasticsearch

def index_to_elasticsearch(es, data):
    try:
        es.index(index=ES_INDEX, id=data.get("video_id"), document=data)
        print(f"Indexed video: {data.get('title', 'Unknown')} | Views: {data.get('views', 'N/A')}")
    except Exception as e:
        print(f"Failed to index document: {e}")

# -------------------------------
# Main Stream Loop

def main():
    print("Starting Kafka → Elasticsearch pipeline...")
    es = connect_elasticsearch()
    consumer = create_consumer()

    for message in consumer:
        try:
            data = message.value
            if not data:
                continue
            index_to_elasticsearch(es, data)
        except Exception as e:
            print(f"Error processing message: {e}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
