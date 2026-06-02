from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.alerts import AlertForm
from app.models.message import Notification, SearchAlert
from app.models.pet import PetSize, PetSpecies
from app.utils.decorators import adopter_required

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts", methods=["GET", "POST"])
@login_required
@adopter_required
def index():
    form = AlertForm()
    if form.validate_on_submit():
        active_count = SearchAlert.query.filter_by(
            adopter_id=current_user.id, is_active=True
        ).count()
        if active_count >= 3:
            flash(
                "Ya tienes 3 alertas activas. Elimina una antes de crear otra.",
                "danger",
            )
            return redirect(url_for("alerts.index")), 400

        alert = SearchAlert(
            adopter_id=current_user.id,
            species=PetSpecies(form.species.data) if form.species.data else None,
            breed=form.breed.data or None,
            age_max=form.age_max.data,
            size=PetSize(form.size.data) if form.size.data else None,
            children_friendly=True if form.children_friendly.data else None,
            other_animals_friendly=True if form.other_animals_friendly.data else None,
        )
        db.session.add(alert)
        db.session.commit()
        flash("Alerta creada correctamente.", "success")
        return redirect(url_for("alerts.index"))

    alerts_list = (
        SearchAlert.query.filter_by(adopter_id=current_user.id, is_active=True)
        .order_by(SearchAlert.created_at.desc())
        .all()
    )
    return render_template("alerts/index.html", alerts=alerts_list, form=form)


@alerts_bp.route("/alerts/<int:alert_id>/delete", methods=["POST"])
@login_required
@adopter_required
def delete_alert(alert_id):
    alert = SearchAlert.query.get_or_404(alert_id)
    if alert.adopter_id != current_user.id:
        abort(403)
    alert.is_active = False
    db.session.commit()
    flash("Alerta eliminada.", "success")
    return redirect(url_for("alerts.index"))


@alerts_bp.route("/notifications")
@login_required
def notifications():
    notifs = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return render_template("notifications/index.html", notifications=notifs)


@alerts_bp.route("/notifications/mark-read", methods=["POST"])
@login_required
def mark_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update(
        {"is_read": True}
    )
    db.session.commit()
    return redirect(url_for("alerts.notifications"))
