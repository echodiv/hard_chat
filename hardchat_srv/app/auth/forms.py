from app.models import Users
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    """Authentication form"""

    TITLES = {
        "email": _l("Email"),
        "password": _l("Password"),
        "remember": _l("Remember Me"),
        "sing_in": _l("Sign In"),
    }

    email = StringField(TITLES["email"], validators=[DataRequired(), Email()])
    password = PasswordField(TITLES["password"], validators=[DataRequired()])
    remember_me = BooleanField(TITLES["remember"])
    submit = SubmitField(TITLES["sing_in"])


class ResetPasswordForm(FlaskForm):
    """Form for regain access to the system"""

    TITLES = {
        "password": _l("Password"),
        "repeat_password": _l("Repeat Password"),
        "button": _l("Request Password Reset"),
    }

    password = PasswordField(TITLES["password"], validators=[DataRequired()])
    password2 = PasswordField(
        TITLES["repeat_password"], validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(TITLES["button"])


class ResetPasswordRequestForm(FlaskForm):
    """After resetting the password, you need to set a new one"""

    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Sign In"))


class RegistrationForm(FlaskForm):
    TITLES = {
        "name": _l("Name"),
        "email": _l("Email"),
        "phone": _l("Phone Number"),
        "button": _l("Register"),
        "sername": _l("Sername"),
        "password": _l("Password"),
        "password2": _l("Repeat Password"),
    }
    VALIDATION_ERROR_TEXT = _l("Please use a different email address")

    name = StringField(TITLES["name"], validators=[DataRequired()])
    sename = StringField(TITLES["sername"])
    email = StringField(TITLES["email"], validators=[DataRequired(), Email()])
    password = StringField(TITLES["password"], validators=[DataRequired()])
    password2 = StringField(
        TITLES["password2"], validators=[DataRequired(), EqualTo("password")]
    )
    phone = StringField(TITLES["phone"])
    submit = SubmitField(TITLES["button"])

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(VALIDATION_ERROR_TEXT)
