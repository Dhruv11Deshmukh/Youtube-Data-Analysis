import json, time, schedule
from kafka import KafkaProducer
from googleapiclient.discovery import build

# === CONFIG ===
API_KEY = "Your_API_Key"
CHANNEL_ID = "UCt4t-jeY85JegMlZ-E5UWtA"  # example: AajTak
KAFKA_TOPIC = "youtube_data"
KAFKA_BROKER = "localhost:9092"

# === SETUP ===
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_youtube_data():
    print("📡 Fetching latest YouTube videos...")
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        order="date",
        maxResults=10
    )
    response = request.execute()

    for item in response.get("items", []):
        video_id = item["id"].get("videoId")
        if not video_id:
            continue
        video_data = {
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "publishedAt": item["snippet"]["publishedAt"]
        }
        producer.send(KAFKA_TOPIC, video_data)
        print(f"Sent: {video_data['title']}")

schedule.every(2).minutes.do(fetch_youtube_data)

if __name__ == "__main__":
    fetch_youtube_data()
    while True:
        schedule.run_pending()
        time.sleep(5)

