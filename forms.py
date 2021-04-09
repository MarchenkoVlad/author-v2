from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class AuthForm(FlaskForm):
    #user_id = StringField('user_id', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
   # login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    
