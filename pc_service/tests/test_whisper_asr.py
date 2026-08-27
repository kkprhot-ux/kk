"""Tests for the ASR provider abstraction + OpenAI Whisper implementation.

This file uses TDD: tests are written first, then implementation.
Run `pytest tests/test_whisper_asr.py -v` after creating asr_base.py
and whisper_asr.py."""
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx


def test_abstract_class_cannot_be_instantiated():
    """The base class should be abstract; instantiating it directly must fail."""
    from server.asr_base import AudioTranscriber
    with pytest.raises(TypeError):
        AudioTranscriber()


def test_whisper_asr_requires_api_key():
    """WhisperApiASR() with no key raises ValueError."""
    from server.whisper_asr import WhisperApiASR
    with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
        WhisperApiASR(api_key=None)


def test_whisper_asr_uses_env_var_by_default():
    """WhisperApiASR() reads OPENAI_API_KEY from env if no arg."""
    os.environ["OPENAI_API_KEY"] = "sk-test-123"
    try:
        from server.whisper_asr import WhisperApiASR
        c = WhisperApiASR()
        assert c.api_key == "sk-test-123"
        assert c.model == "whisper-1"  # default model
    finally:
        del os.environ["OPENAI_API_KEY"]


def test_whisper_asr_accepts_explicit_key_and_model():
    """WhisperApiASR(api_key=..., model=...) works."""
    from server.whisper_asr import WhisperApiASR
    c = WhisperApiASR(api_key="sk-abc", model="whisper-1")
    assert c.api_key == "sk-abc"
    assert c.model == "whisper-1"


@pytest.mark.asyncio
async def test_whisper_asr_recognize_sends_correct_multipart():
    """recognize() hits /audio/transcriptions with multipart form-data
    containing: file (audio bytes), model, language, response_format."""
    from server.whisper_asr import WhisperApiASR

    asr = WhisperApiASR(api_key="sk-test")

    captured = {}

    class FakeResponse:
        status_code = 200
        text = "{\"text\":\"你好世界\"}"

        def json(self):
            return {"text": "你好世界"}

    class FakeAsyncClient:
        def __init__(self, *a, **kw): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, files=None, data=None, headers=None):
            captured["url"] = url
            captured["files"] = files
            captured["data"] = data
            captured["headers"] = headers
            return FakeResponse()

    with patch("server.whisper_asr.httpx.AsyncClient", return_value=FakeAsyncClient()):
        result = await asr.recognize(b"\\x00\\x01\\x02PCM_DATA")

    assert captured["url"] == "https://api.openai.com/v1/audio/transcriptions"
    assert captured["headers"]["Authorization"] == "Bearer sk-test"
    # files is a dict like {"file": (filename, bytes, content_type)}
    assert "file" in captured["files"]
    fname, content, ctype = captured["files"]["file"]
    assert content == b"\\x00\\x01\\x02PCM_DATA"
    assert "audio" in ctype  # content_type contains "audio"
    assert captured["data"]["model"] == "whisper-1"
    assert captured["data"]["language"] == "zh"
    assert captured["data"]["response_format"] == "json"
    assert result == {"text": "你好世界", "confidence": 1.0}


@pytest.mark.asyncio
async def test_whisper_asr_returns_only_text_for_empty_optionals():
    """Without language/response_format kwargs, defaults are used."""
    from server.whisper_asr import WhisperApiASR

    asr = WhisperApiASR(api_key="sk-test")

    captured = {}

    class FakeResp:
        status_code = 200
        text = "{\"text\":\"hi\"}"
        def json(self): return {"text": "hi"}

    class FakeClient:
        def __init__(self, *a, **kw): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, files=None, data=None, headers=None):
            captured.update({"url": url, "files": files, "data": data, "headers": headers})
            return FakeResp()

    with patch("server.whisper_asr.httpx.AsyncClient", return_value=FakeClient()):
        result = await asr.recognize(b"x")

    assert captured["data"]["model"] == "whisper-1"
    assert captured["data"]["language"] == "zh"
    assert result == {"text": "hi", "confidence": 1.0}


@pytest.mark.asyncio
async def test_whisper_asr_raises_on_http_error():
    """If OpenAI returns non-200, raise RuntimeError with status + body."""
    from server.whisper_asr import WhisperApiASR

    asr = WhisperApiASR(api_key="sk-test")

    class FakeResp:
        status_code = 401
        text = "{\"error\":{\"message\":\"Incorrect API key\"}}"
        def json(self): return {"error": {"message": "Incorrect API key"}}

    class FakeClient:
        def __init__(self, *a, **kw): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, files=None, data=None, headers=None):
            return FakeResp()

    with patch("server.whisper_asr.httpx.AsyncClient", return_value=FakeClient()):
        with pytest.raises(RuntimeError, match="401"):
            await asr.recognize(b"x")


def test_pipeline_uses_transcriber_interface():
    """The SuggestionPipeline should accept any AudioTranscriber, not hardcode Xunfei."""
    from server.asr_base import AudioTranscriber
    from server.asr_service import XunfeiASR  # ensure old one still exists
    from server.whisper_asr import WhisperApiASR

    # XunfeiASR must satisfy the protocol
    x = XunfeiASR(app_id="x", api_key="k", api_secret="s")
    assert isinstance(x, AudioTranscriber)

    # WhisperApiASR also must
    w = WhisperApiASR(api_key="sk-test")
    assert isinstance(w, AudioTranscriber)



@pytest.mark.asyncio
async def test_whisper_asr_empty_audio_returns_skip():
    """recognize() with empty bytes returns {text:'', skip:True} without any HTTP call."""
    from server.whisper_asr import WhisperApiASR
    asr = WhisperApiASR(api_key="sk-test")
    with patch("server.whisper_asr.httpx.AsyncClient") as MockClient:
        result = await asr.recognize(b"")
        assert result == {"text": "", "skip": True}
        MockClient.assert_not_called()
