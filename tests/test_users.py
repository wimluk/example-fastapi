import pytest
from app import schemas
from app.config import settings
from jose import jwt

# def test_root(client):
#     res = client.get('/')
#     # print(res.json().get('detail'))
#     assert res.json().get('detail') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):

    # test create user
    res = client.post('/users/', json={'email':'user@gmail.com', 'password':'password'})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201

def test_login_user(client, test_user):
    
    # test login user and verify the access token
    res = client.post('/login', data={'username':test_user['email'], 'password':test_user['password']})
    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password', 403),
    ('user@gmail.com', 'wrongPassword', 403),
    ('wrongemail@gmail.com', 'wrongPassword', 403),
    (None, 'password', 422),
    ('user@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid User or Password'