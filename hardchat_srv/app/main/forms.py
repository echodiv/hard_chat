from flask import request
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditProfile(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=128)])
    sename = StringField("Sename", validators=[DataRequired(), Length(min=1, max=128)])
    phone = StringField("Phone number", validators=[Length(min=10, max=12)])
    submit = SubmitField("Edit Profile")


class SetStatus(FlaskForm):
    status = StringField("Status", validators=[Length(min=0, max=256)])
    submit = SubmitField("Ok")


class PostForm(FlaskForm):
    post = TextAreaField(
        "What's new?", validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField("Publush")


class SearchForm(FlaskForm):
    q = StringField(_l("Search"), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "csrf_enabled" not in kwargs:
            kwargs["csrf_enabled"] = False
        super(SearchForm, self).__init__(*args, **kwargs)
