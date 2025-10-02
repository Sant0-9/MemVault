"""Audio processing endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models import Memory
from app.schemas.memory_schema import MemoryResponse
from app.services.ipfs_service import ipfs_service
from app.services.openai_service import openai_service

router = APIRouter()


@router.post("/transcribe", response_model=dict[str, Any])
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language: str | None = Form(None),
) -> Any:
    """Transcribe an audio file using Whisper API."""
    if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an audio file",
        )

    file_content = await audio_file.read()

    transcription = await openai_service.transcribe_audio(
        audio_file=(audio_file.filename, file_content), language=language
    )

    return {
        "transcription": transcription["text"],
        "language": transcription.get("language"),
        "duration": transcription.get("duration"),
        "filename": audio_file.filename,
    }


@router.post("/upload", response_model=dict[str, Any])
async def upload_audio_to_ipfs(
    audio_file: UploadFile = File(...),
    metadata: str | None = Form(None),
) -> Any:
    """Upload an audio file to IPFS."""
    if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an audio file",
        )

    file_content = await audio_file.read()

    metadata_dict = {}
    if metadata:
        import json

        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid metadata JSON",
            ) from e

    from io import BytesIO

    file_obj = BytesIO(file_content)

    ipfs_result = await ipfs_service.upload_file(
        file=file_obj,  # type: ignore[arg-type]
        filename=audio_file.filename or "audio.mp3",
        metadata=metadata_dict,
    )

    return {
        "cid": ipfs_result["cid"],
        "url": ipfs_result["url"],
        "size": ipfs_result["size"],
        "filename": audio_file.filename,
    }


@router.post(
    "/process", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED
)
async def process_audio_memory(
    audio_file: UploadFile = File(...),
    elder_id: int = Form(...),
    title: str | None = Form(None),
    language: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Process audio file: upload to IPFS, transcribe, enrich, and create memory."""
    if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an audio file",
        )

    file_content = await audio_file.read()

    from io import BytesIO

    file_obj = BytesIO(file_content)
    ipfs_result = await ipfs_service.upload_file(
        file=file_obj,  # type: ignore[arg-type]
        filename=audio_file.filename or "audio.mp3",
        metadata={"elder_id": elder_id, "title": title or "Untitled Memory"},
    )

    file_obj.seek(0)
    transcription = await openai_service.transcribe_audio(
        audio_file=(audio_file.filename, file_obj.read()), language=language
    )

    enrichment = await openai_service.enrich_memory(transcription["text"])

    memory = Memory(
        elder_id=elder_id,
        title=title or enrichment.get("summary", "Untitled Memory")[:200],
        transcription=transcription["text"],
        audio_cid=ipfs_result["cid"],
        audio_url=ipfs_result["url"],
        category=enrichment.get("category"),
        tags=enrichment.get("tags", []),
        emotional_tone=enrichment.get("emotional_tone"),
        time_period=enrichment.get("time_period"),
        people_mentioned=enrichment.get("people", []),
        locations_mentioned=enrichment.get("locations", []),
        ai_summary=enrichment.get("summary"),
        language=transcription.get("language") or language,
        duration_seconds=transcription.get("duration"),
        ai_analysis={
            "enrichment": enrichment,
            "transcription_metadata": {
                "segments": len(transcription.get("segments", [])),
                "language": transcription.get("language"),
            },
        },
    )

    db.add(memory)
    await db.commit()
    await db.refresh(memory)

    return memory  # type: ignore[return-value]


@router.get("/ipfs/{cid}")
async def get_ipfs_file_info(cid: str) -> Any:
    """Get information about a file stored on IPFS."""
    try:
        info = await ipfs_service.get_file_info(cid)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
