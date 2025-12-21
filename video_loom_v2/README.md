# Video Loom v2

A modern desktop application for trimming and combining videos, built with Wails v2 (Go + TypeScript).

## Quick Start

### Installation

Run the installation script to install all dependencies:

```bash
./install.sh
```

This script will:

- Check for required dependencies (Go, Node.js, npm, Wails CLI)
- Install missing dependencies where possible
- Install Go modules
- Install frontend npm packages
- Generate Wails bindings
- Optionally install FFmpeg (required for video processing)

### Manual Installation

If you prefer to install dependencies manually:

#### System Requirements

- **Go**: 1.18 or later ([Download](https://go.dev/dl/))
- **Node.js**: 16 or later ([Download](https://nodejs.org/))
- **npm**: Comes with Node.js
- **Wails CLI**: `go install github.com/wailsapp/wails/v2/cmd/wails@latest`
- **FFmpeg**: Required for video processing
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg` or `sudo yum install ffmpeg`
  - Windows: `choco install ffmpeg-full`

#### Install Dependencies

```bash
# Install Go dependencies
go mod download
go mod tidy

# Install frontend dependencies
cd frontend
npm install
cd ..

# Generate Wails bindings
wails generate module
```

## Development

### Run in Development Mode

```bash
wails dev
```

This will:

- Start the development server
- Watch for file changes
- Hot reload the frontend
- Show debug information

### Build for Production

```bash
wails build
```

This will create a production build in `build/bin/`:

- macOS: `video_loom_v2.app`
- Windows: `video_loom_v2.exe`
- Linux: `video_loom_v2`

## Project Structure

```
video_loom_v2/
├── app.go                 # Main application service
├── main.go                # Application entry point
├── install.sh             # Installation script
├── internal/
│   └── utils/             # Utility packages
│       ├── time.go        # Time utilities
│       ├── file.go        # File utilities
│       ├── sys.go         # System utilities
│       ├── timeline.go    # Timeline utilities
│       ├── video.go       # Video processing
│       └── audio.go       # Audio processing
└── frontend/
    ├── src/
    │   ├── main.ts        # Frontend entry point
    │   ├── app.ts         # Main application logic
    │   ├── app.css        # Application styles
    │   └── style.css      # Base styles
    └── package.json       # Frontend dependencies
```

## Features

- 🎬 Import and preview up to 4 video files simultaneously
- ▶️ Synchronized multi-video playback
- ✂️ Timeline-based video trimming and concatenation
- 🎞️ Custom intro/outro support
- ⚡ GPU-accelerated video processing (Windows with NVIDIA)
- 🎲 Random segment generation
- 📋 YouTube timestamp export
- 💻 Cross-platform support (Windows, macOS, Linux)

## Usage

1. **Import Videos**: Click "Import Videos" and select up to 4 video files
2. **Play Videos**: Use "Play All Videos" to start synchronized playback
3. **Create Timeline**: Enter timeline segments in the format:
   ```
   1,0:00:00,0:10:00
   2,0:10:00,0:15:05
   ```
4. **Generate Video**: Click "Generate Video" to create the final output

## Troubleshooting

### FFmpeg Not Found

If you see errors about FFmpeg not being found:

- Ensure FFmpeg is installed and in your PATH
- Verify installation: `ffmpeg -version`
- Reinstall if needed using the methods above

### Wails CLI Not Found

If `wails` command is not found:

- Ensure Go is installed and `$GOPATH/bin` or `$HOME/go/bin` is in your PATH
- Reinstall: `go install github.com/wailsapp/wails/v2/cmd/wails@latest`

### Build Errors

If you encounter build errors:

- Ensure all dependencies are installed: `./install.sh`
- Clean and rebuild: `wails build -clean`
- Check Go and Node.js versions meet requirements

## License

See the main project README for license information.
