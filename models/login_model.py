from wtforms import StringField, PasswordField , BooleanField
from wtforms.validators import InputRequired, Email, Length , DataRequired
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from app import db

########################################
#######  APP LOGIN FORMS & DB ##########
########################################

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    # remember = BooleanField('remember')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Keep me Logged In')
    email = StringField('email', validators=[InputRequired(), Email(
        message="Invalid Email"), Length(max=50)])

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)    


########################################
####### BASIC MASTER FORMS & DB ########
########################################

class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broker_name = db.Column(db.String(30), unique=True, nullable=False)
    city = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), unique=True, nullable=False)
    contact =  db.Column(db.String(30), unique=True, nullable=False)

class BrokerForm(FlaskForm):
    broker_name = StringField('broker_name', validators=[InputRequired()])
    city = StringField('city', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    country = StringField('country', validators=[InputRequired()])
    contacts = StringField('country', validators=[InputRequired()])

class CommChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(30), unique=True, nullable=False) 

class CommChannelForm(FlaskForm):
    comm_channel = StringField('comm_channel', validators=[InputRequired()])

class HealthCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_code = db.Column(db.String(5), unique=True, nullable=False)

class HealthCodeForm(FlaskForm):
    health_code = StringField('health_code', validators=[InputRequired()])

    
class ProdCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_cat = db.Column(db.String(30), unique=True, nullable=False) 

class ProdCatForm(FlaskForm):
    prod_cat = StringField('prod_cat', validators=[InputRequired()])

    
class BussCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buss_Cat = db.Column(db.String(30), unique=True, nullable=False) 

class BussCatForm(FlaskForm):
    buss_cat = StringField('buss_cat', validators=[InputRequired()])

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), unique=True, nullable=False)

class LocationForm(FlaskForm):
    city = StringField('city', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    country = StringField('country', validators=[InputRequired()])

########################################
####### CONTACT FORMS & DB #############
########################################

class AddContactForm(FlaskForm):
    pass

class AddContact(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(50) , nullable = False)
    contact_one = db.Column(db.String(20) , nullable = True)
    wh_contact = db.Column(db.String(20) , nullable = True)
    email = db.Column(db.String(50) , unique = True , nullable = True)
    country = db.Column(db.String(30) , nullable = True)
    state = db.Column(db.String(20) , nullable = True)
    city = db.Column(db.String(20) , nullable = True)
    buss_cat = db.Column(db.String(20) , nullable = True)
    prod_cat = db.Column(db.String(20) , nullable = True)
    broker = db.Column(db.String(20) , nullable = True)
    comm_channel = db.Column(db.String(20) , nullable = True)

########################################
####### MSSGs FORMS & DB ###############
########################################

class Mssgs(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    type_mssg = db.Column(db.String(20) , nullable =True)
    mssg = db.Column(db.String(500) , nullable = True)

class MssgsForm(FlaskForm):
    pass