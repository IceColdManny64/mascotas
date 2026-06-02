from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, func, or_

from app.extensions import db
from app.forms.messages import MessageForm
from app.models.message import Message, NotificationType
from app.models.user import User
from app.utils.notifications import create_notification

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages")
@login_required
def inbox():
    sent = db.session.query(
        Message.receiver_id.label("other_id"),
        func.max(Message.created_at).label("last_at"),
    ).filter(Message.sender_id == current_user.id).group_by(Message.receiver_id)

    received = db.session.query(
        Message.sender_id.label("other_id"),
        func.max(Message.created_at).label("last_at"),
    ).filter(Message.receiver_id == current_user.id).group_by(Message.sender_id)

    conv_map = {}
    for row in sent.all() + received.all():
        oid = row.other_id
        if oid not in conv_map or row.last_at > conv_map[oid]:
            conv_map[oid] = row.last_at

    conversations = []
    for other_id, last_at in sorted(conv_map.items(), key=lambda x: x[1], reverse=True):
        other = User.query.get(other_id)
        if not other:
            continue
        last_msg = (
            Message.query.filter(
                or_(
                    and_(
                        Message.sender_id == current_user.id,
                        Message.receiver_id == other_id,
                    ),
                    and_(
                        Message.sender_id == other_id,
                        Message.receiver_id == current_user.id,
                    ),
                )
            )
            .order_by(Message.created_at.desc())
            .first()
        )
        unread = Message.query.filter_by(
            sender_id=other_id, receiver_id=current_user.id, is_read=False
        ).count()
        preview = (last_msg.content[:60] + "…") if last_msg and len(last_msg.content) > 60 else (last_msg.content if last_msg else "")
        conversations.append(
            {
                "other": other,
                "preview": preview,
                "last_at": last_at,
                "unread": unread,
            }
        )
    return render_template("messages/inbox.html", conversations=conversations)


@messages_bp.route("/messages/<int:user_id>", methods=["GET", "POST"])
@login_required
def conversation(user_id):
    other = User.query.get_or_404(user_id)
    if other.id == current_user.id:
        abort(400)

    Message.query.filter_by(
        sender_id=user_id, receiver_id=current_user.id, is_read=False
    ).update({"is_read": True})
    db.session.commit()

    messages = (
        Message.query.filter(
            or_(
                and_(
                    Message.sender_id == current_user.id,
                    Message.receiver_id == user_id,
                ),
                and_(
                    Message.sender_id == user_id,
                    Message.receiver_id == current_user.id,
                ),
            )
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    form = MessageForm()
    form.pet_id.data = request.args.get("pet_id", type=int)

    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            content=form.content.data,
            pet_id=form.pet_id.data or request.args.get("pet_id", type=int),
        )
        db.session.add(msg)
        create_notification(
            user_id,
            NotificationType.new_message,
            f"Nuevo mensaje de {current_user.name}",
            f"/messages/{current_user.id}",
        )
        db.session.commit()
        return redirect(url_for("messages.conversation", user_id=user_id))

    return render_template(
        "messages/conversation.html",
        other=other,
        messages=messages,
        form=form,
    )
