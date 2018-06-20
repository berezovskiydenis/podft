# -*- coding: utf-8 -*-

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

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_persons_page(self):
        response = self.client.get('/persons')
        self.assertEqual(response.status_code, 200)

    def test_orgs_page(self):
        response = self.client.get('/orgs')
        self.assertEqual(response.status_code, 200)

    def test_docs_page(self):
        response = self.client.get('api/v1/doc')
        self.assertEqual(response.status_code, 200)
