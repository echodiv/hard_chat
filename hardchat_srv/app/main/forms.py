from flask import request
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditProfile(FlaskForm):
    LABELS = {
        "name": _l("Name"),
        "phone": _l("Phone number"),
        "sename": _l("Sename"),
        "button": _l("Edit profile"),
    }
    name = StringField(
        LABELS["name"], validators=[DataRequired(), Length(min=1, max=128)]
    )
    sename = StringField(
        LABELS["sename"], validators=[DataRequired(), Length(min=1, max=128)]
    )
    phone = StringField(LABELS["phone"], validators=[Length(min=10, max=12)])
    submit = SubmitField(LABELS["phone"])


class SetStatus(FlaskForm):
    LABELS = {
        "status": _l("Status"),
        "button": _l("OK"),
    }
    status = StringField(LABELS["status"], validators=[Length(min=0, max=256)])
    submit = SubmitField(LABELS["button"])


class PostForm(FlaskForm):
    LABELS = {
        "post": _l("What's new?"),
        "button": _l("Publush"),
    }
    post = TextAreaField(
        LABELS["post"], validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField(LABELS["button"])


class SearchForm(FlaskForm):
    q = StringField(_l("Search"), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "csrf_enabled" not in kwargs:
            kwargs["csrf_enabled"] = False
        super(SearchForm, self).__init__(*args, **kwargs)
