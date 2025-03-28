from kafka import KafkaConsumer
import json
import psycopg2
import time
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()

def extract_keywords(title):
    words = tokenizer.tokenize(title.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in words if w.isalnum() and w not in stop_words]
    return ','.join(keywords[:5])

def get_postgres_conn():
    return psycopg2.connect(
        dbname="reddit",
        user="postgres",
        password="postgres",
        host="postgres",
        port=5432
    )

def consume_loop(batch_size=10, poll_interval=5, delay_sec=2):
    print("Starting Kafka consumer (loop mode)...")
    time.sleep(3)

    consumer = KafkaConsumer(
        'reddit_posts',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='reddit_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    conn = get_postgres_conn()
    cur = conn.cursor()

    while True:
        print(f"Polling Kafka (interval: {poll_interval}s)...")
        messages = consumer.poll(timeout_ms=1000, max_records=batch_size)

        if not messages:
            print("No messages. Sleeping...")
            time.sleep(poll_interval)
            continue

        count = 0
        for tp, batch in messages.items():
            for message in batch:
                post = message.value
                time.sleep(delay_sec)  # Simulate processing delay

                keywords = extract_keywords(post.get('title', ''))

                try:
                    cur.execute("""
                        INSERT INTO reddit_posts (id, title, score, author, created_utc, permalink, url, num_comments, subreddit, keywords)
                        VALUES (%s, %s, %s, %s, to_timestamp(%s), %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        post['id'],
                        post['title'],
                        post['score'],
                        post['author'],
                        post['created_utc'],
                        post['permalink'],
                        post['url'],
                        post.get('num_comments', 0),
                        post.get('subreddit', ''),
                        keywords
                    ))
                    conn.commit()
                    count += 1
                    print(f"✅ Inserted: {post['title'][:50]}...")
                except Exception as e:
                    print(f"Error inserting post: {e}")
                    conn.rollback()

        print(f"✔️ Poll cycle done. Inserted {count} posts.")
        time.sleep(poll_interval)

if __name__ == "__main__":
    consume_loop()
