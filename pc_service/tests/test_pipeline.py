import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Force an env var so SuggestionPipeline.__init__ can construct
# DeepSeekClient (which requires DEEPSEEK_API_KEY).
os.environ.setdefault("DEEPSEEK_API_KEY", "test-key")

from analyzer.suggestion import SuggestionPipeline


@pytest.mark.asyncio
async def test_pipeline_processes_audio_to_suggestion():
    """process_audio: ASR returns text -> LLM returns dict -> merged result."""
    pipeline = SuggestionPipeline.__new__(SuggestionPipeline)
    pipeline.asr = MagicMock()
    pipeline.asr.recognize = AsyncMock(
        return_value={"text": "you are too expensive", "confidence": 0.9}
    )
    pipeline.llm = MagicMock()
    pipeline.llm.generate_suggestion = AsyncMock(
        return_value={
            "scenario": "price_negotiation",
            "recommended_script": "I understand your concern",
        }
    )
    result = await pipeline.process_audio(b"fake_audio")
    assert result["customer_text"] == "you are too expensive"
    assert result["scenario"] == "price_negotiation"
    assert result["recommended_script"] == "I understand your concern"


@pytest.mark.asyncio
async def test_pipeline_skips_empty_text():
    """If ASR returns empty/whitespace text, process_audio returns skip=True
    and does NOT call the LLM."""
    pipeline = SuggestionPipeline.__new__(SuggestionPipeline)
    pipeline.asr = MagicMock()
    pipeline.asr.recognize = AsyncMock(
        return_value={"text": "   ", "confidence": 0.5}
    )
    pipeline.llm = MagicMock()
    pipeline.llm.generate_suggestion = AsyncMock(return_value={})  # should not be called
    result = await pipeline.process_audio(b"silence_chunk")
    assert result == {"customer_text": "", "skip": True}
    pipeline.llm.generate_suggestion.assert_not_called()


@pytest.mark.asyncio
async def test_pipeline_passes_history_and_context_to_llm():
    """process_audio forwards history + context to the LLM call."""
    pipeline = SuggestionPipeline.__new__(SuggestionPipeline)
    pipeline.asr = MagicMock()
    pipeline.asr.recognize = AsyncMock(
        return_value={"text": "ok", "confidence": 0.9}
    )
    pipeline.llm = MagicMock()
    pipeline.llm.generate_suggestion = AsyncMock(return_value={"scenario": "ok"})
    history = [{"role": "customer", "text": "hi"}]
    context = {"scenario": "demo"}
    await pipeline.process_audio(
        b"audio", history=history, context=context
    )
    pipeline.llm.generate_suggestion.assert_called_once()
    kwargs = pipeline.llm.generate_suggestion.call_args.kwargs
    assert kwargs["customer_text"] == "ok"
    assert kwargs["history"] == history
    assert kwargs["context"] == context


def test_pipeline_init_constructs_clients():
    """__init__ creates an XunfeiASR (with env-driven creds) and a
    DeepSeekClient (with DEEPSEEK_API_KEY)."""
    os.environ["XUNFEI_APP_ID"] = "test_app"
    os.environ["XUNFEI_API_KEY"] = "test_key"
    os.environ["XUNFEI_API_SECRET"] = "test_secret"
    pipeline = SuggestionPipeline()
    assert pipeline.asr is not None
    assert pipeline.asr.app_id == "test_app"
    assert pipeline.llm is not None
    assert pipeline.llm.api_key == "test-key"
