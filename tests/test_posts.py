from fastapi import responses
import pytest

from _pytest.outcomes import TEST_OUTCOME
from app import schema

def test_get_all_posts(authorize_client, test_posts):
    response = authorize_client.get('/posts/')
    def validate(post):
        return schema.PostOut(**post)
    posts_map = map(validate, response.json())
    post_list = list(posts_map) # the pydantic model will make sure all the posts fullfil the model's criteria
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_one_post(authorize_client, test_posts):
    response = authorize_client.get(f'/posts/{test_posts[0].id}')
    post = schema.PostOut(**response.json()) #pydantic model provides validation
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize('title, content, published', [
    ('this is a very titly title', 'some content', True),
    ('Another cool title', 'Some even cooler content', False),
    ('rice is cool', 'very cool', True)
])
def test_create_post(authorize_client, test_user, test_posts, title, content, published):
    response = authorize_client.post('/posts/', json={'title':title, 'content':content, 'published':published})
    created_post = schema.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_post_default_published_true(authorize_client, test_user, test_posts):
    response = authorize_client.post('/posts/', json={'title':'some title', 'content':'some content'})
    created_post = schema.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == 'some title'
    assert created_post.content == 'some content'
    assert created_post.published == True

def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post('/posts/', json={'title':'some title', 'content':'some content'})
    assert response.status_code == 401

    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401

def test_delete_post_success(authorize_client, test_user, test_posts):
    response = authorize_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204

def test_delete_post_non_existant(authorize_client, test_user, test_posts):
    response = authorize_client.delete('/posts/552')
    assert response.status_code == 404

def test_delete_other_user_post(authorize_client, test_user, test_posts):
    response = authorize_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403

def test_update_post(authorize_client, test_user, test_posts):
    data = {
        'title': 'updated tite',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    response = authorize_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schema.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorize_client, test_user, test_posts, test_user2):
    data = {
        'title': 'updated tite',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    response = authorize_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert response.status_code == 403

def test_update_post_unauthorized_user(client, test_user, test_posts):
    data = {
        'title': 'updated tite',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    response = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 401

def test_update_post_non_existant(authorize_client, test_user, test_posts):
    data = {
        'title': 'updated tite',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    response = authorize_client.delete('/posts/552', json=data)
    assert response.status_code == 404

