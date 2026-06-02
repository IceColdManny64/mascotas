import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class AdoptionStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class HomeType(enum.Enum):
    house = "house"
    apartment = "apartment"
    farm = "farm"


class AdoptionRequest(db.Model):
    __tablename__ = "adoption_requests"
    __table_args__ = (
        UniqueConstraint("pet_id", "adopter_id", name="uq_pet_adopter"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    adopter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[AdoptionStatus] = mapped_column(
        Enum(AdoptionStatus, name="adoption_status"), default=AdoptionStatus.pending
    )
    home_type: Mapped[HomeType] = mapped_column(
        Enum(HomeType, name="home_type"), nullable=False
    )
    has_yard: Mapped[bool] = mapped_column(Boolean, nullable=False)
    other_pets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    other_pets_desc: Mapped[str | None] = mapped_column(String(200))
    has_children: Mapped[bool] = mapped_column(Boolean, nullable=False)
    children_ages: Mapped[str | None] = mapped_column(String(100))
    experience: Mapped[str] = mapped_column(Text, nullable=False)
    motivation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    pet: Mapped["Pet"] = relationship("Pet", back_populates="adoption_requests")
    adopter: Mapped["User"] = relationship(
        "User", back_populates="adoption_requests", foreign_keys=[adopter_id]
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="adoption_request"
    )
    review: Mapped["Review | None"] = relationship(
        "Review", back_populates="adoption_request", uselist=False
    )


class Favorite(db.Model):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("adopter_id", "pet_id", name="uq_adopter_pet_favorite"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    adopter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    adopter: Mapped["User"] = relationship("User", back_populates="favorites")
    pet: Mapped["Pet"] = relationship("Pet", back_populates="favorites")
