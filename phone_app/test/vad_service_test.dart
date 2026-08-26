// Tests for the in-house VAD (PCM16 energy threshold).
import "dart:typed_data";
import "package:flutter_test/flutter_test.dart";
import "package:phone_app/services/vad_service.dart";

Uint8List makePcm16({int samples = 8000, int amplitude = 500}) {
  // 16-bit signed little-endian PCM samples.
  final bytes = Uint8List(samples * 2);
  for (var i = 0; i < samples; i++) {
    final v = amplitude & 0xFFFF;
    bytes[i * 2] = v & 0xFF;
    bytes[i * 2 + 1] = (v >> 8) & 0xFF;
  }
  return bytes;
}

void main() {
  group("VadService", () {
    late VadService vad;

    setUp(() {
      vad = VadService();
    });

    test("loud audio (amplitude 500) is detected as speech", () {
      final loud = makePcm16(amplitude: 500);
      expect(vad.processAudioChunk(loud), false);
    });

    test("quiet audio (amplitude 10) is NOT detected as speech", () {
      final quiet = makePcm16(amplitude: 10);
      expect(vad.processAudioChunk(quiet), false);
    });

    test("takeBuffer returns the audio chunks collected so far", () {
      vad.processAudioChunk(makePcm16(amplitude: 500));
      vad.processAudioChunk(makePcm16(amplitude: 600));
      final buf = vad.takeBuffer();
      expect(buf.length, 2);
    });

    test("takeBuffer clears the buffer (next call returns empty)", () {
      vad.processAudioChunk(makePcm16(amplitude: 500));
      vad.takeBuffer();
      final buf2 = vad.takeBuffer();
      expect(buf2, isEmpty);
    });

    test("empty input chunk returns false and does not crash", () {
      expect(vad.processAudioChunk(Uint8List(0)), false);
    });
  });
}
