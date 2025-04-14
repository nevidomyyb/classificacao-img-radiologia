from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import os

load_dotenv()

DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')   

PASSWORD_ENCODED = quote_plus(PASSWORD)

DATABASE_URL = f'mysql+mysqldb://{USERNAME}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DATABASE}'

class DatabaseSession:
    
    _instance = None

    def __new__(cls, db_url=DATABASE_URL):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._instance._init_engine(db_url)
        return cls._instance

    def _init_engine(self, db_url=DATABASE_URL):
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        return self.SessionLocal()

    def close_session(self):
        self.SessionLocal.remove()