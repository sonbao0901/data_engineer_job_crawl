from crawl_job.utils.get_root_folder import get_project_root
import os

print(get_project_root())

#print data folder
print(os.path.join(get_project_root(), 'data'))