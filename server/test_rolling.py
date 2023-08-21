import unittest
from rolling import app
import json

class TestRolling(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_data(self):
        # Test with valid data
        data = {
            'uuid': '1234',
            'message': 'Hello, world!',
            'colorpicker': '#ff0000'
        }
        response = self.app.post('/update', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'success', 'message': 'data updated'})

        # make sure the data has been written to the file
        with open('uuid/1234', 'r') as f:
            self.assertEqual(json.loads(f.read()), {'color': '#ff0000', 'message': 'Hello, world!'})
    
    # Test with invalid data
    def test_submit_data_invalid(self):

        data = {
            'uuid': '',
            'message': '',
            'colorpicker': ''
        }
        response = self.app.post('/update', data=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.data), {'status': 'error', 'message': 'something went wrong'})
    
    # clean up the file
    def tearDown(self):
        # remove the file(if exists)
        try:
            import os
            os.remove('uuid/1234')
        except:
            pass

if __name__ == '__main__':
    unittest.main()