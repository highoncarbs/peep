#!usr/bin/python

from flask import Flask , render_template , request , redirect , session , abort , url_for , g 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager , login_user  , login_required , logout_user , current_user 
from flask_wtf import FlaskForm 
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Models
from models import login_model

# Flask app intitialization 

app = Flask(__name__)
# app.config.from_pyfile('congig.py')

# SQLAlchemy initialization 

db = SQLAlchemy(app)

# Flask Login Initiialization 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base route 
@app.route('/' , methods = ['GET' , 'POST'])
@login_required
def index():
    user = current_user.username 
    return render_template('base.html' , user = user) , 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    """
    form = LoginForm()
    mssg = ""

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)

                return redirect(url_for('index'))
            else:
                return render_template('login.html', subtitle="Login", form=form, error_mssg="Invalid Username or Password")
        else:
            return render_template('login.html', subtitle="Login", form=form, error_mssg="Invalid Username or Password")
    return render_template('login.html', subtitle="Login", form=form, error_mssg=mssg), 200


@app.route('/signup' , methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    mssg = ""
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pass = generate_password_hash(form.password.data , method='sha256')
            new_user = User(username = form.username.data , email = form.email.data , password = hashed_pass)
            user_table = UserTableCreator(form.email.data)
            Base.metadata.create_all(engine)        
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('signup.html' , form = form ,subtitle = "Signup" ,error_mssg = "Email already exists.")

    return render_template('signup.html' , subtitle = "Signup" , form = form , error_mssg = mssg),200

@app.route('/forgot' , methods=['GET', 'POST'])
def forgot():
    return render_template('login.html' , subtitle = "Forgot"),200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
