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
    # get all user instances
    users = User.query.all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def show_form():
    '''show an add form for users'''

    return render_template("newUser.html")


@app.route('/users/new', methods=['POST'])
def add_form_info():
    '''show list of users'''

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["image_url"]
    # print('first name', first_name)

    #add this user's inputs to the database
    user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(user)
    db.session.commit()

    # redirect to "/users" list
    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    '''show information about given user'''

    user = User.query.get_or_404(user_id)
    return render_template("userDetail.html", user=user)



@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''edit user information'''

    user = User.query.get(user_id)

    return render_template("editUser.html", user=user)



@app.route('/users/<int:user_id>/edit', methods=['POST'])
def commit_user_edits(user_id):
    '''process the edit form'''

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["image_url"]

    # if user press cancel do we write another redirect to their own page
    # if cancel button was click, return redirect(f"/users/{user_id}")
    user = User.query.get(user_id)
    
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = url
        
    # add changes to the user in the database
    db.session.commit()

    # how do we route to the user that's been updated!
    # new_user_inDb = User.query.filter(User.id == user_id)
    # newUser = user.id
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''delete the user'''

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")