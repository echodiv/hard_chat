from app import db
from app.main.forms import EditProfile, PostForm
from app.models import Posts, Users
from flask import (
    current_app,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import lazy_gettext as _l
from flask_login import current_user, login_required


@login_required
def index():
    return redirect("/explore", code=302)


def edit_profile():
    form = EditProfile()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.sename = form.sename.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Change have been saved")
        return redirect(url_for("main.user", id=current_user.id))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.sename.data = current_user.sename
        form.phone.data = current_user.phone

    return render_template(
        "edit_profile.html", title="Edit profile", form=form
    )


@login_required
def user(id):
    user = Users.query.filter_by(id=id).first_or_404()

    return render_template("user.html", user=user)


@login_required
def user_popup(id):
    user = Users.query.filter_by(id=id).first_or_404()

    return render_template("user_popup.html", user=user)


@login_required
def follow(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if user is None:
        flash("User with id {} not found".format(user_id))
        return redirect(url_for("main.index"))

    if user == current_user:
        flash("You can not follow yourself")
        return redirect(url_for("main.index"))

    current_user.follow(user)
    db.session.commit()
    flash("now youre following {}!".format(user.name))

    return redirect(url_for("main.user", id=user_id))


@login_required
def unfollow(user_id):
    FOLLOW_YOURSELF_ERROR = _l("You cannot unfollow yourself!")
    UNFOLLOW_TEXT = _l("You are not following")
    USER_NOT_FOUND_TEXT = _l("User {} not found.")

    user = Users.query.filter_by(id=user_id).first()

    if user is None:
        flash(USER_NOT_FOUND_TEXT.format(user_id))
        return redirect(url_for("main.index"))

    if user == current_user:
        flash(FOLLOW_YOURSELF_ERROR)
        return redirect(url_for("main.user", id=user_id))

    current_user.unfollow(user)
    db.session.commit()
    flash(f"{UNFOLLOW_TEXT} {user.name}.")

    return redirect(url_for("main.user", id=user_id))


@login_required
def explore():
    # TODO: page = request.args.get('page', 1, type=int)
    PAGE_TITLE = _l("Explore")
    POSTED_TEXT = _l("Post published")

    form = PostForm()

    if form.validate_on_submit():
        post = Posts(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(POSTED_TEXT)
        return redirect(url_for("main.index"))

    return render_template("index.html", title=PAGE_TITLE, form=form)


@login_required
def search():
    PAGE_TITLE = _l("Search")

    if not g.search_form.validate():
        return redirect(url_for("main.explore"))

    page = request.args.get("page", 1, type=int)
    posts, total = Posts.search(
        g.search_form.q.data, page, current_app.config["POST_PER_PAGE"]
    )
    next_url = (
        url_for("main.search", q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config["POST_PER_PAGE"]
        else None
    )
    prev_url = (
        url_for("main.search", q=g.search_form.q.data, page=page - 1)
        if page > 1
        else None
    )

    return render_template(
        "search.html",
        title=PAGE_TITLE,
        posts=posts,
        next_url=next_url,
        prev_url=prev_url,
    )


def user_posts(id):
    user = Users.query.filter_by(id=id).first_or_404()
    page = request.args.get("page", 1, type=int)

    return jsonify(
        Users.to_collection_dict(
            user.posts, page, current_app.config["POST_PER_PAGE"]
        )
    )


def followed_posts():
    page = request.args.get("page", 1, type=int)

    return jsonify(
        Users.to_collection_dict(
            current_user.followed_posts(),
            page,
            current_app.config["POST_PER_PAGE"],
        )
    )
