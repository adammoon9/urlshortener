import unittest
import pytest
from app import create_app

class testURLSAPI(unittest.TestCase):

    deleteShortCode = None

    def test_get_url_endpoint(self):
        with create_app().test_client() as tc:
            response = tc.get('/shorten/abc123')
            response_json = response.get_json()
            
            valid_response = {'createdAt': 'Sat, 17 May 2025 00:00:00 GMT', 'id': 0, 'shortCode': 'abc123', 'updatedAt': 'Sat, 17 May 2025 15:45:19 GMT', 'url': 'test123'}
            old_timestamp = valid_response.pop('updatedAt')
            new_timestamp = response_json.pop('updatedAt')
            
            self.assertNotEqual(old_timestamp, new_timestamp) # Test that the updated at actually changes 
            self.assertDictEqual(response_json, {'createdAt': 'Sat, 17 May 2025 00:00:00 GMT', 'id': 0, 'shortCode': 'abc123', 'url': 'test123'})
            self.assertTrue(response.status_code == 200) # Check the resposne code now that the static result data has been checked

    def test_get_url_endpoint_404(self):
        with create_app().test_client() as tc:
            response = tc.get('/shorten/0')
            response_json = response.get_json()

            assert response_json == {'msg': 'URL Not Found'}
            self.assertTrue(response.status_code == 404)


    def test_get_api_statistics_endpoint(self):
        with create_app().test_client() as tc:
            response = tc.get('/shorten/abc123/stats')
            response_json = response.get_json()

            self.assertIn('accessCount', response_json)
            self.assertTrue(type(response_json['accessCount']) == int)

    def test_post_url_endpoint(self):
        with create_app().test_client() as tc:
            response = tc.post('/shorten', json={
                'url': 'https://test.url/123'
            })
            response_json = response.get_json()
            
            self.assertIsNotNone(response_json)
            self.assertTrue(response.status_code == 201)
            testURLSAPI.deleteShortCode = response_json['shortCode']

    def test_post_url_endpoint_no_url(self):
        with create_app().test_client() as tc:
            response = tc.post('/shorten', json={})
            response_json = response.get_json()

            self.assertTrue(response_json == {'msg': 'Invalid URL or URL Not found in request data.'})
            self.assertTrue(response.status_code == 400)

    def test_update_url_endpoint(self):
        with create_app().test_client() as tc:
            response = tc.put('/shorten/abc123', json={'url': 'test123'})
            response_json = response.get_json()

            valid_response = {'createdAt': 'Sat, 17 May 2025 00:00:00 GMT', 'id': 0, 'shortCode': 'abc123', 'updatedAt': 'Sat, 17 May 2025 15:45:19 GMT', 'url': 'test123'}
            old_timestamp = valid_response.pop('updatedAt')
            new_timestamp = response_json.pop('updatedAt')
            
            self.assertNotEqual(old_timestamp, new_timestamp) # Test that the updated at actually changes 
            self.assertDictEqual(response_json, {'createdAt': 'Sat, 17 May 2025 00:00:00 GMT', 'id': 0, 'shortCode': 'abc123', 'url': 'test123'})
            self.assertTrue(response.status_code == 200) # Check the resposne code now that the static result data has been checked

    def test_update_url_endpoint_no_url(self):
        with create_app().test_client() as tc:
            response = tc.put('/shorten/abc123', json={})
            response_json = response.get_json()

            self.assertTrue(response_json == {'msg': 'Invalid URL or URL Not found in request data.'})
            self.assertTrue(response.status_code == 400)

    @pytest.mark.depends(on=['test_post_url_endpoint'])
    def test_delete_url_endpoint(self):
        with create_app().test_client() as tc:
            response = tc.delete(f'/shorten/{testURLSAPI.deleteShortCode}')

            self.assertTrue(response.status_code == 204)
