"""Family member schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class FamilyMemberBase(BaseModel):
    """Base family member schema."""

    user_id: int
    elder_id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    relationship_type: str = Field(..., max_length=50)
    custom_relationship_label: Optional[str] = Field(None, max_length=100)
    access_level: str = Field(default="viewer", max_length=50)
    specific_permissions: Optional[dict] = None
    notification_settings: Optional[dict] = None
    language: str = Field(default="en", max_length=10)


class FamilyMemberCreate(FamilyMemberBase):
    """Schema for creating a family member."""

    pass


class FamilyMemberUpdate(BaseModel):
    """Schema for updating a family member."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    relationship_type: Optional[str] = Field(None, max_length=50)
    custom_relationship_label: Optional[str] = Field(None, max_length=100)
    access_level: Optional[str] = Field(None, max_length=50)
    specific_permissions: Optional[dict] = None
    notification_settings: Optional[dict] = None
    language: Optional[str] = Field(None, max_length=10)


class FamilyMemberResponse(FamilyMemberBase):
    """Schema for family member response."""

    id: int
    last_login_at: Optional[datetime]
    total_time_spent: int
    memories_listened: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FamilyMemberList(BaseModel):
    """Schema for paginated family member list."""

    items: list[FamilyMemberResponse]
    total: int
    page: int
    size: int
    pages: int
