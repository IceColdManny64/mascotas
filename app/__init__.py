import os

from flask import Flask, redirect, url_for

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(
        os.path.join(app.root_path, "static", "uploads"),
        exist_ok=True,
    )

    from app.extensions import csrf, db, login_manager, migrate

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.models import (  # noqa: F401
        AdoptionRequest,
        Favorite,
        Message,
        Notification,
        Pet,
        PetPhoto,
        Review,
        SearchAlert,
        User,
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.admin import admin_bp
    from app.routes.adoptions import adoptions_bp
    from app.routes.alerts import alerts_bp
    from app.routes.auth import auth_bp
    from app.routes.messages import messages_bp
    from app.routes.pets import pets_bp
    from app.routes.reviews import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(adoptions_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return redirect(url_for("pets.index"))

    @app.context_processor
    def inject_counts():
        from flask_login import current_user

        from app.models.message import Message, Notification

        notif_count = 0
        msg_count = 0
        if current_user.is_authenticated:
            notif_count = Notification.query.filter_by(
                user_id=current_user.id, is_read=False
            ).count()
            msg_count = Message.query.filter_by(
                receiver_id=current_user.id, is_read=False
            ).count()
        return dict(unread_notifications=notif_count, unread_messages=msg_count)

    return app
