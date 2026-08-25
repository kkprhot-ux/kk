import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from analyzer.suggestion import SuggestionPipeline

@pytest.mark.asyncio
async def test_pipeline_processes_audio_to_suggestion():
    pipeline = SuggestionPipeline.__new__(SuggestionPipeline)
    pipeline.asr = MagicMock()
    pipeline.asr.recognize = AsyncMock(return_value={"text": "你们太贵了", "confidence": 0.9})
    pipeline.llm = MagicMock()
    pipeline.llm.generate_suggestion = AsyncMock(return_value={
        "scenario": "价格谈判",
        "recommended_script": "理解您的考虑",
    })
    result = await pipeline.process_audio(b"fake_audio")
    assert result["customer_text"] == "你们太贵了"
    assert result["scenario"] == "价格谈判"