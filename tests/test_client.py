import re
import unittest
from app import create_app, db
from app.models import Role, User


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))
        #response.data is in binary form but .get_data can be converted to text by\
        # as_text=True or you can just convert your string by add 'b' in front of them.
        # I'm using 'em in next codes.

    def test_register_and_login(self):
        # register a new account
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertEqual(response.status_code, 302)

        # login with new account
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(b'Hello, john!', response.data))
        self.assertTrue(b'You have not confirmed your account yet.' in response.data)

        # send a confirmation token
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Password' in response.get_data(as_text=True))

        # logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been logged out' in response.data)

    def test_unusual_registration(self):
        response = self.client.post('/auth/register', data={
            'email': 'john',
            'username': 'john wick',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertFalse(response.status_code == 302)