import pytest
from unittest.mock import patch
from server.asr_service import XunfeiASR

@pytest.mark.asyncio
async def test_asr_returns_text():
    asr = XunfeiASR(app_id="test", api_key="test", api_secret="test")
    with patch.object(asr, '_send_audio', return_value={
        "data": {"result": {"ws": [{"cw": [{"w": "你"}]}, {"cw": [{"w": "好"}]}]}}
    }):
        result = await asr.recognize(b"fake_audio")
        assert result["text"] == "你好"