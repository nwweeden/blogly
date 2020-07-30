from unittest import TestCase

from app import app
from models import db, Pet

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
    """Tests for user list."""

        def SetUp(self):
        """ Clear existing users."""

        User.query.delete()

    def setUp(self):
        """ Add sample user."""

        User.query.delete()

        user = User(first_name="Tram", last_name="Nguyen", image_url="https://images.unsplash.com/photo-1596015751570-5469dd49f4da?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
        db.session.add(user)
        db.session.commit()

        self.id = user.id
