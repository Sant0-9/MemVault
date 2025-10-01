"""Elder CRUD endpoints."""

from math import ceil
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models import Elder
from app.schemas.elder_schema import ElderCreate, ElderList, ElderResponse, ElderUpdate

router = APIRouter()


@router.post("/", response_model=ElderResponse, status_code=status.HTTP_201_CREATED)
async def create_elder(elder_data: ElderCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """Create a new elder profile."""
    elder = Elder(**elder_data.model_dump())
    db.add(elder)
    await db.commit()
    await db.refresh(elder)
    return elder


@router.get("/", response_model=ElderList)
async def list_elders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    is_active: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List elders with pagination and filtering."""
    query = select(Elder).where(Elder.deleted_at.is_(None))

    if is_active is not None:
        query = query.where(Elder.is_active == is_active)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Elder.name.ilike(search_pattern),
                Elder.email.ilike(search_pattern),
                Elder.hometown.ilike(search_pattern),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = query.order_by(Elder.created_at.desc()).offset((page - 1) * size).limit(size)

    result = await db.execute(query)
    elders = result.scalars().all()

    return ElderList(
        items=elders,
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total > 0 else 0,
    )


@router.get("/{elder_id}", response_model=ElderResponse)
async def get_elder(elder_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """Get elder details by ID."""
    result = await db.execute(
        select(Elder).where(Elder.id == elder_id, Elder.deleted_at.is_(None))
    )
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elder not found",
        )

    return elder


@router.put("/{elder_id}", response_model=ElderResponse)
async def update_elder(
    elder_id: int, elder_data: ElderUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    """Update elder profile."""
    result = await db.execute(
        select(Elder).where(Elder.id == elder_id, Elder.deleted_at.is_(None))
    )
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elder not found",
        )

    update_data = elder_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(elder, field, value)

    await db.commit()
    await db.refresh(elder)
    return elder


@router.delete("/{elder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_elder(elder_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Soft delete an elder."""
    result = await db.execute(
        select(Elder).where(Elder.id == elder_id, Elder.deleted_at.is_(None))
    )
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elder not found",
        )

    from datetime import datetime, timezone

    elder.deleted_at = datetime.now(timezone.utc)
    await db.commit()
