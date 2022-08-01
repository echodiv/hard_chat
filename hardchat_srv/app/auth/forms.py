from app.models import Users
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    """Authentication form"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class ResetPasswordForm(FlaskForm):
    """Form for regain access to the system"""

    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")


class ResetPasswordRequestForm(FlaskForm):
    """After resetting the password, you need to set a new one"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    sename = StringField("Sename")
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    password2 = StringField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    phone = StringField("Phone Number")
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError("Please use a different email address")
