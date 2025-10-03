"""Advanced search endpoints."""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models.memory import Memory

router = APIRouter()


@router.get("/search")
async def search_memories(
    q: str = Query(..., min_length=1, description="Search query"),
    elder_id: Optional[int] = Query(None, description="Filter by elder ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    era: Optional[str] = Query(None, description="Filter by era"),
    decade: Optional[str] = Query(None, description="Filter by decade"),
    emotional_tone: Optional[str] = Query(None, description="Filter by emotional tone"),
    location: Optional[str] = Query(None, description="Filter by location"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Advanced search for memories with filters and facets.

    Full-text search on title, transcription, and summary.
    Multiple filters can be combined.
    """
    query = select(Memory).where(Memory.deleted_at.is_(None))

    search_term = f"%{q.lower()}%"
    search_conditions = or_(
        func.lower(Memory.title).like(search_term),
        func.lower(Memory.transcription).like(search_term),
        func.lower(Memory.summary).like(search_term),
    )
    query = query.where(search_conditions)

    if elder_id is not None:
        query = query.where(Memory.elder_id == elder_id)

    if category:
        query = query.where(Memory.category == category)

    if era:
        query = query.where(Memory.era == era)

    if decade:
        query = query.where(Memory.decade == decade)

    if emotional_tone:
        query = query.where(Memory.emotional_tone == emotional_tone)

    if location:
        query = query.where(func.lower(Memory.location).like(f"%{location.lower()}%"))

    if date_from:
        from datetime import datetime

        date_from_obj = datetime.fromisoformat(date_from)
        query = query.where(Memory.date_of_event >= date_from_obj)

    if date_to:
        from datetime import datetime

        date_to_obj = datetime.fromisoformat(date_to)
        query = query.where(Memory.date_of_event <= date_to_obj)

    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    memories = result.scalars().all()

    facets = await _get_search_facets(db, elder_id)

    return {
        "query": q,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "results": [
            {
                "id": memory.id,
                "elder_id": memory.elder_id,
                "title": memory.title,
                "summary": memory.summary,
                "category": memory.category,
                "era": memory.era,
                "decade": memory.decade,
                "emotional_tone": memory.emotional_tone,
                "location": memory.location,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "created_at": memory.created_at.isoformat(),
            }
            for memory in memories
        ],
        "facets": facets,
        "filters_applied": {
            "elder_id": elder_id,
            "category": category,
            "era": era,
            "decade": decade,
            "emotional_tone": emotional_tone,
            "location": location,
            "date_from": date_from,
            "date_to": date_to,
        },
    }


async def _get_search_facets(
    db: AsyncSession, elder_id: Optional[int] = None
) -> dict[str, Any]:
    """Get facets for search filtering."""
    base_query = select(Memory).where(Memory.deleted_at.is_(None))

    if elder_id is not None:
        base_query = base_query.where(Memory.elder_id == elder_id)

    category_query = (
        select(Memory.category, func.count(Memory.id).label("count"))
        .select_from(base_query.subquery())
        .where(Memory.category.isnot(None))
        .group_by(Memory.category)
    )
    category_result = await db.execute(category_query)
    categories = [
        {"value": row[0], "count": row[1]} for row in category_result.fetchall()
    ]

    era_query = (
        select(Memory.era, func.count(Memory.id).label("count"))
        .select_from(base_query.subquery())
        .where(Memory.era.isnot(None))
        .group_by(Memory.era)
    )
    era_result = await db.execute(era_query)
    eras = [{"value": row[0], "count": row[1]} for row in era_result.fetchall()]

    decade_query = (
        select(Memory.decade, func.count(Memory.id).label("count"))
        .select_from(base_query.subquery())
        .where(Memory.decade.isnot(None))
        .group_by(Memory.decade)
        .order_by(Memory.decade)
    )
    decade_result = await db.execute(decade_query)
    decades = [{"value": row[0], "count": row[1]} for row in decade_result.fetchall()]

    tone_query = (
        select(Memory.emotional_tone, func.count(Memory.id).label("count"))
        .select_from(base_query.subquery())
        .where(Memory.emotional_tone.isnot(None))
        .group_by(Memory.emotional_tone)
    )
    tone_result = await db.execute(tone_query)
    emotional_tones = [
        {"value": row[0], "count": row[1]} for row in tone_result.fetchall()
    ]

    return {
        "categories": categories,
        "eras": eras,
        "decades": decades,
        "emotional_tones": emotional_tones,
    }


@router.get("/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Search query prefix"),
    elder_id: Optional[int] = Query(None, description="Filter by elder ID"),
    limit: int = Query(10, ge=1, le=20, description="Max suggestions"),
    db: AsyncSession = Depends(get_db),
) -> list[str]:
    """Get search suggestions based on partial query."""
    query = select(Memory.title).where(
        and_(
            Memory.deleted_at.is_(None),
            Memory.title.isnot(None),
            func.lower(Memory.title).like(f"{q.lower()}%"),
        )
    )

    if elder_id is not None:
        query = query.where(Memory.elder_id == elder_id)

    query = query.distinct().limit(limit)

    result = await db.execute(query)
    suggestions = [row[0] for row in result.fetchall()]

    return suggestions
