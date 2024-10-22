import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@db/rule_engine?charset=utf8mb4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False