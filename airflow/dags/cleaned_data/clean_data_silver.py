from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

class DbConnection:
    def _init__(self):
        self.engine = self._create_db_connection()

    def _create_db_connection(self):
        """Create database connection"""
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        try:
            return create_engine(db_url)
        except Exception as e:
            print(f"Database connection error: {e}")

def clean_data_topcv():
    pass