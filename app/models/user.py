import enum
from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class UserRole(enum.Enum):
    adopter = "adopter"
    shelter = "shelter"
    admin = "admin"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), nullable=False
    )
    city: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(20))
    bio: Mapped[str | None] = mapped_column(Text)
    is_suspended: Mapped[bool] = mapped_column(default=False)
    suspended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    pets: Mapped[list["Pet"]] = relationship(
        "Pet", back_populates="shelter", foreign_keys="Pet.shelter_id"
    )
    adoption_requests: Mapped[list["AdoptionRequest"]] = relationship(
        "AdoptionRequest", back_populates="adopter", foreign_keys="AdoptionRequest.adopter_id"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="adopter"
    )
    search_alerts: Mapped[list["SearchAlert"]] = relationship(
        "SearchAlert", back_populates="adopter"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user"
    )
    reviews_written: Mapped[list["Review"]] = relationship(
        "Review", back_populates="reviewer", foreign_keys="Review.reviewer_id"
    )
    reviews_received: Mapped[list["Review"]] = relationship(
        "Review", back_populates="shelter", foreign_keys="Review.shelter_id"
    )
