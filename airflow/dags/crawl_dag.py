from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from crawl_scripts.crawl_job.crawler import main_crawler
# Define DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_job_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Run daily
    catchup=False
)

scrape_task = PythonOperator(
    task_id='scrape_jobs',
    python_callable=main_crawler,
    dag=dag
)

scrape_task
