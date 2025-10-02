"""OpenAI service for AI conversations and transcription."""

from typing import Any, AsyncGenerator, Optional

from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIService:
    """Service for interacting with OpenAI APIs."""

    def __init__(self) -> None:
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def create_interview_prompt(
        self, elder_name: str, conversation_history: list[dict[str, str]]
    ) -> str:
        """Create a system prompt for the AI interviewer."""
        return f"""You are an empathetic AI interviewer helping to preserve {elder_name}'s life stories and memories.

Your role is to:
- Ask thoughtful, open-ended questions about their life experiences
- Listen actively and show genuine interest
- Follow up on interesting details they mention
- Help them remember and articulate precious memories
- Be patient, warm, and respectful
- Adapt your questions based on their responses
- Guide them through different life periods (childhood, youth, career, family, etc.)

Keep your questions conversational and natural. Make them feel comfortable sharing their stories.

Previous conversation:
{self._format_conversation_history(conversation_history)}

Based on the conversation so far, ask your next thoughtful question."""

    def _format_conversation_history(
        self, conversation_history: list[dict[str, str]]
    ) -> str:
        """Format conversation history for the prompt."""
        if not conversation_history:
            return "This is the beginning of the conversation."

        formatted = []
        for turn in conversation_history[-10:]:
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            formatted.append(f"{role.capitalize()}: {content}")

        return "\n".join(formatted)

    async def generate_interview_question(
        self,
        elder_name: str,
        conversation_history: list[dict[str, str]],
        topic: Optional[str] = None,
    ) -> str:
        """Generate the next interview question based on conversation history."""
        system_prompt = await self.create_interview_prompt(
            elder_name, conversation_history
        )

        messages = [{"role": "system", "content": system_prompt}]

        if topic:
            messages.append(
                {
                    "role": "user",
                    "content": f"Focus the next question on: {topic}",
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": "What should I ask next?",
                }
            )

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,  # type: ignore[arg-type]
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=200,
        )

        return response.choices[0].message.content or ""

    async def generate_interview_question_stream(
        self,
        elder_name: str,
        conversation_history: list[dict[str, str]],
        topic: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream the interview question generation."""
        system_prompt = await self.create_interview_prompt(
            elder_name, conversation_history
        )

        messages = [{"role": "system", "content": system_prompt}]

        if topic:
            messages.append(
                {
                    "role": "user",
                    "content": f"Focus the next question on: {topic}",
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": "What should I ask next?",
                }
            )

        stream = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,  # type: ignore[arg-type]
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=200,
            stream=True,
        )

        async for chunk in stream:  # type: ignore[union-attr]
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def transcribe_audio(
        self, audio_file: Any, language: Optional[str] = None
    ) -> dict[str, Any]:
        """Transcribe audio file using Whisper API."""
        params: dict[str, Any] = {
            "file": audio_file,
            "model": settings.WHISPER_MODEL,
            "response_format": "verbose_json",
        }

        if language:
            params["language"] = language

        response = await self.client.audio.transcriptions.create(**params)

        return {
            "text": response.text,
            "language": getattr(response, "language", language),
            "duration": getattr(response, "duration", None),
            "segments": getattr(response, "segments", []),
        }

    async def enrich_memory(
        self, transcription: str, existing_tags: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Enrich a memory with AI-generated metadata."""
        prompt = f"""Analyze this memory transcript and provide enrichment data:

Transcript: "{transcription}"

Provide:
1. Category (choose one: childhood, education, career, family, relationships, travel, achievement, challenge, tradition, wisdom)
2. 3-5 relevant tags
3. Emotional tone (choose one: joyful, nostalgic, reflective, proud, bittersweet, humorous, serious, sad)
4. Time period estimate (e.g., "1950s", "early 1970s", "childhood")
5. Key people mentioned
6. Key locations mentioned
7. Brief summary (1-2 sentences)

Respond in JSON format with these exact keys: category, tags, emotional_tone, time_period, people, locations, summary"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a memory analysis assistant. Always respond with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        import json

        enrichment_data: dict[str, Any] = json.loads(
            response.choices[0].message.content or "{}"
        )

        if existing_tags:
            enrichment_data["tags"] = list(
                set(enrichment_data.get("tags", []) + existing_tags)
            )

        return enrichment_data


openai_service = OpenAIService()
