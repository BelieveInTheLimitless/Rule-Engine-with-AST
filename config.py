import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://user:password@localhost/rule_engine')
    SQLALCHEMY_TRACK_MODIFICATIONS = False