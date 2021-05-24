from flask_testing import TestCase
from flask import url_for
from wtforms.fields.core import StringField

from application import app, db
from application.models import Owner, Pet

class TestBase(TestCase):
    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
        app.config["SECRET_KEY"] = "ANYTHING"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = True
        return app

    def setUp(self):
        db.create_all()

        test_pet_sitter = Owner(first_name="This is a test")
        db.session.add(test_pet_sitter)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):
    def test_home_page_get(self):
        response = self.client.get(url_for("index"))
        self.assertIn(b"This is a test", response.data)
        self.assertEqual(response.status_code, 200)

class TestViews2(TestBase):
    def test_home_page_get2(self):
        response = self.client.get(url_for("add"))
        self.assertIn(b"Home", response.data)
        self.assertEqual(response.status_code, 200)


class TestViews3(TestBase):
    def test_home_page_get3(self):
        response = self.client.get(url_for("delete", owner_id=1))
        all_owners = Owner.query.count()
        self.assertEqual(all_owners, 0)


class TestViews4(TestBase):
    def test_home_page_get4(self):
        response = self.client.get(url_for("update", owner_id=1))
        all_owners = Owner.query.count()
        self.assertEqual(all_owners, 1)
