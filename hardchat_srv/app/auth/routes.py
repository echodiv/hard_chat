from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from app.models import Users

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_babel import lazy_gettext as _l
from werkzeug.urls import url_parse


@bp.route("/login", methods=["GET", "POST"])
def login():
    ERROR_INVALID_USER = _l("Invalid user or password")
    PAGE_TITLE = _l("Sing In")

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(ERROR_INVALID_USER)
            return redirect(url_for("auth.login"))

        login_user(user, form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("auth/login.html", title=PAGE_TITLE, form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("main.index"))


@bp.route("/register", methods=["POST", "GET"])
def register():
    PAGE_TITLE = _l("Register")
    SUCCESS_REGISTRATION_TEXT = _l("Congratulation! Youre register with email")

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users(
            name=form.name.data, sename=form.sename.data, email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"{SUCCESS_REGISTRATION_TEXT} {form.email.data}")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title=PAGE_TITLE, form=form)


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    EMAIL_RESET_TEXT = _l(
        "Check your email for the instructions to reset your password"
    )
    PAGE_TITLE = _l("Reset Password")

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)

        flash(TEXT_EMAIL_RESET)
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password_request.html", title=PAGE_TITLE, form=form
    )


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    SUCCESS_PASSWORD_RESET_TEXT = _l("Your password has been reset.")

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = Users.verify_reset_password_token(token)

    if not user:
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(SUCCESS_PASSWORD_RESET_TEXT)
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)
