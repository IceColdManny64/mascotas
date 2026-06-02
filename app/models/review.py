from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Review(db.Model):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("reviewer_id", "shelter_id", name="uq_reviewer_shelter"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    shelter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    adoption_request_id: Mapped[int] = mapped_column(
        ForeignKey("adoption_requests.id"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    is_reported: Mapped[bool] = mapped_column(Boolean, default=False)
    reported_reason: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    shelter: Mapped["User"] = relationship(
        "User", back_populates="reviews_received", foreign_keys=[shelter_id]
    )
    reviewer: Mapped["User"] = relationship(
        "User", back_populates="reviews_written", foreign_keys=[reviewer_id]
    )
    adoption_request: Mapped["AdoptionRequest"] = relationship(
        "AdoptionRequest", back_populates="review"
    )
