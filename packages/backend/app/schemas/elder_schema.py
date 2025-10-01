"""Elder schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ElderBase(BaseModel):
    """Base elder schema."""

    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: Optional[datetime] = None
    hometown: Optional[str] = Field(None, max_length=100)
    current_location: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    emergency_contact: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = None
    personality_traits: Optional[dict] = None
    voice_profile_id: Optional[str] = Field(None, max_length=100)
    sample_audios: Optional[dict] = None
    preferred_language: str = Field(default="en", max_length=10)
    interview_frequency: Optional[str] = Field(None, max_length=50)
    privacy_settings: Optional[dict] = None


class ElderCreate(ElderBase):
    """Schema for creating an elder."""

    pass


class ElderUpdate(BaseModel):
    """Schema for updating an elder."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[datetime] = None
    hometown: Optional[str] = Field(None, max_length=100)
    current_location: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    emergency_contact: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = None
    personality_traits: Optional[dict] = None
    voice_profile_id: Optional[str] = Field(None, max_length=100)
    sample_audios: Optional[dict] = None
    preferred_language: Optional[str] = Field(None, max_length=10)
    interview_frequency: Optional[str] = Field(None, max_length=50)
    privacy_settings: Optional[dict] = None
    is_active: Optional[bool] = None


class ElderResponse(ElderBase):
    """Schema for elder response."""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_active_at: Optional[datetime]

    class Config:
        from_attributes = True


class ElderList(BaseModel):
    """Schema for paginated elder list."""

    items: list[ElderResponse]
    total: int
    page: int
    size: int
    pages: int
