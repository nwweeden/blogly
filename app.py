"""Blogly application."""
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'  #this is referencing the database that is created by the user
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    '''redirect to list of users'''
    return redirect('/users')

@app.route('/users')
def show_users():
    '''show list of users'''
    # update template
    return render_template('users.html')


@app.route('/users/new')
def add_new():
    '''show an add form for users'''


@app.route('/users/new', methods=['POST'])
def add_form_info():
    '''show list of users'''


@app.route('/users/<user-id>')
def show_user_info():
    '''show information about given user'''


@app.route('/users/<user-id>/edit')
def edit_user():
    '''edit user information'''


@app.route('/users/<user-id>/edit', methods=['POST'])
def commit_user_edits():
    '''process the edit form'''


@app.route('/users/<user-id>/delete', methods=['POST'])
def delete_user():
    '''delete the user'''