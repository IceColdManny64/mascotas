from app.extensions import db
from app.models.message import Notification, NotificationType, SearchAlert
from app.models.pet import Pet


def create_notification(user_id, notif_type, message, link=None):
    notification = Notification(
        user_id=user_id,
        type=notif_type,
        message=message,
        link=link,
    )
    db.session.add(notification)
    return notification


def _alert_matches_pet(alert: SearchAlert, pet: Pet) -> bool:
    if alert.species is not None and alert.species != pet.species:
        return False
    if alert.breed is not None:
        if not pet.breed or alert.breed.lower() not in pet.breed.lower():
            return False
    if alert.age_max is not None:
        if pet.age_years is None or pet.age_years > alert.age_max:
            return False
    if alert.size is not None and alert.size != pet.size:
        return False
    if alert.children_friendly is not None and alert.children_friendly != pet.children_friendly:
        return False
    if (
        alert.other_animals_friendly is not None
        and alert.other_animals_friendly != pet.other_animals_friendly
    ):
        return False
    return True


def check_alerts(pet: Pet):
    """Evaluate active search alerts when a new pet is created."""
    alerts = SearchAlert.query.filter_by(is_active=True).all()
    link = f"/pets/{pet.id}"
    for alert in alerts:
        if alert.adopter_id == pet.shelter_id:
            continue
        if not _alert_matches_pet(alert, pet):
            continue
        existing = Notification.query.filter_by(
            user_id=alert.adopter_id,
            type=NotificationType.new_pet_match,
            link=link,
        ).first()
        if existing:
            continue
        create_notification(
            alert.adopter_id,
            NotificationType.new_pet_match,
            f"Nueva mascota que coincide con tu alerta: {pet.name}",
            link,
        )
    db.session.commit()


def shelter_average_rating(shelter_id: int) -> tuple[float, int]:
    from app.models.review import Review

    reviews = Review.query.filter_by(
        shelter_id=shelter_id, is_reported=False
    ).all()
    if not reviews:
        return 0.0, 0
    avg = sum(r.rating for r in reviews) / len(reviews)
    return round(avg, 1), len(reviews)
