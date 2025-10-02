"""Pydantic schemas for interview sessions."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class InterviewSessionBase(BaseModel):
    """Base schema for interview session."""

    title: Optional[str] = Field(None, max_length=200)
    topic: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class InterviewSessionCreate(InterviewSessionBase):
    """Schema for creating an interview session."""

    elder_id: int = Field(..., gt=0)


class InterviewSessionUpdate(BaseModel):
    """Schema for updating an interview session."""

    title: Optional[str] = Field(None, max_length=200)
    topic: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, pattern="^(active|completed|paused)$")
    notes: Optional[str] = None
    summary: Optional[str] = None


class InterviewSessionResponse(InterviewSessionBase):
    """Schema for interview session response."""

    id: int
    elder_id: int
    user_id: int
    status: str
    conversation_history: Optional[dict[str, Any]] = None
    summary: Optional[str] = None
    total_questions: int
    total_responses: int
    duration_minutes: Optional[int] = None
    session_metadata: Optional[dict[str, Any]] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class InterviewSessionList(BaseModel):
    """Schema for paginated interview session list."""

    items: list[InterviewSessionResponse]
    total: int
    page: int
    size: int
    pages: int


class ConversationTurn(BaseModel):
    """Schema for a conversation turn."""

    role: str = Field(..., pattern="^(assistant|user)$")
    content: str
    timestamp: Optional[datetime] = None


class InterviewQuestionRequest(BaseModel):
    """Schema for requesting the next interview question."""

    topic: Optional[str] = Field(None, max_length=100)


class InterviewQuestionResponse(BaseModel):
    """Schema for interview question response."""

    question: str
    session_id: int


class InterviewResponseSubmit(BaseModel):
    """Schema for submitting an interview response."""

    response: str = Field(..., min_length=1)
    audio_cid: Optional[str] = None


class InterviewResponseAcknowledge(BaseModel):
    """Schema for acknowledging an interview response."""

    success: bool
    message: str
    next_question: Optional[str] = None
