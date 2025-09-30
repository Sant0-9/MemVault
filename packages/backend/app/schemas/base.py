"""Base Pydantic schemas for API responses."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    """Standard success response schema."""

    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    success: bool = False
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(
        cls, items: List[T], total: int, page: int, size: int
    ) -> "PaginatedResponse[T]":
        """Create paginated response with calculated page count."""
        pages = (total + size - 1) // size if size > 0 else 0
        return cls(items=items, total=total, page=page, size=size, pages=pages)
