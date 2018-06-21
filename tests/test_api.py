# -*- coding: utf-8 -*-

import json
import unittest

from flask import url_for

from app import create_app, db
from app.models import Terrorist


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Terrorist.init_active()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'].lower(), 'not found')

    def test_400_terrorist(self):
        response = self.client.get('/api/v1/terrorist')
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'].lower(), 'bad request')

    def test_400_terrorist_name(self):
        response = self.client.get('/api/v1/terrorist?lname=a')
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'].lower(), 'bad request')
        self.assertIn('fname', json_response['message'].lower())

    def test_400_org(self):
        response = self.client.get('/api/v1/org')
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'].lower(), 'bad request')
        self.assertIn('name', json_response['message'].lower())
