from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for model for User"""

    def setUp(self):
        """Clean up any existing users"""

        User.query.delete()

        user = User(first_name="Test", last_name="Testing", image_url="www.test.com")
        db.session.add(user)
        db.session.commit()

        self.user_id=user.id
        self.user=user

    def tearDown(self):

        db.session.rollback()

    def test_list_users(self):
        with app.test_client as client:
            resp = client.get('/')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 302)

    def test_user_info(self):
        with app.test_client as client:
            resp = client.get('users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)


    def test_delete_user(self):
        with app.test_client as client:
            resp = client.get('users/{self.user_id}/delete')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
