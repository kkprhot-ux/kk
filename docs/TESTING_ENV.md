# Testing Environment Setup

## What is installed

| Component | Path | Size |
|---|---|---|
| Flutter SDK 3.47.1 | `D:\flutter` | ~1.5 GB |
| Java JDK 17 (OpenJDK) | `D:\jdk-17` | 180 MB |
| Android command-line tools | `D:\Android\Sdk\cmdline-tools\latest` | 150 MB |
| Android SDK platform-tools | `D:\Android\Sdk\platform-tools` | 50 MB |
| Android build-tools 28.0.3 | `D:\Android\Sdk\build-tools\28.0.3` | 50 MB |
| Android build-tools 34.0.0 | `D:\Android\Sdk\build-tools\34.0.0` | 100 MB |
| Android platforms (34, 36) | `D:\Android\Sdk\platforms\android-{34,36}` | 200 MB |
| System image (android-34 x86_64) | `D:\Android\Sdk\system-images\android-34\google_apis\x86_64` | 1.2 GB |
| AVD "sales_test" | `C:\Users\Administrator\.android\avd\sales_test.avd` | - |

Total: ~3.5 GB

## Environment variables (set in User level)

- `ANDROID_HOME` = `D:\Android\Sdk`
- `ANDROID_SDK_ROOT` = `D:\Android\Sdk`
- `JAVA_HOME` = `D:\jdk-17`
- `Path` += `D:\jdk-17\bin; D:\flutter\bin; D:\Android\Sdk\cmdline-tools\latest\bin; D:\Android\Sdk\platform-tools`

## Flutter doctor status

```
[√] Flutter (Channel stable, 3.47.1)
[√] Windows Version (10 专业版 64-bit)
[√] Android toolchain (Android SDK version 34.0.0)
[√] Chrome
[!] Visual Studio - develop Windows apps (NOT NEEDED for mobile)
[√] Connected device (3 available)
[√] Network resources
```

## Emulator status: AVD created but cannot launch in this sandbox

The AVD `sales_test` (Android 14, Pixel, x86_64) is created and configured.
However, the emulator fails to start in the current environment (likely due
to Windows sandbox restrictions on hardware virtualization).

**Workaround: use a real device** (Xiaomi 8 Lite via USB).

## How to test on a real device

### 1. Connect the Xiaomi 8 Lite

1. Plug in USB cable
2. On the phone: enable Developer Options (tap Build Number 7 times in Settings)
3. Enable USB Debugging
4. Allow USB debugging when prompted

### 2. Verify the device is detected

```powershell
adb devices
# Should show: <serial>   device
```

### 3. Run the app

```powershell
cd D:\GPT浏览器下载\新的录音\phone_app
D:\flutter\bin\flutter.bat run
```

Flutter will:
- Build the APK
- Install it on the phone
- Launch it
- Open a debug session

### 4. Configure the app

1. Open the app on the phone
2. Go to Settings
3. Enter PC IP (find with `ipconfig`, e.g. `192.168.1.100`)
4. Save

### 5. Start a call

Dial any number. The app should auto-detect the call state and start
streaming audio to the PC.

## If you want to try the emulator anyway

1. Make sure Hyper-V is enabled in Windows Features
2. Enable Virtualization in BIOS (VT-x/AMD-V)
3. Reboot
4. Try:
   ```powershell
   $env:JAVA_HOME = "D:\jdk-17"
   D:\Android\Sdk\emulator\emulator.exe -avd sales_test -no-snapshot -no-boot-anim
   ```
5. If the emulator window appears, wait for boot, then `flutter devices` should show it