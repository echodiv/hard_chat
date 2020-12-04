from app.models import Users
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign In') 

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sename = StringField('Sename')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone Number')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

