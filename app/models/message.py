import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.pet import PetSize, PetSpecies


class NotificationType(enum.Enum):
    new_pet_match = "new_pet_match"
    request_approved = "request_approved"
    request_rejected = "request_rejected"
    new_message = "new_message"


class SearchAlert(db.Model):
    __tablename__ = "search_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    adopter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    species: Mapped[PetSpecies | None] = mapped_column(
        Enum(PetSpecies, name="alert_species")
    )
    breed: Mapped[str | None] = mapped_column(String(100))
    age_max: Mapped[int | None] = mapped_column(Integer)
    size: Mapped[PetSize | None] = mapped_column(Enum(PetSize, name="alert_size"))
    children_friendly: Mapped[bool | None] = mapped_column(Boolean)
    other_animals_friendly: Mapped[bool | None] = mapped_column(Boolean)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    adopter: Mapped["User"] = relationship("User", back_populates="search_alerts")


class Notification(db.Model):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type"), nullable=False
    )
    message: Mapped[str] = mapped_column(String(300), nullable=False)
    link: Mapped[str | None] = mapped_column(String(200))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship("User", back_populates="notifications")


class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    pet_id: Mapped[int | None] = mapped_column(ForeignKey("pets.id"))
    adoption_request_id: Mapped[int | None] = mapped_column(
        ForeignKey("adoption_requests.id")
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id])
    pet: Mapped["Pet | None"] = relationship("Pet")
    adoption_request: Mapped["AdoptionRequest | None"] = relationship(
        "AdoptionRequest", back_populates="messages"
    )
