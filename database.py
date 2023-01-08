import os
import ssl

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ['MAV_CANARY_MYSQL_USERNAME']
password = os.environ['MAV_CANARY_MYSQL_PASSWORD']
host = os.environ['MAV_CANARY_MYSQL_HOST']

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/contact_manager"

ssl_context = ssl.create_default_context(cafile=os.environ['MAV_CANARY_CA_PATH'])
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_args = {"ssl": ssl_context}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=ssl_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
