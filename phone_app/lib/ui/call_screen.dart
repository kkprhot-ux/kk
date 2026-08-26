import 'dart:async';

import 'package:flutter/material.dart';

import '../services/audio_capture.dart';
import '../services/stream_service.dart';
import '../services/vad_service.dart';

class CallScreen extends StatefulWidget {
  final StreamService stream;
  final AudioCaptureService audio;
  final VadService vad;

  const CallScreen({
    super.key,
    required this.stream,
    required this.audio,
    required this.vad,
  });

  @override
  State<CallScreen> createState() => _CallScreenState();
}

class _CallScreenState extends State<CallScreen> {
  StreamSubscription<Map<String, dynamic>>? _suggestionSub;
  StreamSubscription<List<int>>? _audioSub;
  final List<Map<String, dynamic>> _suggestions = [];
  Map<String, dynamic>? _latest;

  @override
  void initState() {
    super.initState();
    _suggestionSub = widget.stream.suggestionStream.listen((msg) {
      setState(() {
        _suggestions.insert(0, msg);
        _latest = msg;
        if (_suggestions.length > 50) {
          _suggestions.removeRange(50, _suggestions.length);
        }
      });
    });
    _audioSub = widget.audio.audioStream.listen((chunk) {
      // 1. Run VAD on chunk
      // 2. If VAD says "chunk ends a sentence" (silence > threshold),
      //    forward to PC backend via widget.stream.sendAudioChunk.
      // The real VAD-to-stream glue lives in HomeScreen; for v2.1 we just
      // forward raw chunks so the backend can decide.
      if (_latest == null) {
        widget.stream.sendAudioChunk(chunk);
      }
    });
  }

  @override
  void dispose() {
    _suggestionSub?.cancel();
    _audioSub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final latest = _latest;
    return Scaffold(
      appBar: AppBar(title: const Text('对话中')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildLatestCard(latest),
            const SizedBox(height: 16),
            const Text('历史话术', style: TextStyle(color: Colors.white70)),
            const SizedBox(height: 8),
            Expanded(child: _buildHistory()),
          ],
        ),
      ),
    );
  }

  Widget _buildLatestCard(Map<String, dynamic>? latest) {
    if (latest == null) {
      return Card(
        color: Colors.blueGrey.shade900,
        child: const Padding(
          padding: EdgeInsets.all(20),
          child: Row(
            children: [
              Icon(Icons.hourglass_empty, color: Colors.white60),
              SizedBox(width: 12),
              Expanded(
                child: Text('等待客户开口...',
                    style: TextStyle(color: Colors.white70)),
              ),
            ],
          ),
        ),
      );
    }
    return Card(
      color: Colors.green.shade900,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('🎯 实时话术 (${latest['scenario'] ?? '-'})',
                style: const TextStyle(color: Colors.white, fontSize: 16)),
            const SizedBox(height: 4),
            Text('客户情绪: ${latest['emotion'] ?? '-'}',
                style: const TextStyle(color: Colors.white70)),
            const Divider(),
            Text('💬 ${latest['recommended_script'] ?? '...'}',
                style: const TextStyle(color: Colors.white, fontSize: 16)),
            const SizedBox(height: 8),
            Text('⏱ 下一句: ${latest['next_step'] ?? '-'}',
                style: const TextStyle(color: Colors.white70)),
          ],
        ),
      ),
    );
  }

  Widget _buildHistory() {
    if (_suggestions.isEmpty) {
      return const Center(
        child: Text('还没有历史话术', style: TextStyle(color: Colors.white30)),
      );
    }
    return ListView.builder(
      itemCount: _suggestions.length,
      itemBuilder: (context, i) {
        final s = _suggestions[i];
        return ListTile(
          dense: true,
          leading: const Icon(Icons.history, color: Colors.white60),
          title: Text('${s['scenario'] ?? '-'}',
              style: const TextStyle(color: Colors.white)),
          subtitle: Text('${s['recommended_script'] ?? ''}',
              maxLines: 1, overflow: TextOverflow.ellipsis,
              style: const TextStyle(color: Colors.white70)),
        );
      },
    );
  }
}