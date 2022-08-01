from app.api import bp


@bp.route("/user_posts/<int:id>")
def user_posts(int: id):
    pass


@bp.route("/followed_posts/<int:id>")
def followed_posts(int: id):
    pass
