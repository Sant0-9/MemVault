"""Memory schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MemoryBase(BaseModel):
    """Base memory schema."""

    elder_id: int
    title: Optional[str] = Field(None, max_length=255)
    transcription: Optional[str] = None
    summary: Optional[str] = None
    full_text: Optional[str] = None
    audio_url: Optional[str] = Field(None, max_length=500)
    audio_cid: Optional[str] = Field(None, max_length=255)
    duration_seconds: Optional[int] = None
    waveform_data: Optional[dict] = None
    category: Optional[str] = Field(None, max_length=50)
    subcategory: Optional[str] = Field(None, max_length=50)
    era: Optional[str] = Field(None, max_length=50)
    decade: Optional[str] = Field(None, max_length=10)
    location: Optional[str] = Field(None, max_length=255)
    date_of_event: Optional[datetime] = None
    people_mentioned: Optional[dict] = None
    tags: Optional[dict] = None
    entities: Optional[dict] = None
    sentiment: Optional[str] = Field(None, max_length=50)
    emotional_tone: Optional[str] = Field(None, max_length=50)
    historical_context: Optional[str] = None
    related_events: Optional[dict] = None
    is_private: bool = False
    is_sensitive: bool = False
    content_warnings: Optional[dict] = None
    transcription_confidence: Optional[float] = None
    audio_quality_score: Optional[float] = None
    recorded_at: Optional[datetime] = None


class MemoryCreate(MemoryBase):
    """Schema for creating a memory."""

    pass


class MemoryUpdate(BaseModel):
    """Schema for updating a memory."""

    title: Optional[str] = Field(None, max_length=255)
    transcription: Optional[str] = None
    summary: Optional[str] = None
    full_text: Optional[str] = None
    audio_url: Optional[str] = Field(None, max_length=500)
    audio_cid: Optional[str] = Field(None, max_length=255)
    duration_seconds: Optional[int] = None
    waveform_data: Optional[dict] = None
    category: Optional[str] = Field(None, max_length=50)
    subcategory: Optional[str] = Field(None, max_length=50)
    era: Optional[str] = Field(None, max_length=50)
    decade: Optional[str] = Field(None, max_length=10)
    location: Optional[str] = Field(None, max_length=255)
    date_of_event: Optional[datetime] = None
    people_mentioned: Optional[dict] = None
    tags: Optional[dict] = None
    entities: Optional[dict] = None
    sentiment: Optional[str] = Field(None, max_length=50)
    emotional_tone: Optional[str] = Field(None, max_length=50)
    historical_context: Optional[str] = None
    related_events: Optional[dict] = None
    is_private: Optional[bool] = None
    is_sensitive: Optional[bool] = None
    content_warnings: Optional[dict] = None
    transcription_confidence: Optional[float] = None
    audio_quality_score: Optional[float] = None
    recorded_at: Optional[datetime] = None


class MemoryResponse(MemoryBase):
    """Schema for memory response."""

    id: int
    play_count: int
    share_count: int
    favorite_by: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemoryList(BaseModel):
    """Schema for paginated memory list."""

    items: list[MemoryResponse]
    total: int
    page: int
    size: int
    pages: int
