import json
import unittest
from server import app, db
from server.models import User, ExpiredToken
from flask_testing import TestCase

def login(self, username, password):
    return self.client.post(
        'api/login',
        data=json.dumps(dict(
            username=username,
            password=password,
        )),
        content_type='application/json',
    )


def logout(self, token):
    return self.client.post(
        'api/logout',
        headers={'Authorization': 'Bearer {}'.format(token)},
        content_type='application/json',
    )

def fetch_data(self, token):
    return self.client.get(
        'api/logs',
        headers={'Authorization': 'Bearer {}'.format(token)},
        content_type='application/json',
    )



class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class AuthTestCase(BaseTestCase):
    """
    Auth Test case
    """
    def test_login(self):

        #check non registered user login
        with self.client:
            resp = login(self, 'test', '11112')
            resp_data = json.loads(resp.data.decode())
            self.assertTrue(resp_data['msg'] == 'Try again!')
            self.assertEqual(resp.status_code, 400)

            #register new user
            user = User(name='Test', last_name='Test', password='12343', username='test')
            db.session.add(user)
            db.session.commit()

            # try login again
            resp = login(self, 'test', '12343')
            resp_data = json.loads(resp.data.decode())
            self.assertTrue(resp_data['access_token'])
            self.assertEqual(resp.status_code, 200)


    def test_logout(self):

        with self.client:
            #register new user
            user = User(name='Test1', last_name='Test1', password='12343', username='test1')
            db.session.add(user)
            db.session.commit()

            # try login again
            resp = login(self, 'test1', '12343')
            resp_data = json.loads(resp.data.decode())
            self.assertTrue(resp_data['access_token'])
            self.assertEqual(resp.status_code, 200)

            # try fetch protected data
            protected_data = fetch_data(self, resp_data['access_token'])
            self.assertEqual(protected_data.status_code, 200)

            #logout
            resp_logout = logout(self, resp_data['access_token'])
            self.assertEqual(resp_logout.status_code, 200)

            #try fetch protected data again
            protected_data = fetch_data(self, resp_data['access_token'])
            self.assertEqual(protected_data.status_code, 401)

if __name__ == '__main__':
    unittest.main()
