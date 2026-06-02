from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from app.extensions import db
from app.forms.pets import PetCreateForm, PetForm, SearchForm
from app.models.adoption import AdoptionRequest, AdoptionStatus, Favorite
from app.models.pet import Pet, PetPhoto, PetSize, PetSpecies, PetStatus
from app.models.user import User, UserRole
from app.utils.decorators import shelter_required
from app.utils.notifications import check_alerts, shelter_average_rating
from app.utils.pets import primary_photo_url
from app.utils.uploads import save_pet_photos

pets_bp = Blueprint("pets", __name__)


def _can_edit_pet(pet: Pet) -> bool:
    if not current_user.is_authenticated:
        return False
    if current_user.role == UserRole.admin:
        return True
    return (
        current_user.role == UserRole.shelter
        and pet.shelter_id == current_user.id
    )


@pets_bp.route("/pets")
def index():
    form = SearchForm(request.args, meta={"csrf": False})
    query = (
        Pet.query.join(User, Pet.shelter_id == User.id)
        .filter(Pet.is_active.is_(True), Pet.status == PetStatus.available)
    )

    if form.species.data:
        query = query.filter(Pet.species == PetSpecies(form.species.data))
    if form.breed.data:
        query = query.filter(Pet.breed.ilike(f"%{form.breed.data}%"))
    if form.age_min.data is not None:
        query = query.filter(Pet.age_years >= form.age_min.data)
    if form.age_max.data is not None:
        query = query.filter(Pet.age_years <= form.age_max.data)
    if form.size.data:
        query = query.filter(Pet.size == PetSize(form.size.data))
    if form.location.data:
        query = query.filter(User.city.ilike(f"%{form.location.data}%"))
    if form.children_friendly.data:
        query = query.filter(Pet.children_friendly.is_(True))
    if form.other_animals_friendly.data:
        query = query.filter(Pet.other_animals_friendly.is_(True))

    page = request.args.get("page", 1, type=int)
    pagination = query.order_by(Pet.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    return render_template(
        "pets/index.html",
        form=form,
        pagination=pagination,
        pets=pagination.items,
        total=pagination.total,
    )


@pets_bp.route("/pets/<int:pet_id>")
def detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if not pet.is_active:
        abort(404)

    existing_request = None
    is_favorite = False
    if current_user.is_authenticated and current_user.role == UserRole.adopter:
        existing_request = AdoptionRequest.query.filter_by(
            pet_id=pet.id, adopter_id=current_user.id
        ).first()
        is_favorite = (
            Favorite.query.filter_by(
                adopter_id=current_user.id, pet_id=pet.id
            ).first()
            is not None
        )

    avg_rating, review_count = shelter_average_rating(pet.shelter_id)
    return render_template(
        "pets/detail.html",
        pet=pet,
        existing_request=existing_request,
        is_favorite=is_favorite,
        can_edit=_can_edit_pet(pet),
        shelter_avg=avg_rating,
        shelter_review_count=review_count,
        primary_photo=primary_photo_url(pet),
    )


@pets_bp.route("/pets/new", methods=["GET", "POST"])
@login_required
@shelter_required
def new():
    form = PetCreateForm()
    if form.validate_on_submit():
        files = [f for f in request.files.getlist("photos") if f.filename]
        if len(files) < 1 or len(files) > 5:
            flash("Debes subir entre 1 y 5 fotos.", "danger")
            return render_template("pets/new.html", form=form), 200

        pet = _pet_from_form(form)
        pet.shelter_id = current_user.id
        pet.status = PetStatus.available
        db.session.add(pet)
        db.session.flush()
        _save_photos(pet, files)
        db.session.commit()
        check_alerts(pet)
        flash("Mascota publicada correctamente.", "success")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    return render_template("pets/new.html", form=form)


@pets_bp.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if not pet.is_active and current_user.role != UserRole.admin:
        abort(404)
    if not _can_edit_pet(pet):
        abort(403)

    form = PetForm(obj=pet)
    if request.method == "GET":
        form.species.data = pet.species.value
        if pet.size:
            form.size.data = pet.size.value

    if form.validate_on_submit():
        _update_pet_from_form(pet, form)
        files = [f for f in request.files.getlist("photos") if f.filename]
        if files:
            if len(files) > 5:
                flash("Máximo 5 fotos.", "danger")
                return render_template("pets/edit.html", form=form, pet=pet), 200
            _save_photos(pet, files, replace=False)
        db.session.commit()
        flash("Mascota actualizada.", "success")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    return render_template("pets/edit.html", form=form, pet=pet)


@pets_bp.route("/pets/<int:pet_id>/delete", methods=["POST"])
@login_required
def delete(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if not _can_edit_pet(pet):
        abort(403)
    pending = AdoptionRequest.query.filter_by(
        pet_id=pet.id, status=AdoptionStatus.pending
    ).count()
    if pending > 0:
        flash(
            "No se puede eliminar: hay solicitudes de adopción pendientes.",
            "danger",
        )
        return redirect(url_for("pets.detail", pet_id=pet.id)), 400
    pet.is_active = False
    db.session.commit()
    flash("Mascota eliminada.", "success")
    return redirect(url_for("pets.index"))


@pets_bp.route("/pets/<int:pet_id>/favorite", methods=["POST"])
def favorite(pet_id):
    if not current_user.is_authenticated:
        return jsonify({"redirect": "/login"}), 401
    if current_user.role != UserRole.adopter:
        return jsonify({"error": "Forbidden"}), 403

    pet = Pet.query.get_or_404(pet_id)
    existing = Favorite.query.filter_by(
        adopter_id=current_user.id, pet_id=pet.id
    ).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"status": "removed"})
    count = Favorite.query.filter_by(adopter_id=current_user.id).count()
    if count >= 50:
        return jsonify({"error": "Máximo 50 favoritos alcanzado"}), 400
    fav = Favorite(adopter_id=current_user.id, pet_id=pet.id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"status": "added"})


def _pet_from_form(form):
    size = PetSize(form.size.data) if form.size.data else None
    return Pet(
        name=form.name.data,
        species=PetSpecies(form.species.data),
        breed=form.breed.data or None,
        age_years=form.age_years.data,
        size=size,
        temperament=form.temperament.data or None,
        description=form.description.data,
        medical_history=form.medical_history.data or None,
        special_requirements=form.special_requirements.data or None,
        children_friendly=form.children_friendly.data,
        other_animals_friendly=form.other_animals_friendly.data,
    )


def _update_pet_from_form(pet, form):
    pet.name = form.name.data
    pet.species = PetSpecies(form.species.data)
    pet.breed = form.breed.data or None
    pet.age_years = form.age_years.data
    pet.size = PetSize(form.size.data) if form.size.data else None
    pet.temperament = form.temperament.data or None
    pet.description = form.description.data
    pet.medical_history = form.medical_history.data or None
    pet.special_requirements = form.special_requirements.data or None
    pet.children_friendly = form.children_friendly.data
    pet.other_animals_friendly = form.other_animals_friendly.data


def _save_photos(pet, files, replace=True):
    urls = save_pet_photos(files)
    if not urls:
        return
    has_primary = any(p.is_primary for p in pet.photos)
    for i, url in enumerate(urls):
        is_primary = not has_primary and i == 0
        db.session.add(PetPhoto(pet_id=pet.id, url=url, is_primary=is_primary))
        if is_primary:
            has_primary = True
