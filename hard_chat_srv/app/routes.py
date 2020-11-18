from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfile
from app.models import Users
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit_time = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [{'author': {'username': 'John'},'body': 'Beautiful day in Portland!'},{'author': {'username': 'Susan'},'body': 'The Avengers movie was so cool!'}] 
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sing In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users(name=form.name.data,
                sename=form.sename.data,
                email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulation! Youre register with email {form.email.data}')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/edit_profile', methods=['POST', 'GET'])
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.sename = form.sename.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Change have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.sename.data = current_user.sename
        form.phone.data = current_user.phone
    return render_template('edit_profile.html', title='Edit profile', form=form)

@app.route('/user/<id>')
@login_required
def user(id):
    user = Users.query.filter_by(id=id).first_or_404()
    posts = [
            {'author': user, 'body': 'test'},
            {'author': user, 'body': 'test 2' }
            ]
    return render_template('user.html', user=user, posts=posts)


@app.route("/send")
def send_mesage():
    """
    :param json: {"username":str,"text":str}
    :return: {"ok":bool}
    """
    username = request.json["username"]
    text = request.json["text"]
    if not isinstance(username, str) or len(username) == 0:
        return {"ok": False}
    if not isinstance(text, str) or len(text) == 0:
        return {"ok": False}

    app.logger.info(username)
    app.logger.info(text)

    # TODO ave message
    MESSAGES.append({"username": username, "time": time.time(), "text": text})

    return {"ok": True}

@app.route("/get_messages")
@login_required
def get_messages():
    """
    :return: {"messages": ["username": str, "time": str, "text": str]}
    """
    return str('{"messages": MESSAGES}')

@app.route("/follow/<user_id>")
@login_required
def follow(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        flash("User with id {} not found".format(user_id))
        return redirect(url_for('index'))
    if user == current_user:
        flash("You can not follow yourself")
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash("now youre following {}!".format(user.name))
    return redirect(url_for('user', id=user_id))

@app.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        flash('User {} not found.'.format(user_id))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', id=user_id))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(user.name))
    return redirect(url_for('user', id=user_id))


