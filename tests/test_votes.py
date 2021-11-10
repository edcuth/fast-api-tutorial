import pytest
from app import models


@pytest.fixture
def create_post_with_vote(test_posts, session, test_user):
    vote = models.Votes(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(vote)
    session.commit()
    

def test_vote_on_post(authorize_client, test_posts):
    response = authorize_client.post('/vote/', json={
        'post_id':test_posts[3].id,
        'dir':1
        })
    assert response.status_code == 201


def test_vote_twice_on_post(authorize_client, test_posts, create_post_with_vote):
    response = authorize_client.post('/vote/', json={
        'post_id':test_posts[3].id,
        'dir':1
        })
    assert response.status_code == 409

def test_remove_vote(authorize_client, test_posts, create_post_with_vote):
    response = authorize_client.post('/vote/', json={
        'post_id':test_posts[3].id,
        'dir':0
        })
    assert response.status_code == 201

def test_remove_vote_with_no_vote(authorize_client, test_posts):
    response = authorize_client.post('/vote/', json={
        'post_id':test_posts[3].id,
        'dir':0
        })
    assert response.status_code == 404

def test_remove_vote_non_exist(authorize_client, test_posts):
    response = authorize_client.post('/vote/', json={
        'post_id':8000000,
        'dir':1
        })
    assert response.status_code == 404

def test_vote_unautorized_user(client, test_posts):
    response = client.post('/vote/', json={
        'post_id':test_posts[3].id,
        'dir':1
        })
    assert response.status_code == 401