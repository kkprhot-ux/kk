"""Abstract base class for ASR providers.

The SuggestionPipeline depends on this interface, not on any concrete
provider. New providers (Whisper, local faster-whisper, Azure, etc.)
just need to subclass AudioTranscriber and implement recognize()."""
from abc import ABC, abstractmethod


class AudioTranscriber(ABC):
    """Abstract interface for any speech-to-text provider.

    Concrete providers (Xunfei, Whisper, etc.) must implement recognize().
    The pipeline accepts any AudioTranscriber and does not care which
    cloud / API the bytes go to."""

    @abstractmethod
    async def recognize(self, audio_chunk: bytes) -> dict:
        """Transcribe a chunk of 16 kHz mono PCM audio.

        Returns:
            {"text": "<recognized text>", "confidence": <float 0-1>}

        Implementations should:
        - Skip silently or return {"text": "", "skip": True} if audio is empty.
        - Raise RuntimeError with provider code + description on hard errors.
        """
