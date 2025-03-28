import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from data_ingestion.reddit_fetcher import fetch_top_posts


def wait_for_kafka():
    for attempt in range(5):
        try:
            print(f"🔌 Attempt {attempt + 1}: Connecting to Kafka...")
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Connected to Kafka!")
            return producer
        except NoBrokersAvailable:
            print("Kafka not available yet... retrying in 5s")
            time.sleep(5)
    raise Exception("Kafka not available after retries")


def publish_posts(subreddit='technology'):
    producer = wait_for_kafka()

    print(f"Fetching top posts from: r/{subreddit}")
    posts = fetch_top_posts(limit=50)

    for post in posts:
        producer.send('reddit_posts', value=post)
        print(f"Sent: {post ['title'] [:50]}...")

    producer.flush()
    print("✅ All messages sent!")


if __name__ == "__main__":
    publish_posts()
