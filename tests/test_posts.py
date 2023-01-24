import pytest
from app import schemas

def test_get_posts(authenticated_client, test_posts):
    res = authenticated_client.get('/posts/')
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorized_get_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_get_post(authenticated_client, test_posts):
    res = authenticated_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200

def test_unauthorized_get_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_post_doesnotexist(authenticated_client, test_posts):
    res = authenticated_client.get('/posts/1111')
    assert res.status_code == 404

@pytest.mark.parametrize('title, content, published', [
    ('title new', 'content new', True),
    ('title new', 'content new', False),
    ('title new', 'content new', False),
])
def test_create_post(authenticated_client, test_user, test_posts, title, content, published):
    res = authenticated_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
    assert res.status_code == 201
    # created_post = schemas.PostResponse(**res.json())
    # assert created_post.owner == test_user['id']

def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post(authenticated_client, test_posts):
    res = authenticated_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_update_post(authenticated_client, test_posts):
    res = authenticated_client.put(f'/posts/{test_posts[0].id}', json={'title':'new', 'content':'new', 'id':test_posts[0].id})
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == 'new'

# other tests: unauthorized, does not exist, other users post