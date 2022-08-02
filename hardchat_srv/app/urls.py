from flask import Flask


def register_routers(app: Flask) -> None:

    from app.auth.routes import (
        login,
        logout,
        register,
        reset_password,
        reset_password_request,
    )
    from app.messages.routes import read, send
    from app.main.routes import (
        index,
        edit_profile,
        user,
        user_popup,
        follow,
        unfollow,
        explore,
        search,
        user_posts,
        followed_posts,
    )

    app.add_url_rule(
        "/auth/reset_password/<token>",
        "auth.reset_password",
        reset_password,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/auth/reset_password_request",
        "auth.reset_password_request",
        reset_password_request,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/auth/register", "auth.register", register, methods=["GET", "POST"]
    )
    app.add_url_rule("/auth/logout", "auth.logout", logout)
    app.add_url_rule(
        "/auth/login", "auth.login", login, methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/messages/send/<int:recipient_id>",
        "messages.send",
        send,
        methods=["POST"],
    )
    app.add_url_rule("/messages/read", "messages.read", read)

    app.add_url_rule("/search", "main.search", search)
    app.add_url_rule("/followed_posts", "main.followed_posts", followed_posts)
    app.add_url_rule("/user_posts/<int:id>", "main.user_posts", user_posts)
    app.add_url_rule(
        "/explore", "main.explore", explore, methods=["GET", "POST"]
    )
    app.add_url_rule("/unfollow/<int:user_id>", "main.unfollow", unfollow)
    app.add_url_rule("/follow/<user_id>", "main.follow", follow)
    app.add_url_rule("/user/<id>/popup", "main.user_popup", user_popup)
    app.add_url_rule("/user/<id>", "main.user", user)
    app.add_url_rule(
        "/edit_profile",
        "main.edit_profile",
        edit_profile,
        methods=["POST", "GET"],
    )
    app.add_url_rule("/", "main.index", index)


def register_error_handlers(app: Flask) -> None:

    from app.errors.handlers import not_found_error, internal_error

    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
