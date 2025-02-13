import os
import json
from topcv import *
from it_viec import *
from crawl_job.utils.get_root_folder import get_project_root

class Crawler(object):
    def __init__(self, store_path: str):
        self.store_path = os.path.join(get_project_root(), 'data')
    def save_to_json(self, data, filename: str, job_type: str):
        file_path = f'{filename}_{job_type}.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(filename, 'wb', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def scrape_data(self, source: str):
        scraper = self.scrape[source]
        return scraper(url)
    


    data = [{
        'job': 'abc',
        'title': 'data engineer'
    }]
