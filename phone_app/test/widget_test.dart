// Smoke tests for the app. We construct HomeScreen with mock services
// so flutter_sound is never instantiated.
import "dart:async";
import "dart:typed_data";

import "package:flutter/material.dart";
import "package:flutter_test/flutter_test.dart";
import "package:phone_app/ui/home_screen.dart";
import "package:phone_app/services/audio_capture.dart";
import "package:phone_app/services/stream_service.dart";
import "package:phone_app/services/vad_service.dart";

class _FakeAudio implements AudioCaptureService {
  @override
  Stream<Uint8List> get audioStream => const Stream<Uint8List>.empty();
  @override
  bool get isRecording => false;
  @override
  Future<void> start() async {}
  @override
  Future<void> stop() async {}
}

class _FakeStream implements StreamService {
  @override
  Stream<Map<String, dynamic>> get suggestionStream =>
      const Stream<Map<String, dynamic>>.empty();
  @override
  Future<void> connect() async {}
  @override
  Future<void> disconnect() async {}
  @override
  void sendCallStart() {}
  @override
  void sendCallEnd() {}
  @override
  void sendAudioChunk(List<int> audioBytes) {}
}

class _FakeVad implements VadService {
  @override
  bool processAudioChunk(Uint8List chunk) => false;
  @override
  List<Uint8List> takeBuffer() => [];
}

void main() {
  testWidgets("HomeScreen shows 销售助手 title and Start button", (tester) async {
    final navKey = GlobalKey<NavigatorState>();
    await tester.pumpWidget(MaterialApp(
      navigatorKey: navKey,
      home: HomeScreen(
        navigatorKey: navKey,
        audioOverride: _FakeAudio(),
        streamOverride: _FakeStream(),
        vadOverride: _FakeVad(),
      ),
    ));
    await tester.pump();

    // Top bar
    expect(find.text("销售助手"), findsOneWidget);

    // Idle card
    expect(find.text("未开始"), findsOneWidget);

    // Start button label
    expect(find.text("开始"), findsOneWidget);

    // History and settings rows
    expect(find.text("通话历史"), findsOneWidget);
    expect(find.text("设置"), findsOneWidget);
  });

  testWidgets("Tapping Start changes state to 录音中 (UI only)", (tester) async {
    final navKey = GlobalKey<NavigatorState>();
    final fakeStream = _FakeStream();
    await tester.pumpWidget(MaterialApp(
      navigatorKey: navKey,
      home: HomeScreen(
        navigatorKey: navKey,
        audioOverride: _FakeAudio(),
        streamOverride: fakeStream,
        vadOverride: _FakeVad(),
      ),
    ));
    await tester.pump();

    // Tap Start. This will trigger _startSession which calls audio.start
    // (no-op in fake) and stream.connect (no-op in fake), then sets state.
    await tester.tap(find.text("开始"));
    await tester.pump();

    // After tap, the label should change to "结束" and the card to "录音中…"
    expect(find.text("结束"), findsOneWidget);
    expect(find.text("录音中…"), findsOneWidget);
  });
}
