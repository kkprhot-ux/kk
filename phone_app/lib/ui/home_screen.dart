import 'package:flutter/material.dart';

import '../services/audio_capture.dart';
import '../services/stream_service.dart';
import '../services/vad_service.dart';
import 'call_screen.dart';

class HomeScreen extends StatefulWidget {
  final GlobalKey<NavigatorState> navigatorKey;
  // Optional dependencies for testing: production passes nothing and gets
  // real AudioCaptureService / StreamService / VadService instances.
  final AudioCaptureService? audioOverride;
  final StreamService? streamOverride;
  final VadService? vadOverride;

  const HomeScreen({
    super.key,
    required this.navigatorKey,
    this.audioOverride,
    this.streamOverride,
    this.vadOverride,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // In-person sales: the user explicitly starts/stops a session.
  // We do not rely on phone-state changes.
  bool _isRecording = false;
  late final AudioCaptureService _audio;
  late final StreamService _stream;
  late final VadService _vad;

  @override
  void initState() {
    super.initState();
    _audio = widget.audioOverride ?? AudioCaptureService();
    _stream = widget.streamOverride ?? StreamService();
    _vad = widget.vadOverride ?? VadService();
  }

  @override
  void dispose() {
    if (_isRecording) {
      _stopSession();
    }
    // Only stop audio if we own it (not from override).
    if (widget.audioOverride == null) {
      _audio.stop();
    }
    super.dispose();
  }

  Future<void> _startSession() async {
    await _stream.connect();
    await _audio.start();
    setState(() => _isRecording = true);
    if (!mounted) return;
    widget.navigatorKey.currentState?.push(
      MaterialPageRoute(
        builder: (_) => CallScreen(
          stream: _stream,
          audio: _audio,
          vad: _vad,
        ),
      ),
    );
  }

  Future<void> _stopSession() async {
    await _audio.stop();
    await _stream.disconnect();
    if (mounted) setState(() => _isRecording = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('销售助手')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: _isRecording ? Colors.red.shade900 : Colors.blueGrey.shade900,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Icon(
                    _isRecording ? Icons.mic : Icons.mic_off,
                    size: 64,
                    color: _isRecording ? Colors.redAccent : Colors.white60,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    _isRecording ? '录音中…' : '未开始',
                    style: const TextStyle(fontSize: 18, color: Colors.white),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _isRecording
                        ? '点 "结束" 关闭本通会话, AI 将生成复盘'
                        : '点 "开始" 启动实时话术推荐',
                    style: const TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 56,
            child: ElevatedButton.icon(
              icon: Icon(_isRecording ? Icons.stop_circle : Icons.play_circle),
              label: Text(_isRecording ? '结束' : '开始',
                  style: const TextStyle(fontSize: 18)),
              style: ElevatedButton.styleFrom(
                backgroundColor: _isRecording ? Colors.red : Colors.green,
                foregroundColor: Colors.white,
              ),
              onPressed: _isRecording ? _stopSession : _startSession,
            ),
          ),
          const Divider(height: 32),
          ListTile(
            leading: const Icon(Icons.history),
            title: const Text('通话历史'),
            onTap: () => Navigator.pushNamed(context, '/history'),
          ),
          ListTile(
            leading: const Icon(Icons.settings),
            title: const Text('设置'),
            onTap: () => Navigator.pushNamed(context, '/settings'),
          ),
        ],
      ),
    );
  }
}
