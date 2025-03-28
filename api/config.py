import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATE_LIMIT = 3  # 3 API calls per day
    RATE_LIMIT_EXPIRES = 86400  # 1 day in seconds