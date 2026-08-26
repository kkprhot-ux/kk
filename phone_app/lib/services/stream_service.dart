import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class StreamService {
  WebSocketChannel? _channel;
  StreamController<Map<String, dynamic>>? _suggestionController;

  Stream<Map<String, dynamic>> get suggestionStream =>
      _suggestionController!.stream;

  Future<void> connect() async {
    if (_channel != null) return;
    _suggestionController = StreamController<Map<String, dynamic>>();
    // 电脑 IP（生产环境从配置读取）
    _channel = WebSocketChannel.connect(
      Uri.parse('ws://192.168.1.100:8765/ws/audio'),
    );
    _channel!.stream.listen((data) {
      if (data is String) {
        try {
          final msg = jsonDecode(data);
          if (msg['type'] == 'suggestion') {
            _suggestionController?.add(msg);
          }
        } catch (_) {}
      }
    });
    sendCallStart();
  }

  void sendCallStart() {
    _channel?.sink.add(jsonEncode({'type': 'call_start', 'phone_number': null}));
  }

  void sendCallEnd() {
    _channel?.sink.add(jsonEncode({'type': 'call_end'}));
  }

  void sendAudioChunk(List<int> audioBytes) {
    _channel?.sink.add(audioBytes);
  }

  Future<void> disconnect() async {
    sendCallEnd();
    await _channel?.sink.close();
    _channel = null;
    await _suggestionController?.close();
  }
}