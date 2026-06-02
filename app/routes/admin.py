from datetime import datetime, timedelta, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.models.adoption import AdoptionRequest, AdoptionStatus
from app.models.pet import Pet, PetStatus
from app.models.review import Review
from app.models.user import User, UserRole
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
@admin_required
def dashboard():
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    metrics = {
        "total_pets": Pet.query.count(),
        "available_pets": Pet.query.filter_by(
            status=PetStatus.available, is_active=True
        ).count(),
        "adopted_pets": Pet.query.filter_by(status=PetStatus.adopted).count(),
        "total_users_adopter": User.query.filter_by(role=UserRole.adopter).count(),
        "total_users_shelter": User.query.filter_by(role=UserRole.shelter).count(),
        "pending_requests": AdoptionRequest.query.filter_by(
            status=AdoptionStatus.pending
        ).count(),
        "new_pets_30d": Pet.query.filter(Pet.created_at >= thirty_days_ago).count(),
        "new_users_30d": User.query.filter(User.created_at >= thirty_days_ago).count(),
    }
    return render_template("admin/dashboard.html", metrics=metrics)


@admin_bp.route("/admin/pets")
@login_required
@admin_required
def pets():
    status = request.args.get("status")
    is_active = request.args.get("is_active")
    query = Pet.query.order_by(Pet.created_at.desc())
    if status in ("available", "pending", "adopted"):
        query = query.filter(Pet.status == PetStatus(status))
    if is_active == "true":
        query = query.filter(Pet.is_active.is_(True))
    elif is_active == "false":
        query = query.filter(Pet.is_active.is_(False))
    page = request.args.get("page", 1, type=int)
    pagination = query.paginate(page=page, per_page=20, error_out=False)
    return render_template("admin/pets.html", pagination=pagination)


@admin_bp.route("/admin/pets/<int:pet_id>/deactivate", methods=["POST"])
@login_required
@admin_required
def deactivate_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    pet.is_active = False
    db.session.commit()
    flash("Mascota desactivada.", "success")
    return redirect(url_for("admin.pets"))


@admin_bp.route("/admin/pets/<int:pet_id>/activate", methods=["POST"])
@login_required
@admin_required
def activate_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    pet.is_active = True
    db.session.commit()
    flash("Mascota activada.", "success")
    return redirect(url_for("admin.pets"))


@admin_bp.route("/admin/users")
@login_required
@admin_required
def users():
    page = request.args.get("page", 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("admin/users.html", pagination=pagination)


@admin_bp.route("/admin/users/<int:user_id>/suspend", methods=["POST"])
@login_required
@admin_required
def suspend_user(user_id):
    if user_id == current_user.id:
        flash("No puedes suspenderte a ti mismo.", "danger")
        return redirect(url_for("admin.users")), 400
    user = User.query.get_or_404(user_id)
    user.is_suspended = True
    user.suspended_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Usuario suspendido.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/admin/users/<int:user_id>/unsuspend", methods=["POST"])
@login_required
@admin_required
def unsuspend_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_suspended = False
    user.suspended_at = None
    db.session.commit()
    flash("Usuario reactivado.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/admin/reviews")
@login_required
@admin_required
def reported_reviews():
    reviews = (
        Review.query.filter_by(is_reported=True)
        .order_by(Review.created_at.desc())
        .all()
    )
    return render_template("admin/reviews.html", reviews=reviews)


@admin_bp.route("/admin/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash("Valoración eliminada.", "success")
    return redirect(url_for("admin.reported_reviews"))
