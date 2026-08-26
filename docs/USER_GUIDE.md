# 用户手册 - 实时销售辅助 App

## 5 分钟设置

### 第一步：电脑端准备

1. 安装 Python 3.11+ (推荐 3.12)
2. 进入 `pc_service/` 目录
3. 跑 `pip install -r requirements.txt`
4. 复制 `.env.example` 为 `.env`
5. 填入您的 API 凭证:
   - `DEEPSEEK_API_KEY` — 从 https://platform.deepseek.com 获取
   - `XUNFEI_APP_ID` / `XUNFEI_API_KEY` / `XUNFEI_API_SECRET` — 从 https://www.xfyun.cn 获取
6. 跑 `python main.py` 启动电脑端

### 第二步：手机端安装

1. 安装 Flutter (见 README)
2. 安装 Android Studio + Android SDK
3. 进入 `phone_app/` 目录
4. 跑 `flutter pub get`
5. 用 USB 连接手机
6. 跑 `flutter run`

### 第三步：连接配置

1. 打开 App
2. 进入"设置"页
3. 填入电脑 IP 地址（如 192.168.1.100）
4. 点击"测试连接"确认通

## 5 分钟使用

### 打电话时

1. 用手机拨打电话或接听来电
2. App 自动检测 → 进入"通话中"界面
3. **客户说话 → AI 实时分析 → 屏幕显示推荐话术**（< 2 秒）
4. 您照着话术念

### 通话结束后

1. 挂断电话
2. App 自动生成复盘
3. 查看 5 维度分析:
   - 一句话总结
   - 客户关注点
   - 主要异议
   - 情绪曲线
   - 待改进点
4. 查看后续行动清单

## 常见问题

**Q: AI 话术不准确怎么办？**
A: DeepSeek 模型会随版本更新。第一版用 deepseek-chat (便宜)，第二版可切 deepseek-reasoner (更准)。

**Q: 实时话术推荐有延迟怎么办？**
A: 检查家里 WiFi 信号、电脑是否在睡眠、ASR API 配额。

**Q: 通话录音会不会泄露？**
A: 不会。音频在手机端只临时缓存，转文字后立刻丢弃。文字永久留在您本地电脑。

**Q: 能换其他 AI 模型吗？**
A: 可以。`pc_service/server/llm_service.py` 是 OpenAI 兼容接口，换其他模型只需改 `BASE_URL` 和 `model`。