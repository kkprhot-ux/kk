import 'dart:typed_data';

/// NOTE: Spec 计划使用 `silero_vad: ^0.1.0`，但该包不存在于 pub.dev
/// (404 NoSuchKey)。本服务使用 **能量阈值** 检测作为临时实现，
/// 保留 spec 的 API 形态（processAudioChunk / takeBuffer / silenceThreshold），
/// 后续可替换为 `vad` (Silero VAD 的官方 Flutter 绑定) 或 `onnxruntime`。
class VadService {
  final List<Uint8List> _buffer = [];
  bool _isSpeaking = false;
  DateTime? _lastSpeechTime;
  static const _silenceThreshold = Duration(milliseconds: 800);

  // PCM16 (16-bit signed LE) 平均绝对值阈值。
  // 实测安静室内 ~50-150，正常说话 ~500-3000。
  // TODO(后续): 用 silero_vad 或 vad 包替换
  static const _energyThreshold = 300;

  /// 处理音频块，返回 true 表示"攒句完成"
  bool processAudioChunk(Uint8List chunk) {
    final isSpeech = _calculateEnergy(chunk) > _energyThreshold;
    if (isSpeech) {
      _isSpeaking = true;
      _lastSpeechTime = DateTime.now();
      _buffer.add(chunk);
      return false;
    } else if (_isSpeaking) {
      _buffer.add(chunk);
      if (_lastSpeechTime != null &&
          DateTime.now().difference(_lastSpeechTime!) > _silenceThreshold) {
        return true;
      }
    }
    return false;
  }

  List<Uint8List> takeBuffer() {
    final result = List<Uint8List>.from(_buffer);
    _buffer.clear();
    _isSpeaking = false;
    _lastSpeechTime = null;
    return result;
  }

  int _calculateEnergy(Uint8List chunk) {
    if (chunk.isEmpty) return 0;
    int sum = 0;
    int sampleCount = chunk.lengthInBytes ~/ 2;
    for (int i = 0; i < chunk.lengthInBytes; i += 2) {
      // 小端 PCM16: 低位在前
      int sample = chunk[i] | (chunk[i + 1] << 8);
      // 转有符号
      if (sample >= 0x8000) sample -= 0x10000;
      sum += sample.abs();
    }
    return sampleCount == 0 ? 0 : sum ~/ sampleCount;
  }
}