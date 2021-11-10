from fastapi import testclient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.main import app    
from app.config import settings
from app.database import get_db, Base
import pytest



SQLalchemy_database_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLalchemy_database_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    # this fixture allows us to have access to the client object
    Base.metadata.drop_all(bind=engine) # dropping tables at the start lets you examine them after failing tests
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
    #testing dependencies with override
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # The code above the yield statement will run before the tests
    yield TestClient(app)
    # And the code below it runs after the test

