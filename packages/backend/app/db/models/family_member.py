"""Family member database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class FamilyMember(Base):
    """Family member model linking users to elders."""

    __tablename__ = "family_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    elder_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("elders.id"), nullable=False, index=True
    )

    # Identity
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Relationship
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False)
    custom_relationship_label: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # Permissions
    access_level: Mapped[str] = mapped_column(
        String(50), default="viewer", nullable=False
    )
    specific_permissions: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Preferences
    notification_settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    # Activity
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_time_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    memories_listened: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<FamilyMember(id={self.id}, name={self.name}, relationship={self.relationship_type})>"
