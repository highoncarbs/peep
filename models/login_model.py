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
    pass

class BrokerForm(FlaskForm):
    pass

class CommChannel(db.Model):
    pass 

class CommChannelForm(FlaskForm):
    pass
    
class HealthChannel(db.Model):
    pass 

class HealthChannelForm(FlaskForm):
    pass
    
class ProdCat(db.Model):
    pass 

class ProdCatForm(FlaskForm):
    pass
    
class BussCat(db.Model):
    pass 

class BussCatForm(FlaskForm):
    pass
    
########################################
####### CONTACT FORMS & DB #############
########################################

class AddContact_form(FlaskForm):
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