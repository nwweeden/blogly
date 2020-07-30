"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=False, default='')  #should we include a default image???

    posts = db.relationship('Post')

    def __repr__(self):
        '''Show info about the user'''

        u = self
        return f'<User {u.id} {u.first_name} {u.last_name} {u.image_url}>'


class Post(db.Model):
    '''Post.'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False, default='')
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now) #is this how you do timestamp?
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))
    
    user = db.relationship('User')

    def __repr__(self):
        '''Show info about the user'''

        p = self
        return f'<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>'