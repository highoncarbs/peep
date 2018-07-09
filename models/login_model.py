from wtforms import StringField, PasswordField , BooleanField , DateField
from wtforms.widgets import TextArea
from wtforms_alchemy.fields import QuerySelectField ,SelectMultipleField ,SelectField
from wtforms.validators import InputRequired, Email, Length , DataRequired ,Regexp
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from app import db
import datetime

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
####### QUERY FACTORY METHODS ##########
########################################

def state_choice():
    return db.session.query(State)

def country_choice():
    return db.session.query(Country)

def city_choice():
    return db.session.query(City)

def prod_choice():
    return db.session.query(ProdCat)

def broker_choice():
    return db.session.query(Broker)

def health_choice():
    return db.session.query(HealthCode)

def comm_choice():
    return db.session.query(CommChannel)

def buss_choice():
    return db.session.query(BussCat)

def contact_choice():
    return db.session.query(AddContact)

def firm_choice():
    return db.session.query(Firm)

def group_choice():
    return db.session.query(Group)

def contact_choice():
    return db.session.query(AddContact)


########################################
####### BASIC MASTER FORMS & DB ########
########################################

# Broker Model & Form

class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broker_name = db.Column(db.String(30), unique=True, nullable=False)
    city = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(30), unique=True, nullable=False)
    country = db.Column(db.String(30), unique=True, nullable=False)
    contact =  db.Column(db.String(30), unique=True, nullable=False)

class BrokerForm(FlaskForm):
    broker_name = StringField('broker_name', validators=[InputRequired()])
    city = QuerySelectField('city',validators=[InputRequired()] , query_factory=city_choice , allow_blank= False  , get_label='city')
    contact = StringField('contacts', validators=[InputRequired()])

# CommChannel Model & Form

class CommChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(30), unique=True, nullable=False) 

class CommChannelForm(FlaskForm):
    channel = StringField('channel', validators=[InputRequired()])

# HealthCode Model & Form

class HealthCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.String(5), unique=True, nullable=False)

class HealthCodeForm(FlaskForm):
    health = StringField('health', validators=[InputRequired()])

# ProdCat Model & Form
    
class ProdCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_cat = db.Column(db.String(30), unique=True, nullable=False) 

class ProdCatForm(FlaskForm):
    prod_cat = StringField('prod_cat', validators=[InputRequired()])

# BussCat Model & Form
    
class BussCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buss_cat = db.Column(db.String(30), unique=True, nullable=False) 

class BussCatForm(FlaskForm):
    buss_cat = StringField('buss_cat', validators=[InputRequired()])

# State Model & Form

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(30), unique=True, nullable=False)
    
class StateForm(FlaskForm):
    state = StringField('state', validators=[InputRequired()])

# Country Model & Form
    
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(30), unique=True, nullable=False)

class CountryForm(FlaskForm):
    country = StringField('country', validators=[InputRequired()])

# City Model & Form

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

class CityForm(FlaskForm):
    city = StringField('city', validators=[InputRequired()])
    state = QuerySelectField('state',validators=[InputRequired()] , query_factory=state_choice , allow_blank= False  , get_label='state')
    country = QuerySelectField('country', validators=[InputRequired()], query_factory=country_choice , allow_blank= False ,get_label='country')

# Firm Model & Form
class Firm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firm = db.Column(db.String(30), unique=True, nullable=False)

class FirmForm(FlaskForm):
    firm = StringField('firm', validators=[InputRequired()])

# Group Model & Form
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(30), unique=True, nullable=False)

class GroupForm(FlaskForm):
    group = StringField('group', validators=[InputRequired()])

########################################
####### CONTACT FORMS & DB #############
########################################

class AddContactForm(FlaskForm):
    company_name = StringField('comapany_name' , validators=[InputRequired()])
    company_per = StringField('company_per' , validators=[InputRequired()])    
    contact_one = StringField('contact_one' , validators=[InputRequired()])
    wh_contact = StringField('wh_contact')
    email = StringField('email' , validators=[InputRequired()])
    city = QuerySelectField('city',validators=[InputRequired()] , query_factory=city_choice , allow_blank= False  , get_label='city')
    buss_cat = QuerySelectField('buss_cat',validators=[InputRequired()] , query_factory=buss_choice , allow_blank= False  , get_label='buss_cat')
    broker = QuerySelectField('broker',validators=[InputRequired()] , query_factory=broker_choice , allow_blank= False  , get_label='broker_name')
    comm_channel = QuerySelectField('comm_channel',validators=[InputRequired()] , query_factory=comm_choice , allow_blank= False  , get_label='channel')
    prod_cat = QuerySelectField('prod_cat',validators=[InputRequired()] , query_factory=prod_choice , allow_blank= False  , get_label='prod_cat')
    health_code = QuerySelectField('health_code',validators=[InputRequired()] , query_factory=health_choice , allow_blank= False  , get_label='health')
    pref_comm_channel = QuerySelectField('pref_comm_channel',validators=[InputRequired()] , query_factory=comm_choice , allow_blank= False  , get_label='channel')
    address_one = StringField('address_one' , validators=[InputRequired()])
    address_two = StringField('address_two' )
    address_three = StringField('address_three')
    address_pin = StringField('address_pin' , validators=[InputRequired()])
    group = QuerySelectField('group',validators=[InputRequired()] , query_factory=group_choice , allow_blank= False  , get_label='group')


class AddContact(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(50))
    company_per = db.Column(db.String(50))
    contact_one = db.Column(db.String(20) , nullable = True)
    wh_contact = db.Column(db.String(20) , nullable = True)
    email = db.Column(db.String(50) , unique = True , nullable = True)
    country = db.Column(db.String(30) )
    state = db.Column(db.String(20) )
    city = db.Column(db.String(20) )
    buss_cat = db.Column(db.String(200))
    prod_cat = db.Column(db.String(200))
    broker = db.Column(db.String(20) )
    comm_channel = db.Column(db.String(200) )
    health_code = db.Column(db.String(20) )
    pref_comm_channel = db.Column(db.String(200))
    address_one = db.Column(db.String(100))
    address_two = db.Column(db.String(100))
    address_three = db.Column(db.String(100))
    address_pin = db.Column(db.String(10))
    group = db.Column(db.String(30))


########################################
####### INVOICE DETAIL FORMS & DB ######
########################################

class Invoice(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(50))
    firm = db.Column(db.String(50))
    invoice_no = db.Column(db.String(50))
    amount = db.Column(db.String(15))
    date = db.Column(db.Date)
    
class InvoiceForm(FlaskForm):
    invoice_no = StringField('invoice_no')
    amount = StringField('amount' , validators=[DataRequired() , InputRequired()])
    firm = QuerySelectField('firm' ,  validators=[InputRequired()] , query_factory= firm_choice , allow_blank= False  , get_label='firm')
    company_name = QuerySelectField('company_name', validators=[InputRequired()] , query_factory= contact_choice , allow_blank= False  , get_label='company_name')
    date = StringField('date' , validators=[ Regexp(r'[0-9]{2}[-]{1}[0-9]{2}[-|]{1}[0-9]{4}' , message ="Date format YYYY-MM-DD")  ,  InputRequired() , DataRequired()])

########################################
### COMMUNICATION DETAIL FORMS & DB ####
########################################

class Comm(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    comm_channel = db.Column(db.Integer , db.ForeignKey('comm_channel.id'))
    mssg_detail = db.Column(db.String(100))
    group = db.Column(db.Integer)
    date = db.Column(db.Date)
    comm = db.relationship("CommChannel")
    
class CommForm(FlaskForm):
    comm_channel = SelectField('comm_channel',validators=[InputRequired()] , coerce = int)
    mssg_detail = StringField('mssg_detail', widget= TextArea())
    group = SelectField('group' ,  validators=[InputRequired()] , coerce = int)
    date = StringField('date' , validators=[InputRequired() , DataRequired()])

########################################
####### GROUP ADDITION FORMS & DB ######
########################################

class AddGroupForm(FlaskForm):
    group = SelectField('group' ,coerce =int)
    contact= SelectMultipleField('contact' , coerce=int)

########################################
####### MSSGs FORMS & DB ###############
########################################

class Mssgs(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    type_mssg = db.Column(db.String(20) , nullable =True)
    mssg = db.Column(db.String(500) , nullable = True)

class MssgsForm(FlaskForm):
    type_mssg = SelectField('Communication Type' , coerce =int)
    mssg = StringField('mssg' , widget = TextArea() , validators = [InputRequired() , DataRequired()])

########################################
####### INSIGHTS FILTER FORM ###########
########################################

class FilterForm(FlaskForm):
    date_start = DateField('start_date' ,format = r'%Y-%m-%d')
    date_end = DateField('end_date' ,format = r'%Y-%m-%d')
    buss_cat = SelectMultipleField('buss_cat' , coerce =int)
    prod_cat = SelectMultipleField('prod_cat' , coerce =int)
    city = SelectMultipleField('city' , coerce =int)
    state = SelectMultipleField('state' , coerce =int)
    country = SelectMultipleField('country' , coerce =int)
    broker = SelectMultipleField('broker' , coerce =int)
    health_code = SelectMultipleField('health_code' , coerce = int)
    no_comm = StringField('no_comm')
    comm_channel = SelectMultipleField('buss_cat' , coerce = int)
    no_invoice = StringField('no_invoice')
    amount = StringField('amount')

###### MAPPER #########

