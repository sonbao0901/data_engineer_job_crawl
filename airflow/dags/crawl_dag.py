from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from crawl_scripts.crawl_job.crawler import main_crawler

# Default Arguments for DAG
default_args = {
    'owner': 'harry',
    'start_date': datetime(2025, 3, 16),  # Use a fixed date to prevent errors
    'retries': 2,
    'retry_delay': timedelta(minutes=5)  # Corrected import
}

# Define DAG
with DAG(
    dag_id='crawl_job',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
):
    python_task = PythonOperator(
        task_id='crawl_job_automation',
        python_callable=main_crawler
    )

python_task
