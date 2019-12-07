from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max = 10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    phone_number = StringField('Phone', validators=[DataRequired(), Length(max = 10)])
    submit = SubmitField ('Sign Up!')

class LoginFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max = 10)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField ('Login')