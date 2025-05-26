import pytest
import os
from app import create_app
from app.extensions import db
from app.models.url import URL
from app.db_helper import DBHelper as test_db_helper

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def short_code():
    url = URL(url='https://test.url/123', shortCode='abc123')
    db.session.add(url)
    db.session.commit()

    return url.shortCode

@pytest.fixture
def my_urls():
    url = URL(url='https://test.url/123', shortCode='abc123')
    db.session.add(url)
    db.session.commit()

    return url
    

@pytest.fixture
def app():
    app = create_app(config_object=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        # teardown
        db.session.remove()
        db.drop_all()
        os.remove('./instance/test.db')

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_url_endpoint(client, short_code):

    response = client.get(f'/shorten/{short_code}')
    
    assert response.status_code == 200
    assert response.get_json()['url'] == 'https://test.url/123'

def test_get_url_endpoint_404(client):
    response = client.get('/shorten/0')
    
    assert response.status_code == 404
    assert response.get_json() == {'msg': 'URL Not Found'}

def test_get_api_statistics_endpoint(client, short_code):

    response1 = client.get(f'/shorten/{short_code}/stats')
    response2 = client.get(f'/shorten/{short_code}/stats')
    
    access_count1 = response1.get_json()['accessCount']
    access_count2 = response2.get_json()['accessCount']

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert access_count1 + 1 == access_count2

def test_get_api_statistics_endpoint_404(client):
    response = client.get('/shorten/0/stats')

    assert response.status_code == 404
    assert response.get_json() == {'msg': 'URL Not Found'}

def test_post_url_endpoint(client):
    response = client.post('/shorten', json={
        'url': 'https://test.url/123'
    })

    assert response.get_json()['url'] == 'https://test.url/123'
    assert response.status_code == 201

def test_post_url_endpoint_no_url(client):
    response = client.post('/shorten', json={})

    assert response.status_code == 400
    assert response.get_json() == {'msg': 'Invalid URL or URL Not found in request data.'}

def test_update_url_endpoint(client, short_code):
    response = client.put(f'shorten/{short_code}', json={'url': 'test123'})
    
    assert response.status_code == 200
    assert response.get_json()['url'] == 'test123'

def test_update_url_endpoint_no_url(client, short_code):
    response = client.put(f'shorten/{short_code}', json={})
    
    assert response.status_code == 400
    assert response.get_json() == {'msg': 'Invalid URL or URL Not found in request data.'}

def test_update_url_endpoint_404(client):
    response = client.put('/shorten/0', json={'url': ''})

    assert response.status_code == 404
    assert response.get_json() == {'msg': 'URL Not Found'}

def test_delete_url_endpoint(client, short_code):
    response = client.delete(f'/shorten/{short_code}')
    
    assert response.status_code == 204

def test_delete_url_endpoint_404(client):
    response = client.delete('/shorten/0')

    assert response.status_code == 404

# These tests need the client for the set up and teardown of the test DB
def test_get_my_urls(client, my_urls):
    urls = test_db_helper.get_my_urls()

    assert urls[0] == my_urls.serialize()

def test_get_my_urls_empty(client):
    urls = test_db_helper.get_my_urls()
    assert urls == None