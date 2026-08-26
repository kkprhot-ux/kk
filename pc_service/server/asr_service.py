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
        ts = str(int(time.time()))
        tt = (self.app_id + ts).encode('utf-8')
        md5 = hashlib.md5(tt).hexdigest()
        signature = base64.b64encode(
            hmac.new(self.api_secret.encode('utf-8'),
                    (self.app_id + ts + md5).encode('utf-8'),
                    digestmod=hashlib.sha256).digest()
        ).decode('utf-8')
        params = {"app_id": self.app_id, "ts": ts, "signa": signature}
        return f"{self.WS_URL}?{urlencode(params)}"

    async def _send_audio(self, ws, audio_chunk: bytes):
        start_frame = {
            "common": {"app_id": self.app_id},
            "business": {"language": "zh", "domain": "iat"},
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
        result = await ws.recv()
        return json.loads(result)

    async def recognize(self, audio_chunk: bytes) -> dict:
        url = self._generate_auth_url()
        async with websockets.connect(url) as ws:
            response = await self._send_audio(ws, audio_chunk)
            text = self._extract_text(response)
            return {"text": text, "confidence": 0.9}

    def _extract_text(self, response: dict) -> str:
        try:
            ws = response.get("data", {}).get("result", {}).get("ws", [])
            return "".join(w.get("cw", [{}])[0].get("w", "") for w in ws)
        except (KeyError, IndexError):
            return ""