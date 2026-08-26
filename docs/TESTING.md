# Manual Testing Guide - Real-time Sales Assistant App

## Stage 0: Automated Smoke Test (run anytime, no API key needed)

```powershell
cd pc_service
pytest tests/test_smoke.py -v
```

Expected: all 8 tests PASS. Verifies:
- WebSocket server starts
- Call records persist to DB
- /calls history API works
- BackupManager can create archives
- All modules import cleanly
- Sales prompts have required JSON fields
- Database has all 4 tables

## Stage 1: PC Backend Real Run (requires API keys)

### Get credentials

1. **DeepSeek API key** - https://platform.deepseek.com
   - Register, top up (min 1 CNY)
   - Create an API key

2. **Xunfei ASR credentials** - https://www.xfyun.cn
   - Register, real-name verify
   - Create app: select "Real-time Speech Transcription"
   - Get APPID / APIKey / APISecret

### Configure

```powershell
cd pc_service
copy .env.example .env
# Edit .env, fill in 4 values:
# DEEPSEEK_API_KEY=sk-...
# XUNFEI_APP_ID=...
# XUNFEI_API_KEY=...
# XUNFEI_API_SECRET=...
```

### Run

```powershell
python main.py
```

Expected output:
```
Uvicorn running on http://0.0.0.0:8765
Database initialized at D:\PersonalAssistant\data\assistant.db
```

### Verify

Open browser to `http://localhost:8765/health`:
```json
{"db_connected": true, "status": "ok"}
```

### Test DeepSeek

```powershell
python -c "
import asyncio
from server.llm_service import DeepSeekClient

async def main():
    client = DeepSeekClient()
    result = await client.generate_suggestion(
        customer_text='Your product is too expensive',
        history=[],
        context={'scenario': 'cold_call'}
    )
    print('LLM Response:', result)

asyncio.run(main())
"
```

Expected: JSON with `scenario`, `recommended_script`, etc.

## Stage 2: Phone Connects to PC (requires Android device)

### Prep

1. Android device (Xiaomi 8 Lite)
2. Android Studio (for building APK)
3. USB cable
4. Phone: enable Developer Mode + USB Debugging

### Find PC IP

```powershell
ipconfig
# Find IPv4 Address, e.g. 192.168.1.100
```

### Set Phone App

1. Open `phone_app` in Android Studio
2. Wait for Gradle sync
3. Run `flutter run` (installs to phone)
4. Open App -> Settings -> enter PC IP

### Verify Connection

App should show "connected" or similar. Make a test call:
- Dial another phone (or friend)
- App should auto-enter "in-call" screen
- After customer speaks, AI suggestion should appear in 1-2 seconds

## Stage 3: End-to-End Verification

### Test Real-time Suggestions

1. Prepare fixed script (have friend read):
   > "How much does your product cost? How is the after-sales? What advantages over company XX?"

2. Call and have friend read

3. Observe phone screen:
   - "How much" -> should show "price negotiation" scenario
   - "after-sales" -> should show "product intro" scenario
   - "comparison" -> should show "objection handling" scenario

4. Time check: customer finishes speaking -> suggestion appears should be < 2 seconds

### Test Post-call Replay

1. Hang up
2. App should auto-display "replay" screen
3. Verify 5 dimensions:
   - One-sentence summary
   - Customer concerns
   - Main objections
   - Emotion curve
   - Areas for improvement
   - Follow-up actions

### Test History

1. Exit app, reopen
2. Go to "Call History"
3. Should see the recent call

## Common Issues

### Q: Suggestion latency > 2 seconds
- Check WiFi signal
- Check if PC is in sleep mode
- Check Xunfei API quota

### Q: Replay generation fails
- Check DeepSeek API balance
- Check network (PC needs to reach deepseek.com)
- Check `pc_service/logs/assistant-*.log` for errors

### Q: Phone cannot connect to PC
- Confirm phone and PC on same WiFi
- Check PC firewall allows port 8765
- Try `telnet 192.168.1.100 8765` from PC
- Verify App IP setting

### Q: Audio unclear
- Adjust phone mic position
- Speak louder
- Future: add noise reduction