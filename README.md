# 实时销售辅助 App (MVP)

打电话时 AI 实时推荐话术（< 2 秒延迟），通话后自动生成复盘。

## 项目状态

- ✅ **Phase 1 电脑端**: 完成 (10 个 commit, 10 个测试通过)
- ⏳ **Phase 2 手机端**: 进行中
- ⏳ **Phase 3 集成测试**: 待开始

## 架构

手机端（Flutter）采集通话音频 → WebSocket 推流到电脑端（Python）→ 电脑端调云端 ASR（讯飞）转文字 → 攒句触发 LLM（DeepSeek）分析 → 生成话术推送回手机。

## 快速开始

### 1. 配置电脑端

```powershell
cd pc_service
pip install -r requirements.txt
copy .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY + 讯飞凭证
python main.py
```

电脑端会监听 `0.0.0.0:8765` 端口。

### 2. 配置手机端

```powershell
cd phone_app
flutter pub get
flutter run
```

### 3. 设置电脑 IP

打开 App → 设置 → 填入电脑 IP（如 192.168.1.100:8765）

### 4. 打电话测试

App 自动检测电话状态 → 实时显示 AI 话术

## 文档

- 设计 Spec: `docs/superpowers/specs/2026-08-26-real-time-sales-assistant-design.md`
- 实施计划: `docs/superpowers/plans/2026-08-26-sales-assistant-mvp.md`
- GitHub 调研: `docs/superpowers/specs/2026-08-25-github-research-report.md`
- 用户手册: `docs/USER_GUIDE.md`

## 技术栈

- **手机端**: Flutter 3.47.1 + Dart 3.13.1
- **电脑端**: Python 3.14 + FastAPI + websockets
- **AI**: 讯飞流式 ASR + DeepSeek LLM
- **存储**: SQLite + 每日本地备份

## 参考开源

- [fluxions-ai/vui](https://github.com/fluxions-ai/vui) (747⭐) - 实时架构
- [ptc31141-maker/ai-tob-sales-copilot](https://github.com/ptc31141-maker/ai-tob-sales-copilot) (2⭐) - 销售功能