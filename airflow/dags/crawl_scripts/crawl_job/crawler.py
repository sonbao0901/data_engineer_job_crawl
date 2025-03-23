import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from crawl_scripts.crawl_job.it_viec import scrape_jobs_it_viec
from crawl_scripts.crawl_job.topcv import scrape_jobs_topcv
import json

# Load environment variables
load_dotenv()

class JobDataIngestion:
    def __init__(self):
        self.engine = self._create_db_connection()

    def _create_db_connection(self):
        """Create database connection"""
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        try:
            return create_engine(db_url)
        except Exception as e:
            print(f"Database connection error: {e}")

    def insert_itviec_jobs(self, jobs):
        """Insert IT Viec jobs into database"""
        if not jobs:
            print("No IT Viec jobs to insert")

        query = text("""
            INSERT INTO bronze.itviec_data_job 
            (title, company, logo, url, location, mode, tags, descriptions, requirements)
            VALUES (:title, :company, :logo, :url, :location, :mode, :tags, :descriptions, :requirements)
            ON CONFLICT (url) DO UPDATE SET
            title = EXCLUDED.title,
            company = EXCLUDED.company,
            logo = EXCLUDED.logo,
            location = EXCLUDED.location,
            mode = EXCLUDED.mode,
            tags = EXCLUDED.tags,
            descriptions = EXCLUDED.descriptions,
            requirements = EXCLUDED.requirements
        """)

        try:
            with self.engine.connect() as conn:
                trans = conn.begin()  # Start transaction
                try:
                    conn.execute(query, jobs)  # Bulk insert instead of looping
                    trans.commit()  # Commit once for all jobs
                except SQLAlchemyError as e:
                    trans.rollback()
                    print(f"Error inserting IT Viec jobs: {e}")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    def insert_topcv_jobs(self, jobs):
        """Insert TopCV jobs into database"""
        if not jobs:
            print("No TopCV jobs to insert")

        query = text("""
            INSERT INTO bronze.topcv_data_job 
            (title, company, logo, url, location, salary)
            VALUES (:title, :company, :logo, :url, :location, :salary)
            ON CONFLICT (url) DO UPDATE SET
            title = EXCLUDED.title,
            company = EXCLUDED.company,
            logo = EXCLUDED.logo,
            location = EXCLUDED.location,
            salary = EXCLUDED.salary
        """)

        try:
            with self.engine.connect() as conn:
                trans = conn.begin()
                try:
                    conn.execute(query, jobs)
                    trans.commit()
                except SQLAlchemyError as e:
                    trans.rollback()
                    print(f"Error inserting TopCV jobs: {e}")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    def insert_job(self, source, jobs):
        if source == "itviec":
            self.insert_itviec_jobs(jobs)
        elif source == "topcv":
            self.insert_topcv_jobs(jobs)
        else:
            print(f"Invalid source: {source}")

def load_crawl_sources():
    """Load the list of web sources from the JSON configuration file."""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_crawl.json")
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")


def main_crawler():
    ingestion = JobDataIngestion()
    web_sources = load_crawl_sources()

    for source, url in web_sources.items():
        try:
            if source=="itviec":
                itviec_jobs = scrape_jobs_it_viec(url)
                ingestion.insert_job("itviec", itviec_jobs)
            if source=="topcv":
                topcv_jobs = scrape_jobs_topcv(url)
                ingestion.insert_job("topcv", topcv_jobs)
        except Exception as e:
            print(f"Error in data ingestion: {e}")