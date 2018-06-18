# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from decimal import Decimal

from app import create_app, db
from app.models import Org, Terrorist, User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserModelTest(BaseTest):
    def test_password_hashing(self):
        u = User(
            username='Foobar',
            password='foobar'
        )
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('foobar'))


class TerroristModelTest(BaseTest):
    lname = 'abdul'
    fname = 'zafar'
    mname = 'ofceebovich'
    iin = '858585123412'
    birthdate = datetime(1975, 1, 1)
    note = 'Ass hole'

    def test_terrorist_creation(self):
        t = Terrorist(
                lname=self.lname,
                fname=self.fname,
                mname=self.mname,
                iin=self.iin,
                birthdate=self.birthdate,
                note=self.note
            )
        self.assertEqual(t.fname, self.fname)
        self.assertEqual(t.lname, self.lname)
        self.assertEqual(t.mname, self.mname)
        self.assertEqual(t.birthdate, self.birthdate)
        self.assertEqual(t.iin, self.iin)
        self.assertEqual(t.note, self.note)

    def test_history_creation(self):
        t = Terrorist(
                lname=self.lname,
                fname=self.fname,
                mname=self.mname,
                iin=self.iin,
                birthdate=self.birthdate,
                note=self.note
        )

        hist = {
            'included': datetime(2017, 1, 1),
            'excluded': datetime(2018, 1, 1)
        }

        t.included = hist['included']
        t.excluded = hist['excluded']

        self.assertEqual(t.fname, self.fname)
        self.assertEqual(t.iin, self.iin)

        self.assertEqual(t.included, hist['included'])
        self.assertEqual(t.excluded, hist['excluded'])


class OrgModelTest(BaseTest):
    name = 'Isis'
    name_eng = 'Isis mazafaka'
    note = 'Ass hole'

    def test_org_creation(self):
        o = Org(
                name=self.name,
                name_eng=self.name_eng,
                note=self.note
            )
        self.assertEqual(o.name, self.name)
        self.assertEqual(o.name_eng, self.name_eng)
        self.assertEqual(o.note, self.note)

    def test_history_creation(self):
        o = Org(
                name=self.name,
                name_eng=self.name_eng,
                note=self.note
            )

        hist = {
            'included': datetime(2017, 1, 1),
            'excluded': datetime(2018, 1, 1)
        }

        o.included = hist['included']
        o.excluded = hist['excluded']

        self.assertEqual(o.name_eng, self.name_eng)
        self.assertEqual(o.name, self.name)

        self.assertEqual(o.included, hist['included'])
        self.assertEqual(o.excluded, hist['excluded'])


if __name__ == '__main__':
    unittest.main(verbosity=3)
