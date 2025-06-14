import re
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

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


db_connection = DbConnection()
engine = db_connection.engine.raw_connection()

if engine:
    try:
        df = pd.read_sql("SELECT * FROM bronze.topcv_data_job", con=engine)
    except Exception as e:
        print("Query error:", e)


def clean_salary(salary):
    if salary in ['Thương lượng', 'Thỏa thuận', 'Negotiate']:
        return None, None
    salary = salary.replace(',', '').replace('.', '').lower()
    exchange_rate = 24000

    if 'usd' in salary:
        salary_numeric = salary.replace('usd', '')
        multiplier = exchange_rate / 1_000_000
    elif 'vnd' in salary or 'triệu' in salary:
        salary_numeric = salary.replace('vnd', '').replace('triệu', '')
        multiplier = 1
    else:
        salary_numeric = salary
        multiplier = 1
    try:
        if '-' in salary_numeric:
            low_salary, high_salary = map(lambda x: int(x) * multiplier, salary_numeric.split('-'))
        elif any(keyword in salary_numeric for keyword in ['từ', 'from']) and any(keyword in salary_numeric for keyword in ['tới', 'upto']):
            low_salary, high_salary = map(lambda x: int(x) * multiplier, re.findall(r'\d+', salary_numeric))
        elif 'tới' in salary_numeric or 'upto' in salary_numeric:
            low_salary, high_salary = None, int(re.search(r'\d+', salary_numeric).group(0)) * multiplier
        elif 'từ' in salary_numeric or 'from' in salary_numeric:
            low_salary, high_salary = int(re.search(r'\d+', salary_numeric).group(0)) * multiplier, None
        else:
            match = re.search(r'\d+', salary_numeric)
            low_salary = int(match.group(0)) * multiplier if match else None
            high_salary = None
    except ValueError:
        return None, None
    return low_salary, high_salary

def clean_data_topcv(df):
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
    df['min_salary'], df['max_salary'] = zip(*df['salary'].apply(clean_salary))
    df['experience'] = df['experience'].str.strip()
    df['education'] = df['education'].str.strip().str.title()
    df['type_of_work'] = df['type_of_work'].str.strip().str.title()
    return df