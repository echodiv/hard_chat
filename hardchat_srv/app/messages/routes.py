from datetime import datetime

from app import db
from app.messages import bp
from app.messages.forms import MessageForm
from app.models import Messages, Users
from flask import (current_app, flash, g, redirect, render_template, request,
                   url_for)
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from sqlalchemy import and_, or_


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visit_time = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route("/send/<int:recipient_id>", methods=["POST"])
@login_required
def send(recipient_id):
    user = Users.query.filter_by(id=recipient_id).first_or_404()
    form = MessageForm()

    if form.validate_on_submit():
        msg = Messages(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(_("Your message has been sent."))

        return redirect(url_for("messages.read", dialog=recipient_id))

    redirect(url_for("messages.read"))


@bp.route("/read")
@login_required
def read():
    dialog_id = request.args.get("dialog", None, type=int)
    if dialog_id is not None:
        page = request.args.get("page", 1, type=int)
        messages = (
            Messages.query.filter(
                or_(
                    and_(
                        Messages.sender_id == current_user.id,
                        Messages.recipient_id == dialog_id,
                    ),
                    and_(
                        Messages.sender_id == dialog_id,
                        Messages.recipient_id == current_user.id,
                    ),
                )
            )
            .order_by(Messages.timestamp.desc())
            .paginate(page, current_app.config["MSG_PER_PAGE"], False)
        )
        next_url = (
            url_for("messages.read", dialog=dialog_id, page=messages.next_num)
            if messages.has_next
            else None
        )
        prev_url = (
            url_for("messages.read", dialog=dialog_id, page=messages.prev_num)
            if messages.has_prev
            else None
        )

        send_message_form = MessageForm()
        return render_template(
            "messages.html",
            messages=messages.items,
            recipient_id=dialog_id,
            form=send_message_form,
            next_url=next_url,
            prev_url=prev_url,
        )

    page = request.args.get("page", 1, type=int)
    messages = (
        current_user.messages_received.order_by(Messages.timestamp.desc())
        .group_by("sender_id")
        .paginate(page, current_app.config["POST_PER_PAGE"], False)
    )

    next_url = (
        url_for("messages.read", page=messages.next_num) if messages.has_next else None
    )
    prev_url = (
        url_for("messages.read", page=messages.prev_num) if messages.has_prev else None
    )

    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    return render_template(
        "messages.html", messages=messages.items, next_url=next_url, prev_url=prev_url
    )
