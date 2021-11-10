from jose import jwt
from app import schema
import pytest
from app.config import settings



#def test_root(client):
##    response = client.get("/")
#   assert response.json().get('message') == "Hello world"
#    assert response.status_code == 200

def test_create_user(client):
    response = client.post('/users/', 
    json={
        'email':'test5@gmail.com',
        'password':'test'
    })
    new_user = schema.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == 'test5@gmail.com'


def test_login_user(client, test_user):
    # scope of the fixture runs after each test when it's set to function
    response = client.post('/login', 
    data={
        'username': test_user['email'],
        'password':test_user['password']
    })
    login_res = schema.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get('user_id')
    assert response.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'

@pytest.mark.parametrize('email, password, status_code' ,[
    ('wrongemail@gmail.com', 'password123', 403),
    ('teserpo@gmail.com', 'wrong', 403),
    ('wrong@gmail.com', 'wrongpass', 403),
    (None, 'passwooow', 422),
    ('te@gmail.com', None, 422)
])
def test_incorrent_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={
        "username": email,
        'password': password
        })
    assert res.status_code == status_code