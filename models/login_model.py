from wtforms import StringField, PasswordField , BooleanField , DateField
from wtforms.widgets import TextArea , TableWidget, CheckboxInput
from wtforms_alchemy.fields import QuerySelectField ,SelectMultipleField ,SelectField
from wtforms.validators import InputRequired, Email, Length , DataRequired ,Regexp , Optional
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from app import db
import datetime
########################################
#########  BASE FORMS ##################
########################################
class ChoiceObj(object):
    def __init__(self, name, choices):
        # this is needed so that BaseForm.process will accept the object for the named form,
        # and eventually it will end up in SelectMultipleField.process_data and get assigned
        # to .data
        setattr(self, name, choices)

class MultiCheckboxField(SelectMultipleField):
	widget			= TableWidget()
	option_widget	= CheckboxInput()

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
    broker_name = db.Column(db.String(30), nullable=False)
    contact =  db.Column(db.String(30), nullable=False)
    city = db.relationship('City' , secondary='broker_city' , backref='broker' , lazy = 'dynamic')


class BrokerForm(FlaskForm):
    broker_name = StringField('broker_name', validators=[InputRequired()])
    city = QuerySelectField('city',validators=[InputRequired()] , query_factory=city_choice , allow_blank= False  , get_label='city')
    contact = StringField('contacts', validators=[InputRequired()])

db.Table('broker_city',
    db.Column('broker_id' , db.Integer , db.ForeignKey('broker.id')),
    db.Column('city_id' , db.Integer , db.ForeignKey('city.id'))
    )

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
    group = QuerySelectField('group',validators=[Optional(),] , query_factory=group_choice , allow_blank= False  , get_label='group')

class AddContact(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(50))
    company_per = db.Column(db.String(50))
    contact_one = db.Column(db.String(20) , nullable = True)
    wh_contact = db.Column(db.String(20) , nullable = True)
    email = db.Column(db.String(50) , unique = True , nullable = True)
    address_one = db.Column(db.String(100))
    address_two = db.Column(db.String(100))
    address_three = db.Column(db.String(100))
    address_pin = db.Column(db.String(10))
    
    city = db.relationship('City' ,cascade="all,delete", secondary='contact_city' , backref='contact_city' , lazy = 'joined')
    buss_cat = db.relationship('BussCat' , cascade="all,delete",secondary='contact_buss' , backref='contact_buss' , lazy = 'joined')
    prod_cat = db.relationship('ProdCat' , cascade="all,delete",secondary='contact_prod' , backref='contact_prod' , lazy = 'joined')
    broker = db.relationship('Broker' ,cascade="all,delete", secondary='contact_broker' , backref='contact_broker' , lazy = 'joined')
    comm_channel = db.relationship('CommChannel' ,cascade="all,delete", secondary='contact_comm_a' , backref='contact_comm_a' , lazy = 'joined')
    health_code = db.relationship('HealthCode' , cascade="all,delete",secondary='contact_health' , backref='contact_health' , lazy = 'joined')
    pref_comm_channel = db.relationship('CommChannel' , cascade="all,delete",secondary='contact_comm_b' , backref='contact_comm_b' , lazy = 'joined')
    group = db.relationship('Group' , secondary='contact_group' ,cascade="all,delete", backref='contact_group' , lazy = 'joined')
    invoice = db.relationship('Invoice' , cascade="all,delete", backref='contact_invoice' , lazy = 'joined')

db.Table('contact_comm_a',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' , ondelete='SET NULL' )),
    db.Column('channel_id' , db.Integer , db.ForeignKey('comm_channel.id' , ondelete='SET NULL'))
)

db.Table('contact_comm_b',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' ,ondelete='SET NULL')),
    db.Column('channel_id' , db.Integer , db.ForeignKey('comm_channel.id' , ondelete='SET NULL'))
)

db.Table('contact_city',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' , ondelete='SET NULL')),
    db.Column('city_id' , db.Integer , db.ForeignKey('city.id' , ondelete='SET NULL'))
    )

db.Table('contact_buss',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' , ondelete='SET NULL')),
    db.Column('buss_id' , db.Integer , db.ForeignKey('buss_cat.id' , ondelete='SET NULL'))
    )

db.Table('contact_prod',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' , ondelete='SET NULL')),
    db.Column('prod_id' , db.Integer , db.ForeignKey('prod_cat.id' ,ondelete='SET NULL'))
    )

db.Table('contact_broker',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' ,ondelete='SET NULL')),
    db.Column('broker_id' , db.Integer , db.ForeignKey('broker.id' ,ondelete='SET NULL'))
    )

db.Table('contact_health',
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' ,ondelete='SET NULL')),
    db.Column('health_id' , db.Integer , db.ForeignKey('health_code.id' , ondelete='SET NULL'))
    )

db.Table('contact_group', 
    db.Column('contact_id' , db.Integer , db.ForeignKey('add_contact.id' ,ondelete='SET NULL')),
    db.Column('group_id' , db.Integer , db.ForeignKey('group.id' , ondelete='SET NULL'))
)


########################################
####### INVOICE DETAIL FORMS & DB ######
########################################

class Invoice(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    invoice_no = db.Column(db.Integer)
    firm = db.relationship('Firm', cascade="all,delete", secondary='invoice_firm' , backref='invoice' , lazy = 'dynamic')
    contact = db.Column(db.Integer, db.ForeignKey('add_contact.id'))


class InvoiceForm(FlaskForm):
    invoice_no = StringField('invoice_no')
    amount = StringField('amount' , validators=[DataRequired() , InputRequired()])
    firm = QuerySelectField('firm' ,  validators=[InputRequired()] , query_factory= firm_choice , allow_blank= False  , get_label='firm')
    company_name = QuerySelectField('company_name', validators=[InputRequired()] , query_factory= contact_choice , allow_blank= False  , get_label='company_name')
    date = StringField('date' , validators=[ Regexp(r'[0-9]{2}[-]{1}[0-9]{2}[-|]{1}[0-9]{4}' , message ="Date format YYYY-MM-DD")  ,  InputRequired() , DataRequired()])

db.Table('invoice_firm',
    db.Column('invoice_id' , db.Integer , db.ForeignKey('invoice.id' , ondelete='SET NULL')),
    db.Column('firm_id' , db.Integer , db.ForeignKey('firm.id' , ondelete='SET NULL'))
    )
########################################
### COMMUNICATION DETAIL FORMS & DB ####
########################################

class Comm(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    comm_channel = db.Column(db.Integer, db.ForeignKey('comm_channel.id'))
    mssg_detail = db.Column(db.String(100))
    group = db.relationship('Group' , secondary='commu_group' ,cascade="all,delete", backref='commu_group' , lazy = 'joined')
    date = db.Column(db.Date)
    
db.Table('commu_group',
    db.Column('group_id' , db.Integer , db.ForeignKey('group.id' , ondelete='SET NULL')),
    db.Column('commu_id' , db.Integer , db.ForeignKey('comm.id', ondelete='SET NULL'))
    )
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
    date_start = DateField('start_date' ,format = r'%Y-%m-%d' ,validators=[Optional(),])
    date_end = DateField('end_date' ,format = r'%Y-%m-%d' , validators=[Optional(),])
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

class FilterSaveForm(FlaskForm):
    name = StringField('name')

class FilterSave(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    report_name = db.Column(db.String(50))
    query = db.Column(db.String(5000))    
###### MAPPER #########

