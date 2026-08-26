import 'dart:async';
import 'dart:typed_data';
import 'package:flutter_sound/flutter_sound.dart';

class AudioCaptureService {
  final FlutterSoundRecorder _recorder = FlutterSoundRecorder();
  bool _isRecording = false;
  StreamController<Uint8List>? _audioStreamController;

  Stream<Uint8List> get audioStream => _audioStreamController!.stream;
  bool get isRecording => _isRecording;

  Future<void> start() async {
    await _recorder.openRecorder();
    await _recorder.startRecorder(
      toStream: _audioStreamController = StreamController<Uint8List>(),
      codec: Codec.pcm16,
      sampleRate: 16000,
      numChannels: 1,
    );
    _isRecording = true;
  }

  Future<void> stop() async {
    await _recorder.stopRecorder();
    await _recorder.closeRecorder();
    _isRecording = false;
    _audioStreamController?.close();
  }
}