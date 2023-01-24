import pytest
from app import models

@pytest.fixture()
def test_votes(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote(authenticated_client, test_posts):
    res = authenticated_client.post('/votes', json={'post_id':test_posts[0].id, 'direction': 1})
    assert res.status_code == 201

def test_vote_twice(authenticated_client, test_posts, test_votes):
    res = authenticated_client.post('/votes', json={'post_id':test_posts[0].id, 'direction': 1})
    assert res.status_code == 409

def test_delete_vote(authenticated_client, test_posts, test_votes):
    res = authenticated_client.post('/votes', json={'post_id':test_posts[0].id, 'direction': 0})
    assert res.status_code == 201

def test_delete_vote_doesnotexist(authenticated_client, test_posts):
    res = authenticated_client.post('/votes', json={'post_id':test_posts[0].id, 'direction': 0})
    assert res.status_code == 404

def test_vote_doesnotexist(authenticated_client, test_posts):
    res = authenticated_client.post('/votes', json={'post_id':1111, 'direction': 1})
    assert res.status_code == 404

def test_vote_unauthenticated(client, test_posts):
    res = client.post('/votes', json={'post_id':test_posts[0].id, 'direction': 1})
    assert res.status_code == 401