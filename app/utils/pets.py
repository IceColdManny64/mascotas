from app.models.pet import Pet, PetPhoto


def primary_photo_url(pet: Pet) -> str | None:
    primary = next((p for p in pet.photos if p.is_primary), None)
    if primary:
        return primary.url
    if pet.photos:
        return pet.photos[0].url
    return None
