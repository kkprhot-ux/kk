import 'package:flutter/material.dart';
import 'package:phone_state/phone_state.dart';

class PhoneStateService extends ChangeNotifier {
  String? _currentNumber;
  bool _isInCall = false;

  String? get currentNumber => _currentNumber;
  bool get isInCall => _isInCall;

  void startListening() {
    PhoneState.phoneStateStream.listen((state) {
      switch (state.status) {
        case PhoneStateStatus.CALL_INCOMING:
        case PhoneStateStatus.CALL_OUTGOING:
          _isInCall = true;
          _currentNumber = state.number;
          notifyListeners();
          break;
        case PhoneStateStatus.NOTHING:
        case PhoneStateStatus.CALL_ENDED:
          _isInCall = false;
          _currentNumber = null;
          notifyListeners();
          break;
        default:
          break;
      }
    });
  }
}