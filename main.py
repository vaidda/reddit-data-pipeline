from stream_processing.kafka_producer import publish_posts

if __name__ == "__main__":
    publish_posts(subreddit='technology')
