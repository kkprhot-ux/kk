import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('销售助手')),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.phone, size: 32),
            title: const Text('当前通话'),
            subtitle: const Text('打电话时自动启动'),
          ),
          const Divider(),
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