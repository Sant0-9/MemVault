"""Memory CRUD endpoints."""

from math import ceil
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models import Elder, Memory
from app.schemas.memory_schema import (
    MemoryCreate,
    MemoryList,
    MemoryResponse,
    MemoryUpdate,
)
from app.services.openai_service import openai_service

router = APIRouter()


@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory_data: MemoryCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new memory."""
    result = await db.execute(
        select(Elder).where(
            Elder.id == memory_data.elder_id, Elder.deleted_at.is_(None)
        )
    )
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elder not found",
        )

    memory = Memory(**memory_data.model_dump())
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


@router.get("/", response_model=MemoryList)
async def list_memories(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    elder_id: int | None = Query(None),
    category: str | None = Query(None),
    era: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List memories with pagination and filtering."""
    query = select(Memory).where(Memory.deleted_at.is_(None))

    if elder_id:
        query = query.where(Memory.elder_id == elder_id)

    if category:
        query = query.where(Memory.category == category)

    if era:
        query = query.where(Memory.era == era)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Memory.title.ilike(search_pattern),
                Memory.transcription.ilike(search_pattern),
                Memory.summary.ilike(search_pattern),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = (
        query.order_by(Memory.created_at.desc()).offset((page - 1) * size).limit(size)
    )

    result = await db.execute(query)
    memories = list(result.scalars().all())

    return MemoryList(
        items=memories,  # type: ignore[arg-type]
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total > 0 else 0,
    )


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """Get memory details by ID."""
    result = await db.execute(
        select(Memory).where(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    memory.play_count += 1
    await db.commit()
    await db.refresh(memory)

    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: int, memory_data: MemoryUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    """Update memory."""
    result = await db.execute(
        select(Memory).where(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    update_data = memory_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(memory, field, value)

    await db.commit()
    await db.refresh(memory)
    return memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(memory_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Soft delete a memory."""
    result = await db.execute(
        select(Memory).where(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    from datetime import datetime, timezone

    memory.deleted_at = datetime.now(timezone.utc)
    await db.commit()


@router.post("/{memory_id}/enrich", response_model=MemoryResponse)
async def enrich_memory(memory_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """Enrich memory with AI-generated metadata."""
    result = await db.execute(
        select(Memory).where(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    if not memory.transcription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Memory must have transcription to be enriched",
        )

    enrichment_data = await openai_service.enrich_memory(
        memory.transcription, memory.tags or []
    )

    memory.category = enrichment_data.get("category")
    memory.tags = enrichment_data.get("tags")
    memory.emotional_tone = enrichment_data.get("emotional_tone")
    memory.era = enrichment_data.get("time_period")

    if not memory.summary:
        memory.summary = enrichment_data.get("summary")

    if "people" in enrichment_data:
        memory.people_mentioned = enrichment_data.get("people")
    if "locations" in enrichment_data:
        memory.location = ", ".join(enrichment_data.get("locations", []))[:200]

    await db.commit()
    await db.refresh(memory)
    return memory
