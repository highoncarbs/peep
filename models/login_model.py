from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length , DataRequired
from flask_login import UserMixin

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


class SignupForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(
        message="Invalid Email"), Length(max=50)])

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)