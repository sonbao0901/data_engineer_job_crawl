from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DbConnection:
    def __init__(self):
        self.engine = self._create_db_connection()

    def _create_db_connection(self):
        """Create database connection"""
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        try:
            engine = create_engine(db_url)
            return engine
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            return None

# Instantiate connection
db_connection = DbConnection()
engine = db_connection.engine.raw_connection()

# ✅ Using Pandas to read data
if engine:
    try:
        df = pd.read_sql("SELECT * FROM bronze.topcv_data_job", con=engine)
        print(df.head())
    except Exception as e:
        print("Query error:", e)
def clean_data_topcv():
    df['title'] = df['title']\
                            .str.replace('\n', ' ')\
                            .str.replace(r'\s+', ' ', regex=True)\
                            .str.strip()\
                            .str.title()
    
    df['company'] = df['company']\
                            .str.replace('\n', ' ')\
                            .str.replace(r'\s+', ' ', regex=True)\
                            .str.strip()\
                            .str.title()
