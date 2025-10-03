"""Voice cloning and text-to-speech endpoints."""

from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models.elder import Elder
from app.schemas.voice_schema import (
    VoiceCloneCreate,
    VoiceCloneResponse,
    VoiceListResponse,
    VoiceSettingsUpdate,
    VoiceTTSRequest,
)
from app.services.elevenlabs_service import elevenlabs_service

router = APIRouter()


@router.post("/elders/{elder_id}/voice/clone", response_model=VoiceCloneResponse)
async def clone_voice(
    elder_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    audio_files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
) -> VoiceCloneResponse:
    """
    Create a voice clone for an elder from audio samples.

    Requirements:
    - Minimum 1 minute of clear audio
    - 3-5 samples recommended for best quality
    - Clear speech without background noise
    """
    result = await db.execute(Elder.__table__.select().where(Elder.id == elder_id))
    elder = result.scalars().first()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elder with id {elder_id} not found",
        )

    if len(audio_files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one audio file is required",
        )

    max_files = 10
    if len(audio_files) > max_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {max_files} audio files allowed",
        )

    try:
        files_data = []
        for upload_file in audio_files:
            file_content = await upload_file.read()
            import io

            file_obj = io.BytesIO(file_content)
            files_data.append((upload_file.filename or "audio.mp3", file_obj))

        quality_check = await elevenlabs_service.check_voice_quality(files_data)
        if not quality_check["is_ready"]:
            return VoiceCloneResponse(
                success=False,
                message="Voice quality check failed",
                quality_issues=quality_check["quality_issues"],
                recommendations=quality_check["recommendations"],
            )

        labels = {"elder_id": str(elder_id), "source": "memvault"}

        voice_data = await elevenlabs_service.create_voice_clone(
            name=name or elder.name,
            audio_files=files_data,
            description=description,
            labels=labels,
        )

        elder.voice_profile_id = voice_data["voice_id"]
        elder.sample_audios = {
            "filenames": [f.filename for f in audio_files],
            "created_at": str(Elder.created_at),
        }
        await db.commit()

        return VoiceCloneResponse(
            success=True,
            message="Voice cloned successfully",
            voice_id=voice_data["voice_id"],
            voice_name=name or elder.name,
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clone voice: {str(e)}",
        ) from e


@router.get("/elders/{elder_id}/voice", response_model=dict[str, Any])
async def get_elder_voice(
    elder_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get voice profile for an elder."""
    result = await db.execute(Elder.__table__.select().where(Elder.id == elder_id))
    elder = result.scalars().first()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elder with id {elder_id} not found",
        )

    if not elder.voice_profile_id:
        return {
            "has_voice": False,
            "message": "No voice profile found for this elder",
        }

    try:
        voice_data = await elevenlabs_service.get_voice(elder.voice_profile_id)
        return {
            "has_voice": True,
            "voice_id": elder.voice_profile_id,
            "voice_name": voice_data.get("name"),
            "voice_category": voice_data.get("category"),
            "sample_audios": elder.sample_audios,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch voice: {str(e)}",
        ) from e


@router.delete("/elders/{elder_id}/voice")
async def delete_elder_voice(
    elder_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Delete voice profile for an elder."""
    result = await db.execute(Elder.__table__.select().where(Elder.id == elder_id))
    elder = result.scalars().first()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elder with id {elder_id} not found",
        )

    if not elder.voice_profile_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No voice profile found for this elder",
        )

    try:
        await elevenlabs_service.delete_voice(elder.voice_profile_id)

        elder.voice_profile_id = None
        elder.sample_audios = None
        await db.commit()

        return {"message": "Voice profile deleted successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete voice: {str(e)}",
        ) from e


@router.post("/voice/text-to-speech")
async def text_to_speech(
    request: VoiceTTSRequest,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """
    Convert text to speech using an elder's voice.

    Returns streaming audio response.
    """
    result = await db.execute(
        Elder.__table__.select().where(Elder.id == request.elder_id)
    )
    elder = result.scalars().first()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elder with id {request.elder_id} not found",
        )

    if not elder.voice_profile_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No voice profile found for this elder. Please create one first.",
        )

    try:
        audio_data = await elevenlabs_service.text_to_speech(
            text=request.text,
            voice_id=elder.voice_profile_id,
            model_id=request.model_id or "eleven_multilingual_v2",
            voice_settings=request.voice_settings,
        )

        import io

        audio_stream = io.BytesIO(audio_data)

        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="tts_{elder.name}.mp3"'
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate speech: {str(e)}",
        ) from e


@router.get("/voice/settings/{voice_id}")
async def get_voice_settings(voice_id: str) -> dict[str, Any]:
    """Get voice settings."""
    try:
        settings = await elevenlabs_service.get_voice_settings(voice_id)
        return settings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get voice settings: {str(e)}",
        ) from e


@router.put("/voice/settings/{voice_id}")
async def update_voice_settings(
    voice_id: str, settings: VoiceSettingsUpdate
) -> dict[str, Any]:
    """Update voice settings."""
    try:
        updated_settings = await elevenlabs_service.update_voice_settings(
            voice_id, settings.model_dump(exclude_none=True)
        )
        return updated_settings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update voice settings: {str(e)}",
        ) from e


@router.get("/voice/models")
async def get_available_models() -> list[dict[str, Any]]:
    """Get list of available ElevenLabs models."""
    try:
        models = await elevenlabs_service.get_available_models()
        return models
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch models: {str(e)}",
        ) from e
