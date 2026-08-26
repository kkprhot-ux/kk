import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});
  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<dynamic> _calls = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    try {
      final response = await http.get(Uri.parse('http://192.168.1.100:8765/calls'));
      if (response.statusCode == 200) {
        setState(() {
          _calls = jsonDecode(response.body);
        });
      }
    } catch (e) {
      // 网络错误处理
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('通话历史')),
      body: _calls.isEmpty
          ? const Center(child: Text('暂无通话记录'))
          : ListView.builder(
              itemCount: _calls.length,
              itemBuilder: (context, index) {
                final call = _calls[index];
                return ListTile(
                  title: Text(call['phone_number'] ?? '未知号码'),
                  subtitle: Text('${call['start_time']} - ${call['duration_sec'] ?? 0}秒'),
                );
              },
            ),
    );
  }
}