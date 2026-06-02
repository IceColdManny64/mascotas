from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from app.extensions import db
from app.forms.adoptions import AdoptionForm
from app.models.adoption import AdoptionRequest, AdoptionStatus, Favorite, HomeType
from app.models.message import Message, NotificationType
from app.models.pet import Pet, PetStatus
from app.utils.decorators import adopter_required, shelter_required
from app.utils.notifications import create_notification

adoptions_bp = Blueprint("adoptions", __name__)


@adoptions_bp.route("/pets/<int:pet_id>/apply", methods=["GET", "POST"])
@login_required
@adopter_required
def apply(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.status != PetStatus.available:
        flash("Esta mascota no está disponible para adopción.", "warning")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    existing = AdoptionRequest.query.filter_by(
        pet_id=pet.id, adopter_id=current_user.id
    ).first()
    if existing:
        flash("Ya enviaste una solicitud para esta mascota.", "info")
        return redirect(url_for("pets.detail", pet_id=pet.id))

    form = AdoptionForm()
    if form.validate_on_submit():
        req = AdoptionRequest(
            pet_id=pet.id,
            adopter_id=current_user.id,
            status=AdoptionStatus.pending,
            home_type=HomeType(form.home_type.data),
            has_yard=form.has_yard.data,
            other_pets=form.other_pets.data,
            other_pets_desc=form.other_pets_desc.data or None,
            has_children=form.has_children.data,
            children_ages=form.children_ages.data or None,
            experience=form.experience.data,
            motivation=form.motivation.data,
        )
        db.session.add(req)
        db.session.commit()
        flash("Solicitud enviada", "success")
        return redirect(url_for("adoptions.my_requests"))
    return render_template("adoptions/apply.html", form=form, pet=pet)


@adoptions_bp.route("/adoptions/my")
@login_required
@adopter_required
def my_requests():
    requests = (
        AdoptionRequest.query.filter_by(adopter_id=current_user.id)
        .order_by(AdoptionRequest.created_at.desc())
        .all()
    )
    return render_template("adoptions/my.html", requests=requests)


@adoptions_bp.route("/adoptions/favorites")
@login_required
@adopter_required
def favorites():
    favs = (
        Favorite.query.filter_by(adopter_id=current_user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    return render_template("adoptions/favorites.html", favorites=favs)


@adoptions_bp.route("/shelter/requests")
@login_required
@shelter_required
def shelter_requests():
    status_filter = request.args.get("status")
    query = (
        AdoptionRequest.query.join(Pet)
        .filter(Pet.shelter_id == current_user.id)
        .order_by(AdoptionRequest.created_at.desc())
    )
    if status_filter in ("pending", "approved", "rejected"):
        query = query.filter(
            AdoptionRequest.status == AdoptionStatus(status_filter)
        )
    requests_list = query.all()
    return render_template(
        "adoptions/shelter_list.html",
        requests=requests_list,
        status_filter=status_filter,
    )


@adoptions_bp.route("/shelter/requests/<int:req_id>")
@login_required
@shelter_required
def shelter_request_detail(req_id):
    req = AdoptionRequest.query.get_or_404(req_id)
    if req.pet.shelter_id != current_user.id:
        abort(403)
    messages = (
        Message.query.filter(
            or_(
                and_(
                    Message.sender_id == req.adopter_id,
                    Message.receiver_id == current_user.id,
                ),
                and_(
                    Message.sender_id == current_user.id,
                    Message.receiver_id == req.adopter_id,
                ),
            ),
            or_(Message.pet_id == req.pet_id, Message.pet_id.is_(None)),
        )
        .order_by(Message.created_at.asc())
        .all()
    )
    return render_template(
        "adoptions/shelter_detail.html", req=req, messages=messages
    )


@adoptions_bp.route("/shelter/requests/<int:req_id>/approve", methods=["POST"])
@login_required
@shelter_required
def approve_request(req_id):
    req = AdoptionRequest.query.get_or_404(req_id)
    if req.pet.shelter_id != current_user.id:
        abort(403)
    if req.status != AdoptionStatus.pending:
        return redirect(url_for("adoptions.shelter_requests")), 400

    req.status = AdoptionStatus.approved
    req.pet.status = PetStatus.adopted
    others = AdoptionRequest.query.filter(
        AdoptionRequest.pet_id == req.pet_id,
        AdoptionRequest.id != req.id,
    ).all()
    for other in others:
        if other.status == AdoptionStatus.pending:
            other.status = AdoptionStatus.rejected
            create_notification(
                other.adopter_id,
                NotificationType.request_rejected,
                f"Tu solicitud para {req.pet.name} fue rechazada (otro adoptante fue seleccionado).",
                "/adoptions/my",
            )
    create_notification(
        req.adopter_id,
        NotificationType.request_approved,
        f"¡Tu solicitud para adoptar a {req.pet.name} fue aprobada!",
        "/adoptions/my",
    )
    db.session.commit()
    flash("Adopción aprobada", "success")
    return redirect(url_for("adoptions.shelter_requests"))


@adoptions_bp.route("/shelter/requests/<int:req_id>/reject", methods=["POST"])
@login_required
@shelter_required
def reject_request(req_id):
    req = AdoptionRequest.query.get_or_404(req_id)
    if req.pet.shelter_id != current_user.id:
        abort(403)
    if req.status != AdoptionStatus.pending:
        return redirect(url_for("adoptions.shelter_request_detail", req_id=req.id)), 400
    req.status = AdoptionStatus.rejected
    create_notification(
        req.adopter_id,
        NotificationType.request_rejected,
        f"Tu solicitud para {req.pet.name} fue rechazada.",
        "/adoptions/my",
    )
    db.session.commit()
    flash("Solicitud rechazada", "success")
    return redirect(url_for("adoptions.shelter_request_detail", req_id=req.id))
