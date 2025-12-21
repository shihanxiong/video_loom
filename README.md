# Video Loom

<p align="center">
  <img src="./img/app_logo.png" width="450" height="450" alt="Video Loom Logo" />
</p>

<p align="center">
  <strong>A portable, multi-platform application for trimming and combining videos</strong>
</p>

## Overview

Video Loom is a desktop application that helps you trim and combine multiple video files based on timestamp specifications. Perfect for scenarios where you have multiple cameras shooting simultaneously—Video Loom can cut these videos by timestamps and combine them into a single dynamic final product.

### Key Features

- 🎬 Import and preview up to 4 video files simultaneously
- ▶️ Synchronized multi-video playback with audio preview
- ✂️ Timeline-based video trimming and concatenation
- 🎞️ Custom intro/outro support
- ⚡ GPU-accelerated video processing (Windows with NVIDIA)
- 🎲 Random segment generation
- 📋 YouTube timestamp export
- 💻 Cross-platform support (Windows, macOS)

## Table of Contents

- [Overview](#overview)
- [System Design](#system-design)
- [Prerequisites](#prerequisites)
- [User Guide](#user-guide)
- [Development](#development)
- [Testing](#testing)
- [Packaging](#packaging)
- [Changelog](#changelog)

## System Design

For a detailed technical analysis of the codebase architecture, components, data flow, and implementation details, see [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md).

The system design document covers:

- Architecture overview and component structure
- Video processing pipeline and FFmpeg integration
- User interface layout and component interactions
- Platform-specific implementations (Windows, macOS)
- Utilities and services
- Known limitations and recommendations for v2

## Prerequisites

Before using Video Loom, ensure the following software is installed on your local machine.

### Windows

- **Package Manager**: [Chocolatey](https://chocolatey.org/)
- **Video Processing**: FFmpeg
- **GPU Acceleration** (optional): NVIDIA driver 522.25 or newer for NVENC support
- **Python**: v3.9+ (for development)

### macOS

- **Video Processing**: FFmpeg
- **Python**: v3.9+ (for development)

### Installation Instructions

#### Windows

**Install Chocolatey:**

1. Open PowerShell with administrator access
2. Run the following command:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

**Install FFmpeg:**

1. Open PowerShell with administrator access
2. Run:

   ```powershell
   choco install ffmpeg-full
   ```

3. Verify installation by running `ffmpeg` in a new terminal (should display version information)

#### macOS

**Install FFmpeg:**

```bash
brew install ffmpeg
```

## User Guide

### Getting Started

1. **Download the Application**

   - Download the `.exe` (Windows) or `.app` (macOS) file from the [releases](https://github.com/shihanxiong/video_loom/tree/main/src/dist)
   - Launch the application

2. **Import Videos**

   - Click the **"Import videos"** button
   - Select up to 4 video files (`.mp4` format)
   - Videos will appear in the preview area

   <img src="./img/user_guide_1.png" width="450" height="450" alt="Import videos interface" />

3. **Playback Controls**

   - Click **"Play all videos"** to start synchronized playback
   - Use skip buttons (-30s, -10s, -5s, +5s, +10s, +30s) to navigate
   - Click **"Pause all videos"** to pause playback

4. **Audio Preview (Optional)**

   - Select an audio track from the dropdown (1-4, corresponding to imported videos)
   - Click **"Generate preview"** under Audio Settings
   - Wait for the preview to generate
   - Audio will play synchronized with video playback

   <img src="./img/user_guide_3.png" width="450" height="450" alt="Audio settings interface" />

5. **Create Timeline**

   - In the timeline text box, enter video segments in the format: `video_number,start_time,end_time`
   - Each segment on a new line
   - Example:

     ```text
     1,0:00:00,0:10:00
     2,0:10:00,0:15:05
     ```

   <img src="./img/user_guide_2.png" width="450" height="450" alt="Timeline input interface" />

6. **Generate Final Video**
   - Select the audio track for the final video
   - (Optional) Add intro/outro videos
   - Click **"Generate Video"**
   - The output file will be saved as `.mp4` with a timestamp-based filename

### Timeline Format

The timeline uses a simple text format:

```
video_number,start_time,end_time
```

- **video_number**: 1-4 (corresponding to imported videos)
- **start_time**: Start timestamp in `H:MM:SS` format
- **end_time**: End timestamp in `H:MM:SS` format

**Example:**

```text
1,0:00:00,0:10:00
2,0:10:00,0:15:05
3,0:15:05,0:20:30
```

This creates a video with:

- 0:00:00 to 0:10:00 from video 1
- 0:10:00 to 0:15:05 from video 2
- 0:15:05 to 0:20:30 from video 3

## Development

### Quick Setup

Run the installation script to install all dependencies for both v1 and v2:

```bash
./install.sh
```

The script will:

- Check for required dependencies (Python, Go, Node.js, FFmpeg)
- Install missing dependencies where possible
- Install Python packages for v1
- Install Go modules and npm packages for v2
- Generate Wails bindings for v2

### Manual Setup

#### Video Loom v1 (Python/Tkinter)

1. **Clone the repository**

   ```bash
   git clone https://github.com/shihanxiong/video_loom.git
   cd video_loom
   ```

2. **Install dependencies**

   ```bash
   # Ensure Python 3.9+ is installed
   cd video_loom_v1
   pip3 install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   cd video_loom_v1/src
   python3 app.py
   ```

4. **Run tests**

   ```bash
   cd video_loom_v1/src
   python3 -m pytest test_*.py -vvs
   ```

#### Video Loom v2 (Wails/Go)

See [video_loom_v2/README.md](video_loom_v2/README.md) for detailed v2 setup instructions.

### Windows (WSL2) Setup

For development on Windows using WSL2, you'll need to configure X11 forwarding:

1. **Install Xming**

   - Download and install [Xming](https://sourceforge.net/projects/xming/)

2. **Configure XLaunch**

   - Launch XLaunch
   - Follow the setup wizard
   - For `Additional parameters for VcXsrv`, enter: `-ac`

   <img src="./img/xlaunch_1.png" width="400" height="300" alt="XLaunch configuration 1" />
   <img src="./img/xlaunch_2.png" width="400" height="300" alt="XLaunch configuration 2" />
   <img src="./img/xlaunch_3.png" width="400" height="300" alt="XLaunch configuration 3" />

3. **Set DISPLAY variable**

   - Find your Windows IP address:

     ```bash
     cat /etc/resolv.conf
     # Look for nameserver IP (e.g., 172.27.176.1)
     ```

   - Export DISPLAY variable:

     ```bash
     export DISPLAY=172.27.176.1:0
     ```

4. **VS Code Configuration (Optional)**

   - Configure `code-runner` to run in terminal:
     - Set `"code-runner.runInTerminal": true` in `settings.json`
     - Set Python command to `python3 -m`

   <img src="./img/vscode_1.png" width="450" height="320" alt="VS Code configuration" />

   > **Note**: If you encounter `$DISPLAY` errors, ensure you've exported the DISPLAY variable in your VS Code terminal.

## Testing

### Video Loom v1

Run the test suite:

```bash
cd video_loom_v1/src
python3 -m pytest test_*.py -vvs
```

Test files are located in `video_loom_v1/src/` and cover utility functions for audio, video, timeline, file operations, and system utilities.

### Video Loom v2

Tests for v2 are pending (see [video_loom_v2/README.md](video_loom_v2/README.md)).

## Packaging

### Video Loom v1

Build platform-specific executables using PyInstaller:

```bash
cd video_loom_v1/src
./bundle.sh <app.win32.spec | app.macos.spec> <version>
```

**Examples:**

```bash
# Windows
./bundle.sh app.win32.spec v1.9.13

# macOS
./bundle.sh app.macos.spec v1.9.13
```

**Output:**

- Windows: `dist/win32_video_loom_1_9_13.exe`
- macOS: `dist/macos_video_loom_1_9_13.app`

> **Note**: Executables are automatically determined by the OS (`.exe` for Windows, `.app` for macOS)

### Video Loom v2

Build using Wails:

```bash
cd video_loom_v2
wails build
```

See [video_loom_v2/README.md](video_loom_v2/README.md) for details.

## Changelog

See [changelog.md](changelog.md) for version history and release notes.
