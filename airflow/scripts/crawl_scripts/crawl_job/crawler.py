from dotenv import load_dotenv
from .topcv import scrape_jobs_topcv
from .it_viec import scrape_jobs_it_viec

# load_dotenv()

# class JobDataIngestion:
#     def __init__(self):
#         self.engine = self._create_db_connection()

#     def _create_db_connection(self):
#         """Create database connection"""
#         db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#         try:
#             return create_engine(db_url)
#         except Exception as e:
#             print(f"Database connection error: {e}")

#     def insert_itviec_jobs(self, jobs):
#         """Insert IT Viec jobs into database"""
#         if not jobs:
#             print("No IT Viec jobs to insert")

#         #UpSert jobs into the database
#         #Using ON CONFLICT to handle duplicates based on the URL
#         query = text("""
#             INSERT INTO bronze.itviec_data_job (title, company, logo, url, location, mode, tags, descriptions, requirements)
#                     VALUES (:title, :company, :logo, :url, :location, :mode, :tags, :descriptions, :requirements)
#             ON CONFLICT (url) DO UPDATE SET
#                 title = EXCLUDED.title,
#                 company = EXCLUDED.company,
#                 logo = EXCLUDED.logo,
#                 location = EXCLUDED.location,
#                 mode = EXCLUDED.mode,
#                 tags = EXCLUDED.tags,
#                 descriptions = EXCLUDED.descriptions,
#                 requirements = EXCLUDED.requirements
#         """)

#         try:
#             with self.engine.connect() as conn:
#                 trans = conn.begin()
#                 try:
#                     conn.execute(query, jobs)  #Bulk insert instead of looping
#                     trans.commit()
#                 except SQLAlchemyError as e:
#                     trans.rollback()
#                     print(f"Error inserting IT Viec jobs: {e}")
#         except SQLAlchemyError as e:
#             print(f"Database error: {e}")

#     def insert_topcv_jobs(self, jobs):
#         """Insert TopCV jobs into database"""
#         if not jobs:
#             print("No TopCV jobs to insert")

#         query = text("""
#             INSERT INTO bronze.topcv_data_job (title, company, logo, url, location, salary, descriptions, requirements, experience, education, type_of_work)
#                     VALUES (:title, :company, :logo, :url, :location, :salary, :descriptions, :requirements, :experience, :education, :type_of_work)
#             ON CONFLICT (url) DO UPDATE SET
#                 title = EXCLUDED.title,
#                 company = EXCLUDED.company,
#                 logo = EXCLUDED.logo,
#                 location = EXCLUDED.location,
#                 salary = EXCLUDED.salary,
#                 descriptions = EXCLUDED.descriptions,
#                 requirements = EXCLUDED.requirements,
#                 experience = EXCLUDED.experience,
#                 education = EXCLUDED.education,
#                 type_of_work = EXCLUDED.type_of_work
#         """)

#         try:
#             with self.engine.connect() as conn:
#                 trans = conn.begin()
#                 try:
#                     conn.execute(query, jobs)
#                     trans.commit()
#                 except SQLAlchemyError as e:
#                     trans.rollback()
#                     print(f"Error inserting TopCV jobs: {e}")
#         except SQLAlchemyError as e:
#             print(f"Database error: {e}")

#     def insert_job(self, source, jobs):
#         if source == "itviec":
#             self.insert_itviec_jobs(jobs)
#         elif source == "topcv":
#             self.insert_topcv_jobs(jobs)
#         else:
#             print(f"Invalid source: {source}")


class Crawler:
    def __init__(self, source):
        self.source = source

    def crawler(self, url):
        if self.source == "itviec":
            return scrape_jobs_it_viec(url)
        elif self.source == "topcv":
            return scrape_jobs_topcv(url)
        else:
            raise ValueError(f"Unsupported source: {self.source}")
        
# def main_crawler():
#     ingestion = JobDataIngestion()
#     web_sources = load_crawl_sources()

#     for source, url in web_sources.items():
#         print(f"Processing source: {source} with URL: {url}")
#         source=source.split("_")[0]
#         try:
#             if source=="itviec":
#                 itviec_jobs = scrape_jobs_it_viec(url)
#                 ingestion.insert_job("itviec", itviec_jobs)
#             if source=="topcv":
#                 topcv_jobs = scrape_jobs_topcv(url)
#                 ingestion.insert_job("topcv", topcv_jobs)
#         except Exception as e:
#             print(f"Error in data ingestion: {e}")
#         print("=========================================================================")