from app.models import Users
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class EditProfile(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=128)])
    sename = StringField('Sename', validators=[DataRequired(), Length(min=1, max=128)])
    phone = StringField('Phone number', validators=[Length(min=10, max=12)])
    submit = SubmitField('Edit Profile')


class SetStatus(FlaskForm):
    status = StringField('Status', validators=[Length(min=0, max=256)])
    submit = SubmitField('Ok')

class PostForm(FlaskForm):
    post = TextAreaField('What\'s new?', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Publush')
