"""Memory export endpoints."""

import io
import json
from datetime import datetime
from typing import Any, Optional, cast

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models.elder import Elder
from app.db.models.memory import Memory

router = APIRouter()


@router.get("/elders/{elder_id}/export/json")
async def export_memories_json(
    elder_id: int,
    include_audio_urls: bool = Query(True, description="Include audio URLs"),
    include_transcriptions: bool = Query(True, description="Include transcriptions"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Export memories as JSON."""
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

    if category:
        query = query.where(Memory.category == category)

    result = await db.execute(query.order_by(Memory.created_at.desc()))
    memories = cast(list[Memory], list(result.scalars().all()))

    export_data = {
        "export_date": datetime.now().isoformat(),
        "elder": {
            "id": elder.id,
            "name": elder.name,
            "date_of_birth": (
                elder.date_of_birth.isoformat() if elder.date_of_birth else None
            ),
            "hometown": elder.hometown,
            "bio": elder.bio,
        },
        "total_memories": len(memories),
        "memories": [
            {
                "id": memory.id,
                "title": memory.title,
                "transcription": (
                    memory.transcription if include_transcriptions else None
                ),
                "summary": memory.summary,
                "category": memory.category,
                "era": memory.era,
                "decade": memory.decade,
                "location": memory.location,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
                "people_mentioned": memory.people_mentioned,
                "tags": memory.tags,
                "emotional_tone": memory.emotional_tone,
                "sentiment": memory.sentiment,
                "audio_url": memory.audio_url if include_audio_urls else None,
                "duration_seconds": memory.duration_seconds,
                "created_at": memory.created_at.isoformat(),
            }
            for memory in memories
        ],
    }

    json_bytes = json.dumps(export_data, indent=2).encode("utf-8")
    json_stream = io.BytesIO(json_bytes)

    filename = f"memories_{elder.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"

    return StreamingResponse(
        json_stream,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/elders/{elder_id}/export/csv")
async def export_memories_csv(
    elder_id: int,
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Export memories as CSV."""
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

    if category:
        query = query.where(Memory.category == category)

    result = await db.execute(query.order_by(Memory.created_at.desc()))
    memories = cast(list[Memory], list(result.scalars().all()))

    import csv

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)

    writer.writerow(
        [
            "ID",
            "Title",
            "Summary",
            "Category",
            "Era",
            "Decade",
            "Location",
            "Date of Event",
            "Emotional Tone",
            "Duration (seconds)",
            "Created At",
        ]
    )

    for memory in memories:
        writer.writerow(
            [
                memory.id,
                memory.title or "",
                memory.summary or "",
                memory.category or "",
                memory.era or "",
                memory.decade or "",
                memory.location or "",
                memory.date_of_event.isoformat() if memory.date_of_event else "",
                memory.emotional_tone or "",
                memory.duration_seconds or 0,
                memory.created_at.isoformat(),
            ]
        )

    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    csv_stream = io.BytesIO(csv_bytes)

    filename = f"memories_{elder.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        csv_stream,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/elders/{elder_id}/export/markdown")
async def export_memories_markdown(
    elder_id: int,
    category: Optional[str] = Query(None, description="Filter by category"),
    include_transcriptions: bool = Query(
        True, description="Include full transcriptions"
    ),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Export memories as Markdown document."""
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

    if category:
        query = query.where(Memory.category == category)

    result = await db.execute(query.order_by(Memory.date_of_event.asc()))
    memories = cast(list[Memory], list(result.scalars().all()))

    md_content = f"# Life Memories: {elder.name}\n\n"

    if elder.bio:
        md_content += f"## About\n\n{elder.bio}\n\n"

    if elder.date_of_birth:
        md_content += f"**Born:** {elder.date_of_birth.strftime('%B %d, %Y')}\n\n"

    if elder.hometown:
        md_content += f"**Hometown:** {elder.hometown}\n\n"

    md_content += "---\n\n"
    md_content += f"## Memories ({len(memories)})\n\n"

    current_decade = None
    for memory in memories:
        decade = memory.decade or "Unknown Period"

        if decade != current_decade:
            md_content += f"\n### {decade}\n\n"
            current_decade = decade

        md_content += f"#### {memory.title or 'Untitled'}\n\n"

        if memory.date_of_event:
            md_content += f"*{memory.date_of_event.strftime('%B %d, %Y')}*"

        if memory.location:
            md_content += f" • *{memory.location}*"

        md_content += "\n\n"

        if memory.summary:
            md_content += f"{memory.summary}\n\n"

        if include_transcriptions and memory.transcription:
            md_content += f"> {memory.transcription}\n\n"

        if memory.emotional_tone:
            md_content += f"**Emotional Tone:** {memory.emotional_tone}\n\n"

        if memory.category:
            md_content += f"**Category:** {memory.category}\n\n"

        if memory.people_mentioned:
            people = []
            if isinstance(memory.people_mentioned, dict):
                people = list(memory.people_mentioned.keys())
            elif isinstance(memory.people_mentioned, list):
                people = memory.people_mentioned

            if people:
                md_content += f"**People Mentioned:** {', '.join(people)}\n\n"

        md_content += "---\n\n"

    md_content += f"\n*Exported on {datetime.now().strftime('%B %d, %Y')}*\n"

    md_bytes = md_content.encode("utf-8")
    md_stream = io.BytesIO(md_bytes)

    filename = f"memories_{elder.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"

    return StreamingResponse(
        md_stream,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/elders/{elder_id}/export/request")
async def request_export(
    elder_id: int,
    export_format: str = Query(..., regex="^(json|csv|markdown|pdf)$"),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Request an export (for future async processing of PDF/audio compilations).

    For now, this redirects to the appropriate sync endpoint.
    In production, this would create a background job.
    """
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    endpoints = {
        "json": f"/api/v1/export/elders/{elder_id}/export/json",
        "csv": f"/api/v1/export/elders/{elder_id}/export/csv",
        "markdown": f"/api/v1/export/elders/{elder_id}/export/markdown",
    }

    if export_format in endpoints:
        return {
            "status": "ready",
            "download_url": endpoints[export_format]
            + (f"?category={category}" if category else ""),
            "format": export_format,
        }

    return {
        "status": "processing",
        "message": f"{export_format.upper()} export is being prepared. This may take a few minutes.",
        "format": export_format,
    }


@router.get("/elders/{elder_id}/export/audio-compilation")
async def export_audio_compilation(
    elder_id: int,
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Request an audio compilation of all memories.

    This endpoint returns a list of audio URLs to download.
    A future enhancement would compile them into a single file.
    """
    result = await db.execute(select(Elder).where(Elder.id == elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    query = select(Memory).where(
        and_(
            Memory.elder_id == elder_id,
            Memory.deleted_at.is_(None),
            Memory.audio_url.isnot(None),
        )
    )

    if category:
        query = query.where(Memory.category == category)

    result = await db.execute(query.order_by(Memory.date_of_event.asc()))
    memories = cast(list[Memory], list(result.scalars().all()))

    return {
        "elder_id": elder_id,
        "elder_name": elder.name,
        "total_audio_files": len(memories),
        "total_duration_seconds": sum(m.duration_seconds or 0 for m in memories),
        "audio_files": [
            {
                "id": memory.id,
                "title": memory.title,
                "url": memory.audio_url,
                "duration_seconds": memory.duration_seconds,
                "date_of_event": (
                    memory.date_of_event.isoformat() if memory.date_of_event else None
                ),
            }
            for memory in memories
        ],
    }
