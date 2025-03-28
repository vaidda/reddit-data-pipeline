import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

ALERT_EMAIL = os.getenv("ALERT_EMAIL")

default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': [ALERT_EMAIL],
}

with DAG(
    dag_id='reddit_to_postgres_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 3, 24),
    schedule_interval='@hourly',  # or 'None' for manual runs
    catchup=False,
    tags=["reddit", "kafka", "postgres"],
) as dag:

    produce = BashOperator(
        task_id='produce_to_kafka',
        bash_command='python /app/stream_processing/kafka_producer.py',
    )

    consume = BashOperator(
        task_id='consume_from_kafka',
        bash_command='python /app/stream_processing/kafka_consumer.py',
    )

    produce >> consume
