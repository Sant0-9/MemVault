"""Family member CRUD endpoints."""

from math import ceil
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models import Elder, FamilyMember, User
from app.schemas.family_member_schema import (
    FamilyMemberCreate,
    FamilyMemberList,
    FamilyMemberResponse,
    FamilyMemberUpdate,
)

router = APIRouter()


@router.post(
    "/", response_model=FamilyMemberResponse, status_code=status.HTTP_201_CREATED
)
async def create_family_member(
    family_member_data: FamilyMemberCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new family member relationship."""
    user_result = await db.execute(
        select(User).where(User.id == family_member_data.user_id)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    elder_result = await db.execute(
        select(Elder).where(
            Elder.id == family_member_data.elder_id, Elder.deleted_at.is_(None)
        )
    )
    elder = elder_result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elder not found",
        )

    family_member = FamilyMember(**family_member_data.model_dump())
    db.add(family_member)
    await db.commit()
    await db.refresh(family_member)
    return family_member


@router.get("/", response_model=FamilyMemberList)
async def list_family_members(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    elder_id: int | None = Query(None),
    user_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List family members with pagination and filtering."""
    query = select(FamilyMember).where(FamilyMember.deleted_at.is_(None))

    if elder_id:
        query = query.where(FamilyMember.elder_id == elder_id)

    if user_id:
        query = query.where(FamilyMember.user_id == user_id)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = (
        query.order_by(FamilyMember.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )

    result = await db.execute(query)
    family_members = list(result.scalars().all())

    return FamilyMemberList(
        items=family_members,  # type: ignore[arg-type]
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total > 0 else 0,
    )


@router.get("/{family_member_id}", response_model=FamilyMemberResponse)
async def get_family_member(
    family_member_id: int, db: AsyncSession = Depends(get_db)
) -> Any:
    """Get family member details by ID."""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == family_member_id, FamilyMember.deleted_at.is_(None)
        )
    )
    family_member = result.scalar_one_or_none()

    if not family_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )

    return family_member


@router.put("/{family_member_id}", response_model=FamilyMemberResponse)
async def update_family_member(
    family_member_id: int,
    family_member_data: FamilyMemberUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update family member."""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == family_member_id, FamilyMember.deleted_at.is_(None)
        )
    )
    family_member = result.scalar_one_or_none()

    if not family_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )

    update_data = family_member_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(family_member, field, value)

    await db.commit()
    await db.refresh(family_member)
    return family_member


@router.delete("/{family_member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family_member(
    family_member_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """Soft delete a family member."""
    result = await db.execute(
        select(FamilyMember).where(
            FamilyMember.id == family_member_id, FamilyMember.deleted_at.is_(None)
        )
    )
    family_member = result.scalar_one_or_none()

    if not family_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )

    from datetime import datetime, timezone

    family_member.deleted_at = datetime.now(timezone.utc)
    await db.commit()
