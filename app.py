#!usr/bin/python

from flask import Flask , render_template , request , redirect , session , abort , url_for , g 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager , login_user  , login_required , logout_user , current_user 
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.sql import text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine

# Models
# Flask app intitialization 

app = Flask(__name__)
app.config.from_pyfile('config.py')

# SQLAlchemy initialization 
import MySQLdb
db = SQLAlchemy(app)

from models import login_model

# # Flask Login Initiialization 

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
    form = login_model.LoginForm()
    mssg = ""

    if form.validate_on_submit():
        user = login_model.User.query.filter_by(email=form.email.data).first()
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
    form = login_model.SignupForm()
    mssg = ""
    if form.validate_on_submit():
        user = login_model.User.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pass = generate_password_hash(form.password.data , method='sha256')
            new_user = login_model.User(username = form.username.data , email = form.email.data , password = hashed_pass)
            # user_table = UserTableCreator(form.email.data)
            # Base.metadata.create_all(engine)        
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
    return login_model.User.query.get(int(user_id))

# Function Routes

@app.route('/contacts' , methods=['GET' , 'POST'])
@login_required
def contacts():
    '''
        Add contacts to database with option to export 
        and import data onto Peep.
    '''
    user = current_user.username 
    return render_template('contacts.html' , user = user) , 200

@app.route('/insights' , methods=['GET' , 'POST'])
@login_required
def insights():
    '''
        Get insights based of various filters 
            - Period
            - Business Category
            - Product dealing IN
            - City
            - State
            - Country
            - Customer Credit Health
            - broker
            - preffered Comm channel
            - no of times comm done
            - No fo Invoice
            - Sales for that user
    '''
    pass


@app.route('/basic_master' , methods=['GET' , 'POST'])
@login_required
def basic_master():
    '''
        Basic master setup done here
    '''
    user = current_user.username 
    return render_template('basic-master.html' , user = user) , 200

@app.route('/user_profile' , methods=['GET' , 'POST'])
@login_required
def user_profile():
    '''
        Basic master setup done here
    '''
    pass
