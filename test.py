from email import contentmanager
from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user and sample post."""

        db.drop_all()
        db.create_all()

        self.user = User(first_name='Kaguya', last_name='Shinomiya',
                         image_url='https://cdn.anime-planet.com/characters/primary/kaguya-shinomiya-1-190x266.jpg?t=1625997672')
        db.session.add(self.user)
        db.session.commit()

        test_post = Post(title="test", content="test content", user_id=1)
        db.session.add(test_post)
        db.session.commit()

        self.user_id = self.user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Kaguya', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Kaguya Shinomiya</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            sam = {"first_name": 'Sam', "last_name": 'Wise', "image_url": ""}
            resp = client.post("/users/new", data=sam, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sam", html)

    def test_base_redirect(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Users', html)

    def test_list_post(self):
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test', html)
