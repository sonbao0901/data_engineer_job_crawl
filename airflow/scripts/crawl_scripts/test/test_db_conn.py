import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawl_job.crawler import JobDataIngestion

conn = JobDataIngestion()._create_db_connection()
print(conn)