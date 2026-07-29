# 🎯 丐点名将

> 一款轻量级、多级随机点名工具，支持多队列管理、语音播报、主题切换，适用于课堂、会议、活动抽选。

---

## 📌 项目概览

本项目采用 **双分支** 结构：

- **`python`**（主版本）  
  基于 Python 实现的核心版本，稳定可靠，跨平台支持（Windows / Linux / macOS）。  
  采用模块化设计，包含完整的点名功能、主题切换、语音播报、配置持久化等。

- **`csharp`**（延伸版本）  
  基于 C# / WPF 重新实现的 Windows 原生版本，提供更流畅的 UI 交互体验，功能与主版本保持一致。  
  *此版本是对主版本的功能延伸，适合 Windows 用户进行分层抽选。*

---

## 🐍 Python 版本（主版本）

### ✨ 功能特性

- **多级队列管理**  
  程序从 `Assets/` 文件夹自动加载 `1.txt` 作为第1层名单，您可通过界面添加更多队列，每个队列对应独立的 `txt` 名单文件，实现灵活的多组抽选。

- **随机抽取**  
  从当前选中队列中随机抽取指定人数，结果醒目展示。

- **语音播报**  
  基于 `pyttsx3` 或系统 TTS 引擎，自动朗读被点中姓名，可一键开关。

- **主题切换**  
  支持亮色/暗色主题手动切换（`theme_manager.py`），适配不同使用环境。

- **配置持久化**  
  所有配置（队列列表、抽取人数、主题偏好、语音开关）保存在 `config.json` 中，下次启动自动恢复。

- **跨平台**  
  可在 Windows、Linux、macOS 上运行（需安装 Python 3.x 及依赖库）。

### 🛠️ 技术栈

| 组件 | 说明 |
|------|------|
| Python | 3.13 |
| GUI | PyQt |
| 语音引擎 | pyttsx3 |
| 配置存储 | JSON（内置 json 库） |
| 打包工具 | Inno Setup（`bgrd.iss`） |

### 📂 目录结构（主版本）

```
bgrd/
├── bgrd.py                 # 主程序入口
├── config_manager.py       # 配置读写（JSON）
├── theme_manager.py        # 主题管理（亮色/暗色切换）
├── voice_manager.py        # 语音播报（pyttsx3）
├── settings_dialog.py      # 设置对话框
├── asset_manager.py        # 名单文件管理
├── config.json             # 用户配置（自动生成）
├── names.txt               # 默认名单（示例）
├── dec.ico                 # 应用图标
├── bgrd.iss                # Inno Setup 安装脚本
└── Assets/                 # 存放 1.txt、2.txt…… 各层级名单
```

### 🚀 快速开始（Python）

```bash
# 克隆仓库
git clone https://github.com/bgsgp/bgrd.git
cd bgrd

# 切换到主版本分支
git checkout python

# 安装依赖（如有 requirements.txt）
pip install -r requirements.txt

# 运行
python bgrd.py
```

---

## 🖥️ C# / WPF 延伸版本（`csharp` 分支）

### ✨ 延伸特性

- **WPF 原生 UI**：基于 .NET 10 + C# 14，提供流畅、现代的 Windows 桌面体验。
- **自动主题适配**：启动时自动检测 Windows 系统主题（亮色/暗色），无需手动设置。
- **MVVM 架构**：使用 CommunityToolkit.Mvvm，逻辑与界面分离，易于维护和扩展。
- **依赖注入**：通过 Microsoft.Extensions.DependencyInjection 管理服务，提高可测试性。
- **语音引擎**：基于 System.Speech（Windows 原生），无需额外安装。

### 🛠️ 技术栈（延伸版）

| 组件 | 版本/说明 |
|------|-----------|
| .NET | 10.0 |
| C# | 14.0 |
| UI | WPF |
| MVVM | CommunityToolkit.Mvvm 8.2.2 |
| 依赖注入 | Microsoft.Extensions.DependencyInjection 8.0.0 |
| 语音引擎 | System.Speech（NuGet） |

### 🚀 快速开始（C#）

```bash
# 切换到 C# 分支
git checkout csharp

# 使用 Visual Studio 2026 打开 bgrd.sln 或 bgrd.csproj
# 或使用 .NET CLI
dotnet restore
dotnet build
dotnet run --project bgrd.csproj
```

> 详细使用说明请参考分支中的 README 或代码注释。

---

## 📊 版本对比

| 特性 | Python 版本（主） | C# / WPF 版本（延伸） |
|------|:---:|:---:|
| 开发语言 | Python | C# 14 |
| UI 框架 | Tkinter / PyQt | WPF |
| 架构模式 | 过程式 / MVC | MVVM |
| 跨平台 | ✅ Windows / Linux / macOS | ❌ 仅限 Windows |
| 原生性能 | 中等 | ✅ 高（编译执行） |
| 主题切换 | 手动 | 自动 + 手动 |
| 语音播报 | ✅ pyttsx3 | ✅ System.Speech |
| 配置存储 | JSON | JSON |
| 依赖注入 | ❌ | ✅ |
| 开发效率 | 快速迭代 | 强类型、高可靠性 |

---

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request。

- Python 主版本：修改 `python` 分支。
- WPF 延伸版本：修改 `csharp` 分支。

提交前请确保代码在对应分支上编译/运行通过，并清晰描述改动内容。

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

**Made with ❤️ by 鬼狗子Zero & 清弦-Zero**
