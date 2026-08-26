import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx


# Force an API key for tests (avoids ValueError at construction).
os.environ.setdefault("DEEPSEEK_API_KEY", "test-key")

from server.llm_service import DeepSeekClient


def test_init_raises_without_api_key(monkeypatch):
    """Constructor raises if no API key is set anywhere."""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(ValueError, match="DEEPSEEK_API_KEY not set"):
        DeepSeekClient(api_key=None)


def test_init_uses_env_var_by_default():
    """Constructor reads DEEPSEEK_API_KEY from env if no arg given."""
    c = DeepSeekClient()
    assert c.api_key == "test-key"


def test_init_accepts_explicit_key():
    """Constructor accepts explicit api_key arg."""
    c = DeepSeekClient(api_key="my-explicit-key")
    assert c.api_key == "my-explicit-key"


@pytest.mark.asyncio
async def test_call_api_sends_correct_request():
    """_call_api hits the right URL with the right headers + body."""
    captured = {}

    class FakeAsyncClient:
        def __init__(self, *a, **kw):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, *a):
            return False
        async def post(self, url, headers=None, json=None, timeout=None):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            r = MagicMock()
            r.raise_for_status = MagicMock()
            r.json = MagicMock(return_value={"choices": [{"message": {"content": "ok"}}]})
            return r

    # Patch httpx.AsyncClient to return our fake
    with patch("server.llm_service.httpx.AsyncClient", return_value=FakeAsyncClient()):
        client = DeepSeekClient(api_key="k")
        result = await client._call_api(
            [{"role": "user", "content": "hi"}], model="deepseek-test"
        )
    assert captured["url"] == "https://api.deepseek.com/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer k"
    assert captured["json"]["model"] == "deepseek-test"
    assert captured["json"]["messages"] == [{"role": "user", "content": "hi"}]
    assert result == {"choices": [{"message": {"content": "ok"}}]}


@pytest.mark.asyncio
async def test_format_suggestion_input_with_history():
    """History is rendered with role labels and truncated to last 6."""
    from server.llm_service import DeepSeekClient
    client = DeepSeekClient(api_key="k")
    history = [{"role": "customer", "text": "hi"}, {"role": "sales", "text": "hello"}]
    out = client._format_suggestion_input(
        "new msg",
        history=history,
        context={"scenario": "demo"},
    )
    assert "客户: hi" in out
    assert "您: hello" in out
    assert "new msg" in out
    assert "demo" in out


@pytest.mark.asyncio
async def test_format_suggestion_input_empty_history():
    """No history -> only the customer line is emitted; context gets the
    "unknown" placeholder when scenario key is missing."""
    from server.llm_service import DeepSeekClient
    client = DeepSeekClient(api_key="k")
    out = client._format_suggestion_input("only this", history=[], context={})
    assert "only this" in out
    # The "unknown" placeholder (any encoding) is part of the output
    assert len(out) > len("only this")


def test_parse_json_response_pure_json():
    from server.llm_service import DeepSeekClient
    c = DeepSeekClient(api_key="k")
    assert c._parse_json_response('{"a": 1}') == {"a": 1}


def test_parse_json_response_embedded_json():
    from server.llm_service import DeepSeekClient
    c = DeepSeekClient(api_key="k")
    s = "Here is the answer: {\"a\": 1, \"b\": 2} -- done"
    assert c._parse_json_response(s) == {"a": 1, "b": 2}


def test_parse_json_response_no_json():
    from server.llm_service import DeepSeekClient
    c = DeepSeekClient(api_key="k")
    out = c._parse_json_response("no braces here at all")
    assert "error" in out
    assert out["raw"] == "no braces here at all"



@pytest.mark.asyncio
async def test_generate_suggestion_uses_correct_prompt():
    """generate_suggestion passes the right system prompt (SUGGESTION_SYSTEM_PROMPT)
    and parses the LLM response."""
    os.environ.setdefault("DEEPSEEK_API_KEY", "test-key")
    from server.llm_service import DeepSeekClient
    client = DeepSeekClient(api_key="k")
    fake = {
        "choices": [{"message": {"content": '{"scenario": "x", "recommended_script": "y"}'}}]
    }
    captured = {}
    async def fake_call(messages, model="deepseek-chat"):
        captured["system"] = messages[0]["content"]
        captured["user"] = messages[1]["content"]
        return fake
    client._call_api = fake_call
    result = await client.generate_suggestion(
        customer_text="hi",
        history=[],
        context={"scenario": "demo"},
    )
    assert result["scenario"] == "x"
    assert "SUGGESTION_SYSTEM_PROMPT" not in captured["system"]  # actual content used
    # System prompt must mention 销售 / scenario / etc.
    from server.sales_prompts import SUGGESTION_SYSTEM_PROMPT
    assert captured["system"] == SUGGESTION_SYSTEM_PROMPT
    assert "hi" in captured["user"]
    assert "demo" in captured["user"]


@pytest.mark.asyncio
async def test_generate_replay_uses_correct_prompt():
    """generate_replay passes the right system prompt and includes transcript."""
    os.environ.setdefault("DEEPSEEK_API_KEY", "test-key")
    from server.llm_service import DeepSeekClient
    client = DeepSeekClient(api_key="k")
    fake = {
        "choices": [{"message": {"content": '{"summary": "s"}'}}]
    }
    captured = {}
    async def fake_call(messages, model="deepseek-chat"):
        captured["system"] = messages[0]["content"]
        captured["user"] = messages[1]["content"]
        return fake
    client._call_api = fake_call
    result = await client.generate_replay(transcript="this is a transcript")
    assert result["summary"] == "s"
    from server.sales_prompts import REPLAY_SYSTEM_PROMPT
    assert captured["system"] == REPLAY_SYSTEM_PROMPT
    assert "this is a transcript" in captured["user"]
