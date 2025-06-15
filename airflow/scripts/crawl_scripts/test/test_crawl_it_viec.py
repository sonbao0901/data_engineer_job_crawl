import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawl_job.it_viec import scrape_jobs_it_viec

data = scrape_jobs_it_viec("https://itviec.com/it-jobs/data-analyst")
print(data)