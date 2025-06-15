import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from scripts.crawl_scripts.crawl_job.crawler import Crawler
from scripts.insert_data_bronze import insert_itviec_jobs
from scripts.utils.load_crawl_source import load_crawl_sources

#Define DAG
default_args = {
    'owner': 'sonbao',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 1),
    'retries': 3,
    'retry_delay': timedelta(seconds=30)
}

@dag(
    dag_id='itviec_data_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=15),
    catchup=False,
    tags=['itviec_pipeline']
)

def itviec_pipeline():

    @task
    def load_itviec_url():
        data = load_crawl_sources(file_name='source_itviec.json')
        return data

    @task
    def scrape_itviec_job(sources: dict):
        crawler = Crawler("itviec")
        for source, url in sources.items():
            print(f"Processing source: {source} with URL: {url}")
            try:
                itviec_jobs = crawler.crawler(url)
                if itviec_jobs:
                    print(f"Successfully scraped {len(itviec_jobs)} jobs from IT Viec")
            except Exception as e:
                print(f"Error scraping IT Viec: {e}")

    @task
    def insert_jobs(data):
        if not data:
            print("No IT Viec jobs to insert")
            return
        insert_itviec_jobs(data)

    itviec_sources=load_itviec_url()
    job_data=scrape_itviec_job(itviec_sources)
    insert_jobs(job_data)

dag = itviec_pipeline()