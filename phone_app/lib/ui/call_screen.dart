import 'package:flutter/material.dart';

class CallScreen extends StatelessWidget {
  final String? phoneNumber;
  final Map<String, dynamic>? currentSuggestion;

  const CallScreen({
    super.key,
    this.phoneNumber,
    this.currentSuggestion,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('通话中 - ${phoneNumber ?? "未知"}')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              color: Colors.blue.shade900,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('客户最后一句', style: TextStyle(color: Colors.white70)),
                    const SizedBox(height: 8),
                    Text(
                      currentSuggestion?['customer_text'] ?? '...',
                      style: const TextStyle(fontSize: 18),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              color: Colors.green.shade900,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('🎯 实时话术推荐', style: TextStyle(color: Colors.white, fontSize: 16)),
                    const SizedBox(height: 8),
                    Text('场景：${currentSuggestion?['scenario'] ?? "-"}'),
                    Text('客户情绪：${currentSuggestion?['emotion'] ?? "-"}'),
                    const Divider(),
                    Text('💬 推荐话术：', style: TextStyle(color: Colors.white)),
                    Text(
                      currentSuggestion?['recommended_script'] ?? '...',
                      style: const TextStyle(fontSize: 16, color: Colors.white),
                    ),
                    const SizedBox(height: 8),
                    Text('⏱ 下一句建议：${currentSuggestion?['next_step'] ?? "-"}'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}