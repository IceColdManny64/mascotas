import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class PetSpecies(enum.Enum):
    dog = "dog"
    cat = "cat"
    rabbit = "rabbit"
    bird = "bird"
    other = "other"


class PetSize(enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"


class PetStatus(enum.Enum):
    available = "available"
    pending = "pending"
    adopted = "adopted"


class Pet(db.Model):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[PetSpecies] = mapped_column(
        Enum(PetSpecies, name="pet_species"), nullable=False
    )
    breed: Mapped[str | None] = mapped_column(String(100))
    age_years: Mapped[int | None] = mapped_column(Integer)
    size: Mapped[PetSize | None] = mapped_column(Enum(PetSize, name="pet_size"))
    temperament: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    medical_history: Mapped[str | None] = mapped_column(Text)
    special_requirements: Mapped[str | None] = mapped_column(Text)
    children_friendly: Mapped[bool] = mapped_column(Boolean, default=False)
    other_animals_friendly: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[PetStatus] = mapped_column(
        Enum(PetStatus, name="pet_status"), default=PetStatus.available
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    shelter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    shelter: Mapped["User"] = relationship(
        "User", back_populates="pets", foreign_keys=[shelter_id]
    )
    photos: Mapped[list["PetPhoto"]] = relationship(
        "PetPhoto", back_populates="pet", cascade="all, delete-orphan"
    )
    adoption_requests: Mapped[list["AdoptionRequest"]] = relationship(
        "AdoptionRequest", back_populates="pet"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="pet"
    )


class PetPhoto(db.Model):
    __tablename__ = "pet_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(
        ForeignKey("pets.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(300), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    pet: Mapped["Pet"] = relationship("Pet", back_populates="photos")
