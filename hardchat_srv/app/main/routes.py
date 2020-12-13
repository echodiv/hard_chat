from flask import render_template, flash, redirect, url_for, request, g, current_app, jsonify
from flask_babel import _, get_locale
from app import db
from app.main import bp
from app.main.forms import  EditProfile, PostForm, SetStatus, SearchForm
from app.models import Users, Posts
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit_time = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    return redirect("/explore", code=302)

@bp.route('/edit_profile', methods=['POST', 'GET'])
def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.sename = form.sename.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Change have been saved')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.sename.data = current_user.sename
        form.phone.data = current_user.phone
    return render_template('edit_profile.html', title='Edit profile', form=form)

@bp.route('/user/<id>')
@login_required
def user(id):
    user = Users.query.filter_by(id=id).first_or_404()
    return render_template('user.html', user=user)

@bp.route('/user/<id>/popup')
@login_required
def user_popup(id):
    user = Users.query.filter_by(id=id).first_or_404()
    return render_template('user_popup.html', user=user)

@bp.route("/send")
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

    current_app.logger.info(username)
    current_app.logger.info(text)

    # TODO ave message

    return {"ok": True} # hahaha =)

@bp.route("/get_messages")
@login_required
def get_messages():
    """
    :return: {"messages": ["username": str, "time": str, "text": str]}
    """
    return str('{"messages": MESSAGES}')

@bp.route("/follow/<user_id>")
@login_required
def follow(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        flash("User with id {} not found".format(user_id))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash("You can not follow yourself")
        return redirect(url_for('main.index'))
    current_user.follow(user)
    db.session.commit()
    flash("now youre following {}!".format(user.name))
    return redirect(url_for('main.user', id=user_id))

@bp.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        flash('User {} not found.'.format(user_id))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', id=user_id))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(user.name))
    return redirect(url_for('main.user', id=user_id))

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Post published'))
        return redirect(url_for('main.index'))
    # todo: move to separate function
    return render_template('index.html', title='Explore', form=form)

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Posts.search(g.search_form.q.data, page,
                               current_app.config['POST_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POST_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/user_posts/<int:id>')
def user_posts(id):
    user = Users.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)

    return jsonify(Users.to_collection_dict(user.posts, 
        page, current_app.config['POST_PER_PAGE']))

@bp.route('/followed_posts')
def followed_posts():
    page = request.args.get('page', 1, type=int)
    return jsonify(Users.to_collection_dict(current_user.followed_posts(), 
        page, current_app.config['POST_PER_PAGE']))


