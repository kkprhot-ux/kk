import 'package:flutter/material.dart';
import 'services/phone_state_service.dart';
import 'services/stream_service.dart';
import 'ui/home_screen.dart';
import 'ui/history_screen.dart';
import 'ui/settings_screen.dart';

void main() {
  runApp(const SalesAssistantApp());
}

class SalesAssistantApp extends StatefulWidget {
  const SalesAssistantApp({super.key});
  @override
  State<SalesAssistantApp> createState() => _SalesAssistantAppState();
}

class _SalesAssistantAppState extends State<SalesAssistantApp> {
  final phoneState = PhoneStateService();
  final streamService = StreamService();

  @override
  void initState() {
    super.initState();
    phoneState.startListening();
    phoneState.addListener(_onPhoneStateChanged);
  }

  void _onPhoneStateChanged() {
    if (phoneState.isInCall) {
      streamService.connect();
    } else {
      streamService.disconnect();
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '销售助手',
      theme: ThemeData.dark(),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/history': (context) => const HistoryScreen(),
        '/settings': (context) => const SettingsScreen(),
      },
    );
  }
}