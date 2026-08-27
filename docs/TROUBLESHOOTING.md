# Troubleshooting & Known Gotchas

A log of subtle issues hit during development. Each entry includes symptom,
root cause, fix, and how to verify.

## 1. Xunfei RTAS WebSocket returns 10110 `no license`

**Symptom**: every call to `XunfeiASR.recognize()` raises
`RuntimeError: Xunfei ASR error 10110: no license|illegal signa`.

**Investigation** (took 6 systematic-debugging rounds):

1. We first suspected `signa` was wrong because the error description contained
   `illegal signa`. We fixed:
   - HMAC key: `api_secret` -> `APIKey`
   - URL param: `app_id` -> `appid`
   - WebSocket multi-frame protocol: only recv() once, missing `started` frame
   - HMAC algorithm: SHA256 -> SHA1
   - Missing `transType: "normal"` in start frame
2. After all 5 fixes, the signa value matched the official Java SDK
   (verified with .NET `HMACSHA1` -> identical base64).
3. The error still returned 10110 with description `no license|illegal signa`.
4. We verified that even with 3 different start-frame variants the server
   returned the same 10110, so the issue is not a request-shape problem.
5. The 10110 code, per Xunfei docs, means "appid has no permission for this
   interface", i.e. **account-level**, not code-level.

**Status**: code is verified correct; the 10110 is from the Xunfei account
needing WebAPI permission activated in console.xfyun.cn. Documented template
for contacting Xunfei support is in `docs/USER_GUIDE.md`.

## 2. Port 8765 occupied by Baidu Pinyin

**Symptom**: `uvicorn` startup fails with
`OSError: [Errno 10048] Only one usage of each socket address...`

**Root cause**: `BaiduPinyin.exe` (PID 20084) is a protected process listening
on 8765; cannot be killed even by `taskkill /F /PID`.

**Fix**: run PC server on 8766 (or any other free port):
```
python -m uvicorn server.websocket_server:app --port 8766
```

**Verify**: `netstat -ano | findstr :8765` should show baidupinyin as owner;
`netstat -ano | findstr :8766` should be empty before start.

## 3. `D:\PersonalAssistant\data` is not SQLite-writable

**Symptom**: `sqlite3.OperationalError: attempt to write a readonly database`
even though:
- The file's Windows attributes show 0x20 (ARCHIVE, no READONLY flag).
- `os.access(db_path, os.W_OK)` returns True.
- `os.access(parent_dir, os.W_OK)` returns True.
- `init_app()` succeeded and created the file.

**Root cause**: unknown directory-level restriction. Even creating a *new*
DB in the same dir (e.g. `test_fresh.db`) fails with `unable to open database file`.

**Fix**: use `C:\Users\<user>\AppData\Local\Temp\sales_assistant.db` (verified
writable in this env). Update `DB_PATH` and `BACKUP_DIR` in `.env`.

## 4. SQLite `INSERT` returns readonly even with read-write connection

**Symptom**: `Database.execute("INSERT ...")` raises readonly error, but
`PRAGMA query_only` returns 0, `PRAGMA quick_check` returns ok, and
fresh connections from a separate process succeed.

**Root cause**: same as #3 (directory restriction). Once the file is in
`D:\PersonalAssistant\data`, the only writable operation is `init_schema`
(once, on first connect). After that, any further INSERT fails.

## 5. `flutter analyze` crashes on workspace path with non-ASCII characters

**Symptom**: `FormatException: Unterminated string` from Flutter analyze,
ending in `D:\GPT浏览器下载\新的录音\phone_app/`.

**Root cause**: known bug in the Flutter tool (analysis_server JSON
decoder) when the workspace path contains non-ASCII characters.

**Fix**: create a junction to a pure-ASCII path:
```
cmd /c "mklink /J C:\sales_assistant_dev D:\GPT浏览器下载\新的录音"
```
Then run `flutter` from `C:\sales_assistant_dev\phone_app`.

## 6. Python `subprocess.Popen` with `CREATE_NO_WINDOW` flag 0x08000000

**Symptom**: subprocess starts but `proc.pid` is empty; Start-Process fails
with "Path" -> "PATH" keyword conflict.

**Fix**: use `subprocess.Popen([...], creationflags=0x08000000)` (a Python int
literal, not PowerShell variable name). And use absolute path for the
executable, not a bare name.

## 7. PowerShell terminal encoding garbles Chinese stdout

**Symptom**: `print(deepseek_response)` shows `���` for every Chinese char.

**Root cause**: Windows PowerShell default code page is GBK (936), not UTF-8.
Our test scripts write UTF-8 to console, but PS reinterprets as GBK.

**Workarounds**:
- For one-off prints: `Write-Host $chineseString` may show correctly.
- For programmatic verification: write to a UTF-8 file and `Get-Content
  -Encoding UTF8`.
- For long-running tests: redirect output to a file with `[System.IO.File]::WriteAllText`.

## 8. `phone_state: ^1.0.0` Flutter API was wrong

**Symptom**: app failed to compile; we used `PhoneState.phoneStateStream`
and `PhoneStateStatus.CALL_OUTGOING` which do not exist in the real package.

**Root cause**: plan was written from memory, not from verified docs.
The actual 1.0.4 API uses `PhoneState.stream` (static getter) and
`PhoneStateStatus.{NOTHING, CALL_INCOMING, CALL_STARTED, CALL_ENDED}`.
No `CALL_OUTGOING` exists.

**Fix**: removed `phone_state` dependency entirely (in-person sales
mode does not need call-state monitoring).

## 9. Python 3.14 `hmac` module differs from manual implementation

**Symptom**: manual HMAC-SHA1 produced different result from `hmac.new(..., sha1)`.

**Root cause**: my manual HMAC implementation had a bug. `hmac` module
is correct in Python 3.14. Verified with .NET `HMACSHA1` -> identical result.

**Lesson**: do not implement HMAC manually; always cross-check against a
standard library implementation.

## 10. `pubspec.lock` was generated AFTER commit, not committed in time

**Symptom**: `flutter pub get` reinstalled the wrong version of `http`
package even after we added it to `pubspec.yaml`. The first commit said
"http added" but `pubspec.lock` did not yet contain it.

**Root cause**: `flutter pub get` writes the lock file asynchronously and
may not have flushed it before the first `git add` happened.

**Fix**: always re-run `flutter pub get` after editing `pubspec.yaml`,
verify the lock file mentions the new dep, THEN commit.
