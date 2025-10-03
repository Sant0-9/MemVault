"""Analytics and insights endpoints."""

from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models.elder import Elder
from app.db.models.memory import Memory

router = APIRouter()


@router.get("/elders/{elder_id}/analytics")
async def get_elder_analytics(
    elder_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get comprehensive analytics for an elder."""
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Elder not found")

    query = select(Memory).where(
        and_(
            Memory.elder_id == elder_id,
            Memory.deleted_at.is_(None),
        )
    )

    result = await db.execute(query)
    memories = result.scalars().all()

    return {
        "elder_id": elder_id,
        "elder_name": elder.name,
        "overview": await _get_overview_stats(memories),
        "timeline_analysis": await _get_timeline_analysis(memories),
        "content_analysis": await _get_content_analysis(memories),
        "emotional_insights": await _get_emotional_insights(memories),
        "engagement_metrics": await _get_engagement_metrics(memories),
        "quality_metrics": await _get_quality_metrics(memories),
    }


async def _get_overview_stats(memories: list[Memory]) -> dict[str, Any]:
    """Get overview statistics."""
    total_memories = len(memories)
    total_duration = sum(m.duration_seconds or 0 for m in memories)

    return {
        "total_memories": total_memories,
        "total_duration_seconds": total_duration,
        "total_duration_formatted": _format_duration(total_duration),
        "average_duration_seconds": total_duration // total_memories if total_memories > 0 else 0,
        "memories_with_audio": sum(1 for m in memories if m.audio_url),
        "memories_with_transcription": sum(1 for m in memories if m.transcription),
    }


async def _get_timeline_analysis(memories: list[Memory]) -> dict[str, Any]:
    """Analyze timeline coverage."""
    decades = {}
    eras = {}
    years = {}

    for memory in memories:
        if memory.decade:
            decades[memory.decade] = decades.get(memory.decade, 0) + 1
        elif memory.date_of_event:
            decade = f"{(memory.date_of_event.year // 10) * 10}s"
            decades[decade] = decades.get(decade, 0) + 1
            years[memory.date_of_event.year] = years.get(memory.date_of_event.year, 0) + 1

        if memory.era:
            eras[memory.era] = eras.get(memory.era, 0) + 1

    earliest = min((m.date_of_event for m in memories if m.date_of_event), default=None)
    latest = max((m.date_of_event for m in memories if m.date_of_event), default=None)

    return {
        "decades": [{"decade": k, "count": v} for k, v in sorted(decades.items())],
        "eras": [{"era": k, "count": v} for k, v in eras.items()],
        "years_with_memories": [{"year": k, "count": v} for k, v in sorted(years.items())],
        "earliest_memory": earliest.isoformat() if earliest else None,
        "latest_memory": latest.isoformat() if latest else None,
        "span_years": (latest.year - earliest.year) if earliest and latest else 0,
    }


async def _get_content_analysis(memories: list[Memory]) -> dict[str, Any]:
    """Analyze content distribution."""
    categories = {}
    locations = set()
    people = set()
    tags_count = {}

    for memory in memories:
        if memory.category:
            categories[memory.category] = categories.get(memory.category, 0) + 1

        if memory.location:
            locations.add(memory.location)

        if memory.people_mentioned:
            if isinstance(memory.people_mentioned, dict):
                people.update(memory.people_mentioned.keys())
            elif isinstance(memory.people_mentioned, list):
                people.update(memory.people_mentioned)

        if memory.tags:
            if isinstance(memory.tags, dict):
                for tag in memory.tags.get("tags", []):
                    tags_count[tag] = tags_count.get(tag, 0) + 1
            elif isinstance(memory.tags, list):
                for tag in memory.tags:
                    tags_count[tag] = tags_count.get(tag, 0) + 1

    top_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "categories": [{"category": k, "count": v} for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)],
        "total_categories": len(categories),
        "locations_mentioned": list(locations),
        "total_locations": len(locations),
        "people_mentioned": list(people),
        "total_people": len(people),
        "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
    }


async def _get_emotional_insights(memories: list[Memory]) -> dict[str, Any]:
    """Analyze emotional content."""
    emotions = {}
    sentiments = {}

    for memory in memories:
        if memory.emotional_tone:
            emotions[memory.emotional_tone] = emotions.get(memory.emotional_tone, 0) + 1

        if memory.sentiment:
            sentiments[memory.sentiment] = sentiments.get(memory.sentiment, 0) + 1

    emotion_distribution = [
        {"emotion": k, "count": v, "percentage": round(v / len(memories) * 100, 1)}
        for k, v in sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    ]

    dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else None

    return {
        "emotion_distribution": emotion_distribution,
        "dominant_emotion": dominant_emotion,
        "sentiment_distribution": [
            {"sentiment": k, "count": v} for k, v in sentiments.items()
        ],
        "emotional_diversity": len(emotions),
    }


async def _get_engagement_metrics(memories: list[Memory]) -> dict[str, Any]:
    """Get engagement metrics."""
    total_plays = sum(m.play_count for m in memories)
    total_shares = sum(m.share_count for m in memories)

    most_played = max(memories, key=lambda m: m.play_count) if memories else None
    most_shared = max(memories, key=lambda m: m.share_count) if memories else None

    return {
        "total_plays": total_plays,
        "total_shares": total_shares,
        "average_plays_per_memory": total_plays // len(memories) if memories else 0,
        "most_played_memory": {
            "id": most_played.id,
            "title": most_played.title,
            "play_count": most_played.play_count,
        } if most_played and most_played.play_count > 0 else None,
        "most_shared_memory": {
            "id": most_shared.id,
            "title": most_shared.title,
            "share_count": most_shared.share_count,
        } if most_shared and most_shared.share_count > 0 else None,
    }


async def _get_quality_metrics(memories: list[Memory]) -> dict[str, Any]:
    """Get quality metrics."""
    transcription_confidences = [
        m.transcription_confidence for m in memories if m.transcription_confidence
    ]
    audio_quality_scores = [
        m.audio_quality_score for m in memories if m.audio_quality_score
    ]

    avg_transcription = (
        sum(transcription_confidences) / len(transcription_confidences)
        if transcription_confidences
        else 0
    )
    avg_audio_quality = (
        sum(audio_quality_scores) / len(audio_quality_scores)
        if audio_quality_scores
        else 0
    )

    return {
        "average_transcription_confidence": round(avg_transcription, 2),
        "average_audio_quality": round(avg_audio_quality, 2),
        "memories_with_high_quality_transcription": sum(
            1 for c in transcription_confidences if c > 0.8
        ),
        "memories_with_low_quality_transcription": sum(
            1 for c in transcription_confidences if c < 0.5
        ),
        "memories_needing_review": sum(
            1 for m in memories
            if m.transcription_confidence and m.transcription_confidence < 0.5
        ),
    }


@router.get("/elders/{elder_id}/analytics/recent-activity")
async def get_recent_activity(
    elder_id: int,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get recent activity analytics."""
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Elder not found")

    cutoff_date = datetime.now() - timedelta(days=days)

    query = select(Memory).where(
        and_(
            Memory.elder_id == elder_id,
            Memory.created_at >= cutoff_date,
            Memory.deleted_at.is_(None),
        )
    ).order_by(Memory.created_at.desc())

    result = await db.execute(query)
    recent_memories = result.scalars().all()

    memories_by_day = {}
    for memory in recent_memories:
        day_key = memory.created_at.date().isoformat()
        if day_key not in memories_by_day:
            memories_by_day[day_key] = []
        memories_by_day[day_key].append({
            "id": memory.id,
            "title": memory.title,
            "category": memory.category,
            "created_at": memory.created_at.isoformat(),
        })

    return {
        "elder_id": elder_id,
        "period_days": days,
        "total_memories": len(recent_memories),
        "memories_by_day": [
            {"date": k, "count": len(v), "memories": v}
            for k, v in sorted(memories_by_day.items(), reverse=True)
        ],
        "average_per_week": len(recent_memories) / (days / 7) if days >= 7 else 0,
    }


@router.get("/analytics/global")
async def get_global_analytics(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get global analytics across all elders."""
    elders_result = await db.execute(select(Elder).where(Elder.deleted_at.is_(None)))
    elders = elders_result.scalars().all()

    memories_result = await db.execute(select(Memory).where(Memory.deleted_at.is_(None)))
    memories = memories_result.scalars().all()

    total_duration = sum(m.duration_seconds or 0 for m in memories)

    categories = {}
    for memory in memories:
        if memory.category:
            categories[memory.category] = categories.get(memory.category, 0) + 1

    return {
        "total_elders": len(elders),
        "total_memories": len(memories),
        "total_duration_seconds": total_duration,
        "total_duration_formatted": _format_duration(total_duration),
        "average_memories_per_elder": len(memories) // len(elders) if elders else 0,
        "most_common_categories": [
            {"category": k, "count": v}
            for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        ],
    }


def _format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
