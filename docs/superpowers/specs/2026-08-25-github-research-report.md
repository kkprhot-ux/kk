# GitHub 开源项目调研报告 - 实时销售辅助 App

| 项目 | 内容 |
|---|---|
| **日期** | 2026-08-25 |
| **调研目的** | 在写代码前，找类似项目，参考架构，避免重复造轮子 |
| **目标产品** | 实时监听电话 → AI 分析 → 销售话术推荐 → 推到手机 |

---

## 1. 调研方法

通过 GitHub Search API 按以下关键词搜索：
- ealtime speech AI assistant
- sales copilot
- whisper realtime LLM
- AI 销售 辅助
- ealtime voice agent whisper
- AI call center assistant

筛选标准：
- ⭐ Stars 较高（成熟度）
- 🔄 最近更新（活跃维护）
- 🎯 与"实时语音 + AI 分析"相关
- 💼 与"销售/客服"场景相关

---

## 2. 候选项目（5 个最相关）

### 2.1 fluxions-ai/vui

| 项目 | 内容 |
|---|---|
| **GitHub** | https://github.com/fluxions-ai/vui |
| **Stars** | 747 ⭐ |
| **Forks** | 77 |
| **语言** | Python |
| **License** | Apache 2.0 |
| **更新** | 2026-08-25（活跃） |

**定位**：通用实时语音助手框架

**架构**：
- 🎙️ **音频流**：WebRTC + WebSocket
- 🔇 **VAD**：基于浏览器/服务器端
- 📝 **ASR**：faster-whisper（本地）
- 🧠 **LLM**：本地 + 云端混合
- 🔊 **TTS**：自研 Vui Nano（300M，基于 Qwen3 TTS）

**关键特性**：
- ✅ 实时延迟 < 200ms
- ✅ **Barge-in**（用户说话时 AI 停止回应）
- ✅ OpenAI Realtime API 兼容
- ✅ 声纹克隆
- ✅ VAD-driven turn taking
- ✅ 推测性 LLM prefill

**优点**：
- 🟢 架构成熟，文档完整
- 🟢 有 Hugging Face 模型权重
- 🟢 活跃维护
- 🟢 实时性能优秀

**缺点**：
- 🔴 **通用场景，不是销售专用**
- 🔴 没有"话术推荐"功能
- 🔴 TTS 是给 AI 主动说话用的，您可能不需要

---

### 2.2 smithakolan/AssemblyAI-AI-Voice-Bot

| 项目 | 内容 |
|---|---|
| **GitHub** | https://github.com/smithakolan/AssemblyAI-AI-Voice-Bot |
| **Stars** | 68 ⭐ |
| **语言** | Python |
| **License** | MIT |
| **更新** | 2026-08-13 |

**定位**：AI 客服/前台（用例：牙医助手）

**架构**：
- 📝 **ASR**：AssemblyAI（商业 API）
- 🧠 **LLM**：OpenAI
- 🔊 **TTS**：ElevenLabs（商业 API）

**优点**：
- 🟢 专门为 **call center** 设计
- 🟢 文档 + 视频教程完整
- 🟢 开箱即用

**缺点**：
- 🔴 全商业 API（贵：AssemblyAI + OpenAI + ElevenLabs）
- 🔴 不是销售专用
- 🔴 没有话术推荐

---

### 2.3 doshiankit/ai-voice-agent

| 项目 | 内容 |
|---|---|
| **GitHub** | https://github.com/doshiankit/ai-voice-agent |
| **Stars** | 1 ⭐ |
| **语言** | Shell + Python |
| **更新** | 2026-08-23 |

**定位**：生产级 AI voice agent（电话系统集成）

**架构**：
- 📞 **电话**：SIP + **FreeSWITCH**
- 🔇 **VAD**
- 📝 **ASR**：Whisper
- 🧠 **LLM**：Groq
- 🔊 **TTS**

**关键特性**：
- ✅ **<2s 延迟**
- ✅ 微服务架构
- ✅ 真实电话系统集成（不是麦克风监听）

**优点**：
- 🟢 **真实电话系统**集成（解决"怎么获取电话音频"的问题）
- 🟢 延迟低

**缺点**：
- 🔴 Stars 太少（1 ⭐，不成熟）
- 🔴 需要 FreeSWITCH（复杂、门槛高）
- 🔴 不是销售专用

---

### 2.4 Krishhs89/call-center-ai

| 项目 | 内容 |
|---|---|
| **GitHub** | https://github.com/Krishhs89/call-center-ai |
| **Stars** | 3 ⭐ |
| **语言** | Python |
| **更新** | 2026-05-13 |

**定位**：AI Call Center Assistant

**架构**：
- 🧠 **多 agent**：**LangGraph**（可以做"客户意图分析"、"话术生成"、"情绪判断"分别的 agent）
- 🤖 **LLM**：Claude / GPT-4o / Gemini
- 🖥️ **UI**：Streamlit

**优点**：
- 🟢 **多 agent 架构**（可以拆分任务：实时分析、话术生成、复盘）
- 🟢 AWS-ready

**缺点**：
- 🔴 Stars 少（不成熟）
- 🔴 不是实时（看起来是批量分析）
- 🔴 不是销售专用

---

### 2.5 ptc31141-maker/ai-tob-sales-copilot ⭐最相关

| 项目 | 内容 |
|---|---|
| **GitHub** | https://github.com/ptc31141-maker/ai-tob-sales-copilot |
| **Stars** | 2 ⭐ |
| **语言** | TypeScript |
| **技术栈** | Next.js 16 + TypeScript + Tailwind CSS v4 |
| **更新** | 2026-08-11 |

**定位**：**ToB 销售辅助**（面向应届 ToB 销售新人）

**核心功能**（**直接命中您的需求**）：
1. ✅ **AI 客户画像分析**（自动分析客户）
2. ✅ **销售话术生成**（基于客户背景）
3. ✅ **沟通复盘助手**（分析沟通记录）
4. ✅ 销售工作台（仪表盘）
5. ✅ 客户线索管理

**架构亮点**：
- ✅ **OpenAI-compatible API**（支持 DeepSeek、Qwen、Ollama 等）
- ✅ **Mock-first 架构**（没 API Key 也能跑）
- ✅ 内置 ToB 销售场景系统提示词
- ✅ 顾问式销售方法论

**优点**：
- 🟢 **直接是销售场景**，功能高度匹配
- 🟢 AI 调用层设计灵活（支持国产模型）
- 🟢 UI 完整（截图看效果不错）
- 🟢 一周内更新过（活跃）

**缺点**：
- 🔴 **不是实时的**（用户手动输入对话 → AI 给出话术）
- 🔴 Stars 少
- 🔴 没有电话/麦克风监听
- 🔴 没有 VAD、自动监听

---

### 2.6 其他相关项目

- **mehdi-jahani/ai_call_center** (15 ⭐) - FastAPI + VoIP + STT + LLM
- **skip53/oneclear-skill** (2 ⭐) - 工业除尘 ToB 销售 Skill
- **busrabektas/Digital-Assistant-for-Call-Centers** (6 ⭐) - 客服分析

---

## 3. 关键发现

### 3.1 没有"完美对口"的项目

**没有一个开源项目同时满足**：
- 实时监听电话
- 销售专用
- 话术推荐
- 推到手机

但有 **互补的两个项目**：

| 项目 | 提供的能力 |
|---|---|
| **fluxions-ai/vui** | **实时架构**（WebRTC + VAD + ASR + LLM + TTS 全套） |
| **ptc31141-maker/ai-tob-sales-copilot** | **销售功能**（话术生成、客户画像、复盘） |

### 3.2 实时性的核心要素（来自 vui）

实现 < 2s 延迟需要：

1. **流式 ASR**（不等整句结束就开始处理）
2. **VAD 严格**（静音 N 秒才提交一段对话）
3. **LLM streaming**（不等整段回复完，先显示前半段）
4. **段落级处理**（不是字符级，是语义段）
5. **WebRTC/WebSocket**（低延迟通信）

### 3.3 销售场景的关键技术（来自 sales-copilot）

- **多维度 prompt 模板**（开场白、异议处理、逼单、复盘）
- **客户画像自动生成**
- **话术分场景**（冷开发、跟进、谈判）
- **Mock-first 架构**（没 API 也能演示）

### 3.4 业界常用的技术栈组合

| 组件 | 推荐选型 | 理由 |
|---|---|---|
| 音频流 | **WebRTC** 或 **WebSocket + Opus** | 低延迟 |
| VAD | **silero-vad**（开源、CPU 友好） | 准确 |
| ASR | **faster-whisper**（本地）或 **讯飞流式**（云端） | 中文准 |
| LLM | **DeepSeek**（便宜）或 **Qwen**（中文好） | 性价比 |
| 多 agent | **LangGraph** | 任务拆分 |
| 桌面 UI | **Tauri** | 轻量 |
| 手机端 | **Flutter** 或 **Kotlin** | 跨平台/原生 |
| 实时通信 | **WebSocket** | 简单可靠 |

---

## 4. 实现方案（基于调研）

### 4.1 核心架构（融合 vui + sales-copilot）

\\\
┌──────────────┐
│  📞 电话音频  │  ← 来源：手机麦克风 / VoIP / 系统音频
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  🔇 VAD 检测  │  ← silero-vad（开源、CPU 友好）
└──────┬───────┘
       │ (说话时激活)
       ▼
┌──────────────┐
│  📝 ASR 转写  │  ← 讯飞流式 或 faster-whisper
└──────┬───────┘
       │ (实时文字片段)
       ▼
┌──────────────────────────────────────────────┐
│  🤖 LangGraph 多 Agent                         │
│  ┌────────────┐  ┌────────────┐  ┌────────┐  │
│  │ 意图分析   │  │ 异议检测   │  │ 情绪判断 │  │
│  └────────────┘  └────────────┘  └────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ 📣 话术生成（销售方法论 prompt）         │  │
│  └────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────┘
                   │ (流式输出)
                   ▼
┌──────────────────────────────────────────────┐
│  📱 推到手机 / 💻 显示在电脑                   │
│  - 实时字幕（您/客户）                         │
│  - 话术推荐（分场景）                          │
│  - 异议提醒                                   │
└──────────────────────────────────────────────┘
\\\

### 4.2 技术选型（针对您的环境）

| 组件 | 选型 | 理由 |
|---|---|---|
| ASR | **讯飞流式 API** | 中文准、便宜（0.003元/秒） |
| LLM | **DeepSeek** | 便宜、中文好 |
| 桌面应用 | **Tauri** | 轻量、您入门级电脑友好 |
| 手机 App | **Flutter**（跨平台）或 **Kotlin**（原生） | Flutter 跨平台省事 |
| 音频流 | **WebSocket + Opus** | 简单稳定 |
| VAD | **silero-vad-android**（手机）+ 服务端 VAD | 开源、准确 |
| 多 agent | **LangGraph**（可选，第一版可不用） | 任务拆分清晰 |
| 数据存储 | **SQLite**（第一版）| 单文件、好备份 |

### 4.3 第一版（MVP）范围

**必做**：
1. 手机 App：监听通话音频 + VAD + 推流
2. 电脑端：接收音频 + ASR + LLM 分析 + 实时话术推送
3. 销售话术分场景（开场白、异议处理、逼单、结束）
4. 实时显示：客户说的 + AI 推荐话术
5. 通话结束后：自动生成复盘（参考 sales-copilot）

**第一版暂缓**：
- 说话人识别（第一版都标"对方"）
- 完整人物图谱
- 24h 监听（销售只在打电话时用）
- 长期记忆
- 周报

---

## 5. 决策点（需要您拍板）

请回答以下问题，我再继续：

1. **技术路线**：采用"vui 实时架构 + sales-copilot 销售功能"的融合方案吗？
2. **手机端**：用 **Flutter**（跨平台）还是 **Kotlin**（原生安卓）？
3. **延迟要求**：实时话术多久出可以接受？
   - A. < 1 秒（快但可能不准）
   - B. < 2 秒（推荐，平衡）
   - C. < 5 秒（慢但准）
4. **第一版范围**：按上面"必做"清单做吗？还是要再加/减？
5. **预算重审**：实时话术调用 AI 很频繁，月预算 50 元可能不够。要加到多少？

---

## 6. 踩过的坑提醒（来自调研）

1. **WebRTC 自己实现很坑** — 建议用现成的（vui 已经实现）
2. **Whisper 本地化对您电脑太重** — 入门级 + 没独显，建议用云端 ASR
3. **多 agent 看着高大上但慢** — 第一版用单 agent 就够
4. **Mock-first 很重要** — 没 API 也能先跑起来（参考 sales-copilot）
5. **MIUI 14 后台** — 销售场景只打电话时活，不需要 24h 死守（之前担心的难题化解）
