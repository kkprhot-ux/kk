import json
import base64
import hashlib
import hmac
import time
import logging
from urllib.parse import urlencode
import websockets

logger = logging.getLogger(__name__)

class XunfeiASR:
    """讯飞流式 ASR 封装（基于 WebSocket）"""

    WS_URL = "wss://rtasr.xfyun.cn/v1/ws"

    def __init__(self, app_id: str, api_key: str, api_secret: str):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret

    def _generate_auth_url(self) -> str:
        # Xunfei RTAS signa algorithm:
        #   md5 = md5(appid + ts)
        #   signa = base64(hmac-sha256(APIKey, appid + ts + md5))
        # NOTE: the HMAC key is the APIKey, NOT the APISecret.
        # Verified by trial: signa-with-secret returns 10106 "empty appid".
        ts = str(int(time.time()))
        tt = (self.app_id + ts).encode('utf-8')
        md5 = hashlib.md5(tt).hexdigest()
        signature = base64.b64encode(
            hmac.new(self.api_key.encode('utf-8'),
                    (self.app_id + ts + md5).encode('utf-8'),
                    digestmod=hashlib.sha256).digest()
        ).decode('utf-8')
        params = {"appid": self.app_id, "ts": ts, "signa": signature}  # Xunfei uses 'appid' (no underscore)
        return f"{self.WS_URL}?{urlencode(params)}"

    async def _send_audio(self, ws, audio_chunk: bytes):
        start_frame = {
            "common": {"appid": self.app_id},
            "business": {
                "language": "zh",
                "domain": "iat",
                "transType": "normal",  # required by Xunfei; missing -> 10110
            },
            "data": {"status": 0, "format": "audio/L16;rate=16000"}
        }
        await ws.send(json.dumps(start_frame))
        audio_frame = {
            "data": {
                "status": 1,
                "format": "audio/L16;rate=16000",
                "audio": base64.b64encode(audio_chunk).decode('utf-8'),
                "encoding": "raw"
            }
        }
        await ws.send(json.dumps(audio_frame))
        # Xunfei protocol: server first sends a 'started' string frame,
        # then a 'result' or 'error' dict frame. Loop until we see a dict.
        while True:
            raw = await ws.recv()
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed

    async def recognize(self, audio_chunk: bytes) -> dict:
        url = self._generate_auth_url()
        async with websockets.connect(url) as ws:
            response = await self._send_audio(ws, audio_chunk)
        if isinstance(response, dict) and response.get("action") == "error":
            code = response.get("code", "")
            desc = response.get("desc", "")
            raise RuntimeError(f"Xunfei ASR error {code}: {desc}")
        text = self._extract_text(response)
        return {"text": text, "confidence": 0.9}

    def _extract_text(self, response: dict) -> str:
        try:
            ws = response.get("data", {}).get("result", {}).get("ws", [])
            return "".join(w.get("cw", [{}])[0].get("w", "") for w in ws)
        except (KeyError, IndexError):
            return ""