"""Elder database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Elder(Base):
    """Elder model for storing elder profiles."""

    __tablename__ = "elders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Personal info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    hometown: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    current_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Contact
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Profile
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    personality_traits: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Voice
    voice_profile_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sample_audios: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Preferences
    preferred_language: Mapped[str] = mapped_column(
        String(10), default="en", nullable=False
    )
    interview_frequency: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    privacy_settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_active_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<Elder(id={self.id}, name={self.name})>"
