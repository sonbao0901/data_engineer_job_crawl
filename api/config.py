import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATE_LIMIT = 3  # 3 API calls per day
    RATE_LIMIT_EXPIRES = 86400  # 1 day in seconds
    SECRET_KEY = os.getenv('SECRET_KEY')