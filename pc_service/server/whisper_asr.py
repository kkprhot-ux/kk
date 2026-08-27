"""OpenAI Whisper API provider.

Docs: https://platform.openai.com/docs/api-reference/audio/createTranscription
Endpoint: POST https://api.openai.com/v1/audio/transcriptions
Auth: Bearer token in Authorization header
Body: multipart/form-data with file (audio bytes), model, language, response_format
Cost: $0.006 / minute of audio (as of 2026).

This provider satisfies the AudioTranscriber interface and can be used as
a drop-in replacement for XunfeiASR in the SuggestionPipeline."""
import os
import logging

import httpx

from server.asr_base import AudioTranscriber

logger = logging.getLogger(__name__)


class WhisperApiASR(AudioTranscriber):
    """OpenAI Whisper ASR (https://api.openai.com/v1/audio/transcriptions)."""

    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    DEFAULT_MODEL = "whisper-1"
    DEFAULT_LANGUAGE = "zh"

    def __init__(
        self,
        api_key: str = None,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        language: str = DEFAULT_LANGUAGE,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.language = language

    async def recognize(self, audio_chunk: bytes) -> dict:
        """Transcribe a PCM audio chunk via OpenAI Whisper.

        Returns {"text": "...", "confidence": 1.0}.
        Whisper's response_format=json does not include a confidence
        score; we set confidence to 1.0 as a placeholder.
        """
        if not audio_chunk:
            return {"text": "", "skip": True}

        url = f"{self.base_url}/audio/transcriptions"
        files = {
            "file": (
                "audio.pcm",
                audio_chunk,
                "audio/L16;rate=16000",
            ),
        }
        data = {
            "model": self.model,
            "language": self.language,
            "response_format": "json",
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url, files=files, data=data, headers=headers
            )
        if response.status_code != 200:
            raise RuntimeError(
                f"OpenAI Whisper error {response.status_code}: {response.text[:300]}"
            )
        body = response.json()
        return {"text": body.get("text", ""), "confidence": 1.0}
