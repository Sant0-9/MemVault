"""Timeline visualization endpoints."""

from typing import Any, Optional, cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models.elder import Elder
from app.db.models.memory import Memory

router = APIRouter()


@router.get("/elders/{elder_id}/timeline")
async def get_elder_timeline(
    elder_id: int,
    group_by: str = "decade",
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get timeline data for an elder's memories.

    Args:
        elder_id: ID of the elder
        group_by: How to group memories (decade, year, era, category)

    Returns:
        Timeline data grouped by specified parameter
    """
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    query = (
        select(Memory)
        .where(
            and_(
                Memory.elder_id == elder_id,
                Memory.deleted_at.is_(None),
            )
        )
        .order_by(Memory.date_of_event.asc())
    )

    result = await db.execute(query)
    memories = cast(list[Memory], list(result.scalars().all()))

    if group_by == "decade":
        timeline_data = _group_by_decade(memories)
    elif group_by == "year":
        timeline_data = _group_by_year(memories)
    elif group_by == "era":
        timeline_data = _group_by_era(memories)
    elif group_by == "category":
        timeline_data = _group_by_category(memories)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid group_by: {group_by}")

    return {
        "elder_id": elder_id,
        "elder_name": elder.name,
        "group_by": group_by,
        "total_memories": len(memories),
        "timeline": timeline_data,
    }


def _group_by_decade(memories: list[Memory]) -> list[dict[str, Any]]:
    """Group memories by decade."""
    decades: dict[str, list[dict[str, Any]]] = {}

    for memory in memories:
        decade_key = "Unknown"

        if memory.decade:
            decade_key = memory.decade
        elif memory.date_of_event:
            year = memory.date_of_event.year
            decade_key = f"{(year // 10) * 10}s"

        if decade_key not in decades:
            decades[decade_key] = []

        decades[decade_key].append(
            {
                "id": memory.id,
                "title": memory.title,
                "category": memory.category,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "summary": memory.summary,
                "emotional_tone": memory.emotional_tone,
                "location": memory.location,
            }
        )

    sorted_decades = sorted(
        [
            {
                "period": decade,
                "memories": memories_list,
                "count": len(memories_list),
            }
            for decade, memories_list in decades.items()
        ],
        key=lambda x: str(x["period"]) if x["period"] != "Unknown" else "9999",
    )

    return sorted_decades


def _group_by_year(memories: list[Memory]) -> list[dict[str, Any]]:
    """Group memories by year."""
    years: dict[int, list[dict[str, Any]]] = {}

    for memory in memories:
        if memory.date_of_event:
            year = memory.date_of_event.year
        else:
            year = 0

        if year not in years:
            years[year] = []

        years[year].append(
            {
                "id": memory.id,
                "title": memory.title,
                "category": memory.category,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "summary": memory.summary,
                "emotional_tone": memory.emotional_tone,
                "location": memory.location,
            }
        )

    sorted_years = sorted(
        [
            {
                "period": str(year) if year > 0 else "Unknown",
                "memories": memories_list,
                "count": len(memories_list),
            }
            for year, memories_list in years.items()
        ],
        key=lambda x: int(str(x["period"])) if str(x["period"]).isdigit() else 9999,
    )

    return sorted_years


def _group_by_era(memories: list[Memory]) -> list[dict[str, Any]]:
    """Group memories by era/life stage."""
    eras: dict[str, list[dict[str, Any]]] = {}

    for memory in memories:
        era_key = memory.era or "Unknown"

        if era_key not in eras:
            eras[era_key] = []

        eras[era_key].append(
            {
                "id": memory.id,
                "title": memory.title,
                "category": memory.category,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "summary": memory.summary,
                "emotional_tone": memory.emotional_tone,
                "location": memory.location,
            }
        )

    era_order = [
        "childhood",
        "adolescence",
        "young_adult",
        "adult",
        "middle_age",
        "senior",
        "Unknown",
    ]

    sorted_eras = sorted(
        [
            {
                "period": era,
                "memories": memories_list,
                "count": len(memories_list),
            }
            for era, memories_list in eras.items()
        ],
        key=lambda x: (
            era_order.index(str(x["period"]))
            if str(x["period"]) in era_order
            else len(era_order)
        ),
    )

    return sorted_eras


def _group_by_category(memories: list[Memory]) -> list[dict[str, Any]]:
    """Group memories by category."""
    categories: dict[str, list[dict[str, Any]]] = {}

    for memory in memories:
        category_key = memory.category or "Uncategorized"

        if category_key not in categories:
            categories[category_key] = []

        categories[category_key].append(
            {
                "id": memory.id,
                "title": memory.title,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "summary": memory.summary,
                "emotional_tone": memory.emotional_tone,
                "location": memory.location,
            }
        )

    sorted_categories = sorted(
        [
            {
                "period": category,
                "memories": memories_list,
                "count": len(memories_list),
            }
            for category, memories_list in categories.items()
        ],
        key=lambda x: int(x["count"]) if isinstance(x["count"], int) else 0,
        reverse=True,
    )

    return sorted_categories


@router.get("/elders/{elder_id}/timeline/stats")
async def get_timeline_stats(
    elder_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get timeline statistics for an elder."""
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    query = select(Memory).where(
        and_(
            Memory.elder_id == elder_id,
            Memory.deleted_at.is_(None),
        )
    )

    result = await db.execute(query)
    memories = cast(list[Memory], list(result.scalars().all()))

    earliest_memory = None
    latest_memory = None

    for memory in memories:
        if memory.date_of_event:
            if earliest_memory is None or memory.date_of_event < earliest_memory:
                earliest_memory = memory.date_of_event
            if latest_memory is None or memory.date_of_event > latest_memory:
                latest_memory = memory.date_of_event

    decades_covered: set[str] = set()
    categories: dict[str, int] = {}
    eras: dict[str, int] = {}

    for memory in memories:
        if memory.decade:
            decades_covered.add(memory.decade)
        elif memory.date_of_event:
            year = memory.date_of_event.year
            decades_covered.add(f"{(year // 10) * 10}s")

        if memory.category:
            categories[memory.category] = categories.get(memory.category, 0) + 1

        if memory.era:
            eras[memory.era] = eras.get(memory.era, 0) + 1

    return {
        "total_memories": len(memories),
        "earliest_memory": earliest_memory.isoformat() if earliest_memory else None,
        "latest_memory": latest_memory.isoformat() if latest_memory else None,
        "decades_covered": sorted(list(decades_covered)),
        "total_decades": len(decades_covered),
        "categories": categories,
        "eras": eras,
        "completeness_score": _calculate_completeness(decades_covered, memories),
    }


def _calculate_completeness(decades_covered: set[str], memories: list[Memory]) -> float:
    """Calculate timeline completeness score (0-100)."""
    if not memories:
        return 0.0

    expected_decades = 8
    decade_score = (len(decades_covered) / expected_decades) * 50

    category_coverage = len(set(m.category for m in memories if m.category))
    category_score = min((category_coverage / 10) * 50, 50)

    return min(decade_score + category_score, 100.0)
