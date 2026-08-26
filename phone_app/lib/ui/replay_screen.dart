import 'package:flutter/material.dart';

class ReplayScreen extends StatelessWidget {
  final Map<String, dynamic> replay;
  final String phoneNumber;

  const ReplayScreen({super.key, required this.replay, required this.phoneNumber});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('复盘 - $phoneNumber')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _section('一句话总结', replay['summary'] ?? '-'),
          _listSection('客户关注点', replay['customer_concerns'] ?? []),
          _listSection('主要异议', replay['objections'] ?? []),
          _section('情绪曲线', (replay['emotion_curve'] ?? []).join(' → ')),
          _listSection('您的亮点', replay['highlights'] ?? []),
          _listSection('待改进', replay['improvements'] ?? []),
          _listSection('后续行动', replay['next_actions'] ?? []),
        ],
      ),
    );
  }

  Widget _section(String title, String content) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(content),
          ],
        ),
      ),
    );
  }

  Widget _listSection(String title, List<dynamic> items) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...items.map((item) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text('• $item'),
            )),
          ],
        ),
      ),
    );
  }
}