import 'dart:async';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class StreamService {
  WebSocketChannel? _channel;
  StreamController<Map<String, dynamic>>? _suggestionController;
  String? _pcIp;

  Stream<Map<String, dynamic>> get suggestionStream =>
      _suggestionController!.stream;

  /// Lazily reads the PC IP from SharedPreferences (set on the
  /// Settings screen). Falls back to a sensible LAN default.
  Future<String> _resolvePcHost() async {
    if (_pcIp != null) return _pcIp!;
    final prefs = await SharedPreferences.getInstance();
    _pcIp = prefs.getString('pc_ip') ?? '192.168.1.100';
    return _pcIp!;
  }

  Future<void> connect() async {
    if (_channel != null) return;
    _suggestionController = StreamController<Map<String, dynamic>>();
    final host = await _resolvePcHost();
    final uri = Uri.parse('ws://$host:8765/ws/audio');
    _channel = WebSocketChannel.connect(uri);
    _channel!.stream.listen((data) {
      if (data is String) {
        try {
          final msg = jsonDecode(data);
          if (msg is Map && msg['type'] == 'suggestion') {
            _suggestionController?.add(
              Map<String, dynamic>.from(msg),
            );
          }
        } catch (_) {}
      }
    });
    sendCallStart();
  }

  void sendCallStart() {
    _channel?.sink.add(jsonEncode({
      'type': 'call_start',
      'phone_number': null,
      'mode': 'in_person',
    }));
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
    _suggestionController = null;
  }
}