# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2026-08-27

### Changed
- **Product mode**: Switched from phone-call sales to in-person sales.
  Reason: Android disallows third-party apps from recording call audio
  (Xunfei RTAS `voiceDownlink` / `voiceUpLink` are explicitly documented
  as not working on Android). Default-microphone capture works in person.
- **Trigger model**: Removed automatic call-state listener; user manually
  presses Start/End button on the Home screen.
- **Storage**: Removed unused `contacts` table; added `mode` column to `calls`.

### Fixed
- **`finalize_call` SQL bug**: Single `UPDATE` with `duration_sec = end_time - start_time`
  always returned NULL because SQLite evaluates `end_time` reference to the
  pre-update value. Split into two UPDATEs.
- **`home_screen.dart`**: Now accepts optional `audioOverride`, `streamOverride`,
  `vadOverride` so widget tests can run without instantiating `flutter_sound`.
- **Flutter analyze in workspace with Chinese path**: Created junction
  `C:\sales_assistant_dev` -> workspace to bypass the Flutter tool bug.
- **Port 8765 occupied by Baidu Pinyin**: PC server now runs on 8766 by default.
- **`.env` path `D:\PersonalAssistant\data` is not SQLite-writable in this env**:
  switched to `C:\Users\...\Temp\sales_assistant.db`.

### Tests
- 56 tests passing, 100% coverage of `pc_service`.
- 7 Flutter tests passing, 0 `flutter analyze` warnings.

### Known Limitations
- Xunfei ASR (RTAS WebSocket) returns 10110 `no license` from this account.
  Code is verified correct against the official Java SDK; account-level
  permission issue. Documented in `docs/TROUBLESHOOTING.md`.
- `flutter analyze` crashes on paths with non-ASCII characters (Flutter tool
  bug, not code). Use the `C:\sales_assistant_dev` junction.
- `D:\PersonalAssistant\data` directory is mysteriously not SQLite-writable
  even though it appears normal. Use the workspace directory instead.

## [2.0.0] - 2026-08-26

### Added
- Initial MVP scaffold: 20 tasks across PC + Flutter sides.
- Realtime sales assistant with in-person mode.
