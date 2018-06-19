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
    form = login_model.AddContact()
    mssg = ""

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

    mssg = ""
    user = current_user.username 
    form_broker = login_model.BrokerForm()
    form_comm = login_model.CommChannelForm()
    form_health = login_model.HealthCodeForm()
    form_prod = login_model.ProdCatForm()
    form_buss = login_model.BussCatForm()
    form_state = login_model.StateForm()
    form_coun = login_model.CountryForm()
    form_city = login_model.CityForm()


    prod_list = db.session.query(login_model.ProdCat).all()
    health_list = db.session.query(login_model.HealthCode).all()
    commlist = db.session.query(login_model.HealthCode).all()
    busslist = db.session.query(login_model.BussCat).all()
    broklist = db.session.query(login_model.Broker).all()
    statelist = db.session.query(login_model.State).all()
    countrylist = db.session.query(login_model.Country).all()
    citylist = db.session.query(login_model.City).all()

    if form_broker.validate_on_submit():
        # Checks for Broker submit 
        pass

    if form_comm.validate_on_submit():
        # Checks for Comm submit 
        pass
    if form_health.validate_on_submit():
        # Checks for health code submit 
        mssg = ""
        print('ohh')
        prod = login_model.HealthCode.query.filter_by(health=form_health.health.data).first()
        print(prod)
        print('ok')
        if prod :
            mssg = "Duplicate Data "
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.HealthCode(health=form_health.health.data.upper())  
            print(new_data)
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                return redirect(url_for('basic_master'))

    if form_prod.validate_on_submit():
        mssg = ""
        prod = login_model.ProdCat.query.filter_by(prod_cat=form_prod.prod_cat.data).first()

        if prod :
            mssg = "Duplicate Data "
            return redirect(url_for('basic_master'))

        else:
            new_data = login_model.ProdCat(prod_cat = form_prod.prod_cat.data.upper())  
            try:
                db.session.add(new_data)
                db.session.commit()
                mssg = "Data Successfully added 👍"
                return redirect(url_for('basic_master'))

            
            except Exception as e:
                mssg = "Error occured while adding data 😵. Here's the error : "+str(e)
                return redirect(url_for('basic_master'))

    if form_buss.validate_on_submit():
        # Checks for Bussiness Category submit
        pass
    if form_state.validate_on_submit():
        # Checks for Location submit
        pass
    return render_template('basic_master.html' , user = user , 
        form_broker = form_broker , form_buss = form_buss , form_comm = form_comm ,
        form_health = form_health , form_state = form_state , form_prod = form_prod ,
        error_mssg = mssg , subtitle = "Basic Master" , plist = prod_list ,
        hlist = health_list , commlist = commlist , busslist = busslist , broklist = broklist , statelist = statelist) , 200


@app.route('/delete/<item_id>' , methods=['GET', 'POST'])
@login_required
def delete_data_prod(item_id):
    '''
        Deletes data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a signle routes for delete in multiple tables
        
    '''
    login_model.ProdCat.query.filter_by(id=int(item_id)).delete()
    db.session.commit()
    mssg = "Data Successfully deleted"
    return redirect(url_for('basic_master'))

@app.route('/edit/<item_id>' , methods=['GET' , 'POST'])
@login_required
def edit_data_prod(item_id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id

        ** FIX : Needs refactoring , using a single routes for delete in multiple tables
        
    '''
    prod_model = login_model.ProdCat.query.filter_by(id=int(item_id)).first()
    prod_model.prod_cat = request.form['edit_input'].upper()
    db.session.commit()
    mssg = "Data Successfully Edited" 
    return redirect(url_for('basic_master'))

@app.route('/user_profile' , methods=['GET' , 'POST'])
@login_required
def user_profile():
    '''
        Basic master setup done here
    '''
    pass
