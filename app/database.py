from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.base import SQL_OK

#user = os.getenv("USER")
#password = os.getenv("PASSWORD")
#url = os.getenv("DBURL")
#db = os.getenv("DATABASE")

#SQLalchemy_database_URL = f'postgresql://{user}:{password}@{url}/{db}'
SQLalchemy_database_URL = "postgresql://postgres:postgres123@localhost/fastapi"
engine = create_engine(SQLalchemy_database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
