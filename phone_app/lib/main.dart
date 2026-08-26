import 'package:flutter/material.dart';
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
  // v2.1: in-person sales mode. The user manually starts/stops a recording
  // session from the Home screen; no automatic call-state monitoring
  // is needed. Recording UI is managed by HomeScreen -> CallScreen.
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '销售助手',
      theme: ThemeData.dark(),
      navigatorKey: navigatorKey,
      initialRoute: '/',
      routes: {
        '/': (context) => HomeScreen(navigatorKey: navigatorKey),
        '/history': (context) => const HistoryScreen(),
        '/settings': (context) => const SettingsScreen(),
      },
    );
  }
}