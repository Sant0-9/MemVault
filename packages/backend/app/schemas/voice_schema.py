"""Voice cloning and TTS schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class VoiceCloneCreate(BaseModel):
    """Request schema for voice cloning."""

    name: str = Field(..., description="Name for the voice")
    description: Optional[str] = Field(None, description="Optional voice description")


class VoiceCloneResponse(BaseModel):
    """Response schema for voice cloning."""

    success: bool
    message: str
    voice_id: Optional[str] = None
    voice_name: Optional[str] = None
    quality_issues: Optional[list[str]] = None
    recommendations: Optional[list[str]] = None


class VoiceListResponse(BaseModel):
    """Response schema for listing voices."""

    voices: list[dict]


class VoiceTTSRequest(BaseModel):
    """Request schema for text-to-speech."""

    elder_id: int = Field(..., description="ID of the elder whose voice to use")
    text: str = Field(..., description="Text to convert to speech", min_length=1)
    model_id: Optional[str] = Field(
        "eleven_multilingual_v2", description="ElevenLabs model ID"
    )
    voice_settings: Optional[dict[str, float]] = Field(
        None,
        description="Voice settings (stability, similarity_boost, style, use_speaker_boost)",
    )


class VoiceSettingsUpdate(BaseModel):
    """Schema for updating voice settings."""

    stability: Optional[float] = Field(None, ge=0.0, le=1.0)
    similarity_boost: Optional[float] = Field(None, ge=0.0, le=1.0)
    style: Optional[float] = Field(None, ge=0.0, le=1.0)
    use_speaker_boost: Optional[bool] = None
