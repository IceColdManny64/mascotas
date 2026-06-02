from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.forms.reviews import ReportReviewForm, ReviewForm
from app.models.adoption import AdoptionRequest, AdoptionStatus
from app.models.pet import Pet
from app.models.review import Review
from app.models.user import User, UserRole
from app.utils.decorators import adopter_required
from app.utils.notifications import shelter_average_rating

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/shelters/<int:shelter_id>")
def shelter_profile(shelter_id):
    shelter = User.query.get_or_404(shelter_id)
    if shelter.role != UserRole.shelter:
        abort(404)

    page = request.args.get("page", 1, type=int)
    pets = (
        Pet.query.filter_by(shelter_id=shelter.id, is_active=True)
        .order_by(Pet.created_at.desc())
        .paginate(page=page, per_page=6, error_out=False)
    )

    reviews = (
        Review.query.filter_by(shelter_id=shelter.id, is_reported=False)
        .order_by(Review.created_at.desc())
        .all()
    )
    avg_rating, total_reviews = shelter_average_rating(shelter.id)

    can_review = False
    form = None
    if current_user.is_authenticated and current_user.role == UserRole.adopter:
        has_approved = (
            AdoptionRequest.query.join(Pet)
            .filter(
                AdoptionRequest.adopter_id == current_user.id,
                AdoptionRequest.status == AdoptionStatus.approved,
                Pet.shelter_id == shelter.id,
            )
            .first()
        )
        existing_review = Review.query.filter_by(
            reviewer_id=current_user.id, shelter_id=shelter.id
        ).first()
        if has_approved and not existing_review:
            can_review = True
            form = ReviewForm()

    return render_template(
        "reviews/shelter_profile.html",
        shelter=shelter,
        pets=pets,
        reviews=reviews,
        avg_rating=avg_rating,
        total_reviews=total_reviews,
        can_review=can_review,
        form=form,
    )


@reviews_bp.route("/shelters/<int:shelter_id>/review", methods=["POST"])
@login_required
@adopter_required
def create_review(shelter_id):
    shelter = User.query.get_or_404(shelter_id)
    if shelter.role != UserRole.shelter:
        abort(404)

    existing = Review.query.filter_by(
        reviewer_id=current_user.id, shelter_id=shelter.id
    ).first()
    if existing:
        flash("Ya valoraste a este refugio.", "danger")
        return redirect(url_for("reviews.shelter_profile", shelter_id=shelter_id)), 400

    approved = (
        AdoptionRequest.query.join(Pet)
        .filter(
            AdoptionRequest.adopter_id == current_user.id,
            AdoptionRequest.status == AdoptionStatus.approved,
            Pet.shelter_id == shelter.id,
        )
        .first()
    )
    if not approved:
        abort(403)

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            shelter_id=shelter.id,
            reviewer_id=current_user.id,
            adoption_request_id=approved.id,
            rating=form.rating.data,
            comment=form.comment.data or None,
        )
        db.session.add(review)
        db.session.commit()
        flash("Valoración enviada. ¡Gracias!", "success")
        return redirect(url_for("reviews.shelter_profile", shelter_id=shelter_id))
    flash("Revisa los datos del formulario.", "danger")
    return redirect(url_for("reviews.shelter_profile", shelter_id=shelter_id)), 400


@reviews_bp.route("/reviews/<int:review_id>/report", methods=["POST"])
@login_required
def report_review(review_id):
    review = Review.query.get_or_404(review_id)
    form = ReportReviewForm()
    if form.validate_on_submit():
        review.is_reported = True
        review.reported_reason = form.reason.data
        db.session.commit()
        flash("Reportado para revisión", "success")
    return redirect(url_for("reviews.shelter_profile", shelter_id=review.shelter_id))
