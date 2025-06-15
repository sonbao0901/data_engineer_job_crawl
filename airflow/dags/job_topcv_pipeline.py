import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from scripts.crawl_scripts.crawl_job.crawler import Crawler
from scripts.insert_data_bronze import insert_topcv_jobs
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
    dag_id='topcv_data_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=15),
    catchup=False,
    tags=['topcv_pipeline']
)

def topcv_pipeline():

    @task
    def load_topcv_url():
        data = load_crawl_sources(file_name='source_topcv.json')
        return data

    @task
    def scrape_topcv_job(sources: dict):
        crawler = Crawler("topcv")
        for source, url in sources.items():
            print(f"Processing source: {source} with URL: {url}")
            try:
                itviec_jobs = crawler.crawler(url)
                if itviec_jobs:
                    print(f"Successfully scraped {len(itviec_jobs)} jobs from IT Viec")
            except Exception as e:
                print(f"Error scraping TopCV: {e}")

    @task
    def insert_jobs(data):
        if not data:
            print("No IT Viec jobs to insert")
            return
        insert_topcv_jobs(data)

    itviec_sources=load_topcv_url()
    job_data=scrape_topcv_job(itviec_sources)
    insert_jobs(job_data)

dag = topcv_pipeline()