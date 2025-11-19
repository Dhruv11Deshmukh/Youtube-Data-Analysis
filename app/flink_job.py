from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from elasticsearch import Elasticsearch
import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    consumer = FlinkKafkaConsumer(
        topics='youtube_data',
        deserialization_schema=SimpleStringSchema(),
        properties={'bootstrap.servers': 'kafka:9092', 'group.id': 'flink-group'}
    )

    es = Elasticsearch(["http://elasticsearch:9200"])

    def process(message):
        try:
            data = json.loads(message)
            es.index(index='youtube_stream', id=data['video_id'], document=data)
            print(f"Indexed: {data['title']}")
        except Exception as e:
            print(f"Error: {e}")

    stream = env.add_source(consumer)
    stream.map(process)

    env.execute("YouTube-Flink-Job")

if __name__ == "__main__":
    main()
