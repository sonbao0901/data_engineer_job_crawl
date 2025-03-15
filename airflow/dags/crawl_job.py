import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from crawl_scripts.crawl_job.crawler import main_crawler

default_args = {
    'owner': 'harry',
    'start_date': datetime.now(),
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=5)
}

with DAG('job_crawl_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False
         ) as dag:

    crawl_job = PythonOperator(
        task_id='crawl_job',
        python_callable=main_crawler
    )