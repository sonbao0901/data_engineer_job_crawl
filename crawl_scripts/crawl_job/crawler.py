import os
import json
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from topcv import scrape_jobs_topcv
from it_viec import scrape_jobs_it_viec
from crawl_scripts.utils.get_root_folder import get_project_root

load_dotenv()

class Database:
    def __init__(self):
        self.db_user, self.db_pass, self.db_host, self.db_port, self.db_name = self.get_database_config()
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @staticmethod
    def get_database_config():
        """Retrieve database configuration from environment variables."""
        return (
            os.getenv('DB_USER'), 
            os.getenv('DB_PASSWORD'),
            os.getenv('DB_HOST'),
            os.getenv('DB_PORT'),
            os.getenv('DB_NAME')
        )

    def insert_data(self, data: list[dict], table: str):
        """Insert scraped job data into the specified database table."""
        if not data:
            print(f"No data to insert into {table}.")
            return
        
        try:
            df = pd.DataFrame(data)  # Convert list of dicts to DataFrame
            df.to_sql(table, self.engine, if_exists='append', index=False)
            print(f"Inserted {len(df)} records into {table}.")
        except SQLAlchemyError as e:
            print(f"Database error while inserting data into {table}: {e}")

class Crawler(Database):
    def scrape_data(self, source: str, url: str):
        """Scrape job data from the given source and URL."""
        scrape_functions = {
            "topcv": scrape_jobs_topcv,
            "itviec": scrape_jobs_it_viec
        }
        scrape_function = scrape_functions.get(source)
        
        if not scrape_function:
            print(f"Unknown source: {source}")
            return []
        
        return scrape_function(url)

def load_crawl_sources():
    """Load the list of web sources from the JSON configuration file."""
    file_path = os.path.join(get_project_root(), "crawl_scripts", "crawl_job", "source_crawl.json")
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def main():
    crawler = Crawler()
    web_sources = load_crawl_sources()
    
    if not web_sources:
        print("No web sources found to crawl.")
        return
    
    for web, url in web_sources.items():
        print(f"Crawling {web} at {url}...")
        job_data = crawler.scrape_data(source=web, url=url)
        if job_data:
            crawler.insert_data(job_data, f"{web}_data_job")
        else:
            print(f"No data found for {web} at {url}.")

if __name__ == "__main__":
    main()
