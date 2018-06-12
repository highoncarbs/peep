import os


# WTF config

WTF_CSRF_ENABLED = True
SECRET_KEY = 'the_very_secure_secret_security_key_that_no_will_ever_guess'

# MySQL Config

host = "localhost"
user = "root"
passwrd = ""
db = "PEEPS"

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@127.0.0.1/PEEPS'
SQLALCHEMY_TRACK_MODIFICATIONS = False