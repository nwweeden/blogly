from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """ Tests User model."""

    def setUp(self):
        """ Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Nick", last_name="Weeden", image_url="https://images.unsplash.com/photo-1596015751570-5469dd49f4da?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
        db.session.add(user) #can we add multiple things here?
        db.session.commit()
        self.user_id = user.id
        # user2 = User(first_name="Tram", last_name="Nguyen", image_url="https://images.unsplash.com/photo-1596015751570-5469dd49f4da?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
        #any test can find nick's id, by self.user_id
        #add tram's tram_id

        post = Post(title="fakeTitle", content="this is my fake content", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """ Clean up any foul transactions."""

        db.session.rollback()


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            # resp = client.get("/", data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            #scan through html, if it sees Nick Weeden, then it will pass
            self.assertIn("Nick Weeden", html)
            # self.assertIn("Tram Nguyen", html)
            self.assertNotIn("Wayne", html)



    def test_individual_user(self):
        with app.test_client() as client:
            #self.user_id
            print('test_individual_user:',self.user_id)
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Nick Weeden</h1>", html)
            # TODO:
            self.assertIn('fakeTitle', html)
            #scan through html, if it sees Nick Weeden, then it will pass
            self.assertNotIn("Tram Nguyen", html)
            

    def test_user(self):
        with app.test_client() as client:
            print('test_userId:',self.user_id)
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            #if you click on edit button, will it do that...
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<button>Save</button>", html)
            #scan through html, if it sees Nick Weeden, then it will pass
            self.assertIn("Weeden", html)
            self.assertNotIn("Tram Nguyen", html)


    #write a test for posting - posting form submission (users/new) to add a new user
    def test_new_user(self):
        with app.test_client() as client:
            #testuser = User(first_name="Lily", last_name="Wayne")
            user = {"first_name": "Lily", "last_name": "Wayne", "image_url": ""}
            # testuser.first_name, testuser.last_name
            resp = client.post("/users/new", data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Lily Wayne", html)
            self.assertNotIn("John", html)
            self.assertIn("Nick Weeden", html)

    
    def test_user_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Detail", html)
            self.assertIn("this is my fake content", html)
            self.assertNotIn('this shouldnt be in there!', html)
    

    def test_user_post_change(self):
        with app.test_client() as client:
            post = {f"title": "new title", "content": "this is the new content",'user_id': {self.user_id}}
            resp = client.post(f"/posts/{self.post_id}/edit", data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("new title", html)
            self.assertNotIn("fakeTitle", html)
