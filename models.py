from email.policy import default
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

default_url = "https://as2.ftcdn.net/v2/jpg/03/49/49/79/1000_F_349497933_Ly4im8BDmHLaLzgyKg2f2yZOvJjBtlw5.jpg"


class User(db.Model):
    """User of Blogly"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_url)

    posts = db.relationship('Post', backref='user')

    @property
    def full_name(self):
        "returns the first and last name of a user"

        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post of Blogly Users"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


def connect_db(app):
    """Connects to database."""

    db.app = app
    db.init_app(app)
