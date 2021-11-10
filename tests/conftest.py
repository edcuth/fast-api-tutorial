from fastapi import testclient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.main import app    
from app.config import settings
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models


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

@pytest.fixture
def test_user(client):
    # creates a mock user to test login
    user_data = {
        "email":"test1@gmail.com",
        "password":"test"}
    response = client.post("/users/", json=user_data)
    assert response.status_code ==201
    new_user = response.json()
    new_user['password'] = user_data['password']
    yield new_user

@pytest.fixture
def test_user2(client):
    # creates a mock user to test login
    user_data = {
        "email":"test2@gmail.com",
        "password":"test"}
    response = client.post("/users/", json=user_data)
    assert response.status_code ==201
    new_user = response.json()
    new_user['password'] = user_data['password']
    yield new_user



@pytest.fixture
def token(test_user):
    # creates a token string to authorize a client
    yield create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorize_client(client, token):
    # adds the token authorization to the header
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    yield client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [{
        'title':'first title',
        'content':'first content',
        'owner_id': test_user['id']
    }, {
        'title':'second title',
        'content':'second content',
        'owner_id':test_user['id']
    }, {
        'title':'third title',
        'content':'third content',
        'owner_id':test_user['id']
    }, {
        'title':'forth title',
        'content':'forth content',
        'owner_id':test_user2['id']
    }]

    def create_post_model(post_dic):
        return models.Post(**post_dic)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    queried_posts = session.query(models.Post).all()
    return queried_posts