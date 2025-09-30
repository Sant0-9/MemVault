from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(
        cls, items: List[T], total: int, page: int, size: int
    ) -> "PaginatedResponse[T]":
        pages = (total + size - 1) // size if size > 0 else 0
        return cls(items=items, total=total, page=page, size=size, pages=pages)
