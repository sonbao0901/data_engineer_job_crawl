import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from it_viec import scrape_jobs_it_viec
from topcv import scrape_jobs_topcv
import json
from crawl_scripts.utils.get_root_folder import get_project_root

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class JobDataIngestion:
    def __init__(self):
        self.engine = self._create_db_connection()

    def _create_db_connection(self):
        """Create database connection"""
        try:
            db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            return create_engine(db_url)
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def insert_itviec_jobs(self, jobs):
        """Insert IT Viec jobs into database"""
        if not jobs:
            logger.warning("No IT Viec jobs to insert")
            return

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
                for job in jobs:
                    conn.execute(query, job)
                conn.commit()
            logger.info(f"Successfully inserted {len(jobs)} IT Viec jobs")
        except SQLAlchemyError as e:
            logger.error(f"Error inserting IT Viec jobs: {e}")
            raise

    def insert_topcv_jobs(self, jobs):
        """Insert TopCV jobs into database"""
        if not jobs:
            logger.warning("No TopCV jobs to insert")
            return

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
                for job in jobs:
                    conn.execute(query, job)
                conn.commit()
            logger.info(f"Successfully inserted {len(jobs)} TopCV jobs")
        except SQLAlchemyError as e:
            logger.error(f"Error inserting TopCV jobs: {e}")
            raise

def load_crawl_sources():
    """Load the list of web sources from the JSON configuration file."""
    file_path = os.path.join(get_project_root(), "crawl_scripts", "crawl_job", "source_crawl.json")

    with open(file_path) as f:
        return json.load(f)

def main():
    # Initialize the ingestion class
    ingestion = JobDataIngestion()
    web_sources = load_crawl_sources()
    for _, url in web_sources.items():
        try:
            # Insert data from both sources
            itviec_jobs = scrape_jobs_it_viec(url)
            ingestion.insert_itviec_jobs(itviec_jobs)
            topcv_jobs = scrape_jobs_topcv(url)
            ingestion.insert_topcv_jobs(topcv_jobs)
        except Exception as e:
            logger.error(f"Error in data ingestion: {e}")

if __name__ == "__main__":
    main()