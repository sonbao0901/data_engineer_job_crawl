from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from crawl_scripts.crawl_job.crawler import main_crawler
import os

# Default Arguments for DAG
default_args = {
    'owner': 'harry',
    'start_date': datetime(2025, 3, 16),  # Use a fixed date to prevent errors
}

# Define DAG
with DAG(
    dag_id='crawl_job',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
):
    python_task = PythonOperator(
        task_id='crawl_job',
        python_callable=main_crawler
    )

python_task
