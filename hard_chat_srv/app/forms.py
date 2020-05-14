from app.models import Users
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
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


class EditProfile(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=128)])
    sename = StringField('Sename', validators=[DataRequired(), Length(min=1, max=128)])
    phone = StringField('Phone number', validators=[Length(min=10, max=12)])
    submit = SubmitField('Edit Profile')


class SetStatus(FlaskForm):
    status = StringField('Status', validators=[Length(min=0, max=256)])
    submit = SubmitField('Ok')
