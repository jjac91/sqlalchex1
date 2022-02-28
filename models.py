from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_url = "https://as2.ftcdn.net/v2/jpg/03/49/49/79/1000_F_349497933_Ly4im8BDmHLaLzgyKg2f2yZOvJjBtlw5.jpg"


class User(db.Model):
    """User of Blogly"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_url)

    @property
    def full_name(self):
        "returns the first and last name of a user"

        return f'{self.first_name} {self.last_name}'


def connect_db(app):
    """Connects to database."""

    db.app = app
    db.init_app(app)
