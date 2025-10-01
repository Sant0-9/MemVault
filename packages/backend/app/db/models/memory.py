"""Memory database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Memory(Base):
    """Memory model for storing elder memories."""

    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    elder_id: Mapped[int] = mapped_column(Integer, ForeignKey("elders.id"), nullable=False, index=True)

    # Content
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    transcription: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    full_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Media
    audio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    audio_cid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    waveform_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Classification
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    era: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    decade: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Context
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_of_event: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    people_mentioned: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # AI Analysis
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    entities: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    emotional_tone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Enrichment
    historical_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_events: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Engagement
    play_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    share_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    favorite_by: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Privacy
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    content_warnings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Quality
    transcription_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    audio_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    recorded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Full-text search
    search_vector: Mapped[Optional[str]] = mapped_column(TSVECTOR, nullable=True)

    def __repr__(self) -> str:
        return f"<Memory(id={self.id}, elder_id={self.elder_id}, title={self.title})>"
