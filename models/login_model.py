from wtforms import StringField, PasswordField , BooleanField
from wtforms.validators import InputRequired, Email, Length , DataRequired
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from app import db

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