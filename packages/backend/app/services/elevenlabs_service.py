"""ElevenLabs voice cloning and text-to-speech service."""

import io
from typing import Any, BinaryIO, Optional, Sequence, Union

import httpx

from app.core.config import settings


class ElevenLabsService:
    """Service for ElevenLabs voice cloning and TTS."""

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self) -> None:
        """Initialize ElevenLabs service."""
        self.api_key = settings.ELEVENLABS_API_KEY
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def create_voice_clone(
        self,
        name: str,
        audio_files: Sequence[tuple[str, Union[BinaryIO, io.BytesIO]]],
        description: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Create a voice clone from audio samples.

        Args:
            name: Name for the voice
            audio_files: List of tuples (filename, file_object) for voice samples
                        Minimum 1 minute of clear audio, 3-5 samples recommended
            description: Optional description of the voice
            labels: Optional metadata labels for the voice

        Returns:
            dict with voice_id and other voice details
        """
        url = f"{self.BASE_URL}/voices/add"

        files_data = []
        for filename, file_obj in audio_files:
            files_data.append(("files", (filename, file_obj, "audio/mpeg")))

        data: dict[str, Any] = {"name": name}
        if description:
            data["description"] = description
        if labels:
            data["labels"] = labels

        headers: dict[str, str] = {"xi-api-key": self.api_key}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url, headers=headers, data=data, files=files_data
            )
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return result

    async def get_voice(self, voice_id: str) -> dict[str, Any]:
        """Get voice details by ID."""
        url = f"{self.BASE_URL}/voices/{voice_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return result

    async def list_voices(self) -> list[dict[str, Any]]:
        """List all available voices."""
        url = f"{self.BASE_URL}/voices"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            voices: list[dict[str, Any]] = data.get("voices", [])
            return voices

    async def delete_voice(self, voice_id: str) -> dict[str, Any]:
        """Delete a voice by ID."""
        url = f"{self.BASE_URL}/voices/{voice_id}"

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=self.headers)
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return result

    async def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        voice_settings: Optional[dict[str, float]] = None,
        output_format: str = "mp3_44100_128",
    ) -> bytes:
        """
        Convert text to speech using a voice.

        Args:
            text: Text to convert to speech
            voice_id: ID of the voice to use
            model_id: ElevenLabs model ID (default: eleven_multilingual_v2)
            voice_settings: Optional voice settings (stability, similarity_boost, style, use_speaker_boost)
            output_format: Audio output format

        Returns:
            Audio data as bytes
        """
        url = f"{self.BASE_URL}/text-to-speech/{voice_id}"

        default_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        }

        if voice_settings:
            default_settings.update(voice_settings)

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": default_settings,
        }

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": f"audio/{output_format.split('_')[0]}",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.content

    async def text_to_speech_stream(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        voice_settings: Optional[dict[str, float]] = None,
    ) -> httpx.Response:
        """
        Stream text-to-speech audio.

        Args:
            text: Text to convert to speech
            voice_id: ID of the voice to use
            model_id: ElevenLabs model ID
            voice_settings: Optional voice settings

        Returns:
            Streaming response
        """
        url = f"{self.BASE_URL}/text-to-speech/{voice_id}/stream"

        default_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        }

        if voice_settings:
            default_settings.update(voice_settings)

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": default_settings,
        }

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        client = httpx.AsyncClient(timeout=60.0)
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response

    async def get_voice_settings(self, voice_id: str) -> dict[str, Any]:
        """Get current settings for a voice."""
        url = f"{self.BASE_URL}/voices/{voice_id}/settings"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return result

    async def update_voice_settings(
        self, voice_id: str, settings: dict[str, float]
    ) -> dict[str, Any]:
        """Update settings for a voice."""
        url = f"{self.BASE_URL}/voices/{voice_id}/settings/edit"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=settings)
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            return result

    async def get_available_models(self) -> list[dict[str, Any]]:
        """Get list of available ElevenLabs models."""
        url = f"{self.BASE_URL}/models"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            result: list[dict[str, Any]] = response.json()
            return result

    async def check_voice_quality(
        self, audio_files: Sequence[tuple[str, Union[BinaryIO, io.BytesIO]]]
    ) -> dict[str, Any]:
        """
        Check quality of audio samples before voice cloning.

        Returns quality assessment and recommendations.
        """
        total_duration = 0.0
        quality_issues = []

        if len(audio_files) < 1:
            quality_issues.append("At least 1 audio sample is required")

        if len(audio_files) < 3:
            quality_issues.append("For best results, provide 3-5 diverse audio samples")

        return {
            "is_ready": len(quality_issues) == 0,
            "total_samples": len(audio_files),
            "total_duration_seconds": total_duration,
            "quality_issues": quality_issues,
            "recommendations": [
                "Use clear, high-quality recordings",
                "Include varied emotional expressions",
                "Avoid background noise",
                "Aim for 1-5 minutes total duration",
                "Use consistent recording quality",
            ],
        }


elevenlabs_service = ElevenLabsService()
