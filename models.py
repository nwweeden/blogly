"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

class Post(db.Model):
    '''Post.'''

    __tablename__ = 'posts'

    id = db.Column(db.integer, primary_key=True)
    title = db.Column(db.string(50), nullable=False)
    content = db.Column(db.string(1000), nullable=False, default='')
    created_at = db.Column(db.'timestammp with time zone',nullable=false, default=Current_Timestamp) #is this how you do timestamp?
    user_id = db.column(
        db.string, #what's the difference between txt and string?
        db.ForeignKey(users.id))
    
    user = db.relationship('User')