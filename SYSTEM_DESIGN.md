# Video Loom System Design Document

## Table of Contents

1. [Overview](#overview)
2. [Version Comparison](#version-comparison)
3. [Video Loom v1 (Python/Tkinter)](#video-loom-v1-pythontkinter)
   - [Architecture](#v1-architecture)
   - [Component Structure](#v1-component-structure)
   - [Data Flow](#v1-data-flow)
   - [User Interface](#v1-user-interface)
   - [Utilities and Services](#v1-utilities-and-services)
   - [Dependencies](#v1-dependencies)
   - [Testing](#v1-testing)
   - [Packaging and Distribution](#v1-packaging-and-distribution)
4. [Video Loom v2 (Go/Wails)](#video-loom-v2-gowails)
   - [Architecture](#v2-architecture)
   - [Component Structure](#v2-component-structure)
   - [Data Flow](#v2-data-flow)
   - [User Interface](#v2-user-interface)
   - [Utilities and Services](#v2-utilities-and-services)
   - [Dependencies](#v2-dependencies)
   - [Testing](#v2-testing)
   - [Packaging and Distribution](#v2-packaging-and-distribution)
5. [Video Processing Pipeline](#video-processing-pipeline)
6. [Platform Support](#platform-support)
7. [Known Limitations and Technical Debt](#known-limitations-and-technical-debt)

---

## Overview

Video Loom is a desktop application designed to trim and combine multiple video files based on timestamp specifications. The application supports up to 4 simultaneous video inputs, allows synchronized playback, and generates a final composite video with selected audio tracks.

### Key Features

- Import and preview up to 4 video files simultaneously
- Synchronized multi-video playback with audio preview
- Timeline-based video trimming and concatenation
- Custom intro/outro support
- GPU-accelerated video processing (Windows)
- Random segment generation
- YouTube timestamp export
- Cross-platform support (Windows, macOS, Linux)

---

## Version Comparison

| Aspect               | v1 (Python/Tkinter)          | v2 (Go/Wails)                           |
| -------------------- | ---------------------------- | --------------------------------------- |
| **Backend**          | Python 3.9+                  | Go 1.18+                                |
| **Frontend**         | Tkinter                      | TypeScript/HTML/CSS                     |
| **Framework**        | async-tkinter-loop           | Wails v2                                |
| **Video Playback**   | tkVideoPlayer (TkinterVideo) | HTML5 Video Element                     |
| **Audio Playback**   | Pygame mixer                 | Browser Audio API                       |
| **Video Processing** | FFmpeg (subprocess)          | FFmpeg (exec.Command)                   |
| **Packaging**        | PyInstaller                  | Wails build system                      |
| **Testing**          | pytest                       | Go testing + frontend tests             |
| **State Management** | Component refresh pattern    | Thread-safe Go struct with mutex        |
| **Status Updates**   | Direct UI updates            | Polling-based status updates            |
| **Output Directory** | Current working directory    | User-selectable (defaults to Downloads) |

---

## Video Loom v1 (Python/Tkinter)

### V1 Architecture

The application follows a **component-based architecture** with a clear separation between:

- **UI Components** (Frames and Modals)
- **Business Logic** (Utils classes)
- **Platform Abstraction** (SysUtils, Windows-specific code)

```
┌─────────────────────────────────────────────────────────┐
│                    VideoLoom (Main App)                 │
│                  (tk.Tk - Root Window)                  │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼─────────────────┐
        │                   │                 │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│  MenuFrame     │  │ VideoFrame  │  │ SettingsFrame   │
│  (Menu Bar)    │  │ (Main Area) │  │ (Audio/Video)   │
└────────────────┘  └──────┬──────┘  └─────────────────┘
                            │
        ┌───────────────────┼──────────────────┐
        │                   │                  │
┌───────▼────────┐  ┌──────▼───────┐  ┌────────▼────────┐
│ TimelineFrame  │  │ StatusFrame  │  │ ToolbarFrame    │
│ (Text Input)   │  │ (Status Bar) │  │ (Actions)       │
└────────────────┘  └──────────────┘  └─────────────────┘
```

### Component Interface Pattern

All UI components inherit from `ComponentInterface`, which provides:

- `refresh()` method (abstract, must be implemented)
- Common button manipulation methods
- File selection dialogs

This ensures consistent behavior across all components and enables the app-wide refresh mechanism.

### V1 Component Structure

#### Main Application (`app.py`)

**VideoLoom** class extends `tk.Tk` and serves as the root window:

- **Initialization**:

  - Configures window size based on platform (Windows: 1200x1100, macOS: 1000x900)
  - Sets up logging (file + console handlers)
  - Initializes all component frames
  - Registers components for refresh mechanism

- **Key Methods**:

  - `app_configure()`: Platform-specific window configuration
  - `app_refresh()`: Refreshes all registered components

- **Component Registration**:
  Components are stored in a list and refreshed in order:
  1. MenuFrame
  2. VideoFrame
  3. SettingsFrame
  4. TimelineFrame
  5. StatusFrame
  6. ToolbarFrame

#### UI Components

1. **MenuFrame** (`menu_frame.py`)

   - Provides application menu bar
   - Menu items: File (Exit), Segment (Create random segments, Export YouTube timestamp)
   - Manages modal dialogs for advanced features

2. **VideoFrame** (`video_frame.py`)

   - **Core component** managing video import, playback, and processing
   - **Sub-components**:
     - `VideoImportFrame`: Import/clear videos, play/pause controls
     - `VideoIntroOutroFrame`: Import intro/outro videos
     - `VideoRendererFrame`: Multi-video display (up to 4)
     - `VideoControlFrame`: Playback controls (seek, skip, timestamp)
   - **State Management**:
     - `video_list`: List of imported video file paths (max 4)
     - `intro`: Optional intro video path
     - `outro`: Optional outro video path
     - `trimmed_video_list`: Temporary trimmed video segments
     - `output_directory`: Output file location (current working directory)
     - `output_file_name`: Generated output filename (timestamp-based)
     - `output_width/height`: Calculated output resolution
   - **Key Methods**:
     - `generate_video_with_ffmpeg()`: Main video processing pipeline
     - `calculate_output_resolutions()`: Determines max width/height from inputs
     - `calculate_video_durations()`: Extracts duration for each video
     - `process_trimmed_videos()`: Trims videos based on timeline
     - `concatenate_trimmed_videos()`: Combines trimmed segments
     - `process_audio()`: Extracts audio from selected video track
     - `finalize_video()`: Combines video and audio
     - `add_intro_outro()`: Prepends/appends intro/outro if present

3. **SettingsFrame** (`settings_frame.py`)

   - Container for audio and video settings:
     - `AudioSettingFrame`: Audio track selection, preview generation
     - `VideoSettingFrame`: FFmpeg preset selection (processing speed)

4. **TimelineFrame** (`timeline_frame.py`)

   - Text input area for timeline specification
   - Format: `video_number,start_time,end_time` (one per line)
   - Example:
     ```
     1,0:00:00,0:10:00
     2,0:10:00,0:15:05
     ```

5. **StatusFrame** (`status_frame.py`)

   - Displays current processing status
   - Logs status messages to both UI and log file

6. **ToolbarFrame** (`toolbar_frame.py`)
   - "Generate Video" button (enabled when videos are imported)
   - "Quit" button

#### Modal Dialogs

- **VideoListModalFrame** (`video_list_modal_frame.py`): Displays imported videos, intro, and outro; allows removal
- **CreateRandomSegmentsModalFrame** (`create_random_segments_modal_frame.py`): Generates random timeline segments
- **ExportYoutubeTimestampModalFrame** (`export_youtube_timestamp_modal_frame.py`): Converts timeline to YouTube format

### V1 Data Flow

#### Video Import Flow

```
User clicks "Import videos"
  ↓
VideoImportFrame.select_files()
  ↓
VideoFrame.video_list.append(filenames)
  ↓
app_refresh() → All components refresh
  ↓
VideoRendererFrame creates TkinterVideo instances
  ↓
Videos displayed in grid layout
```

#### Video Generation Flow

```
User clicks "Generate Video"
  ↓
VideoFrame.generate_video_with_ffmpeg()
  ↓
1. Clean up temp files
2. Calculate output resolution (max width/height)
3. Calculate video durations
4. Validate timeline
5. Process trimmed videos (FFmpeg)
6. Concatenate trimmed videos (if > 1 segment)
7. Extract audio from selected track
8. Combine video + audio
9. Add intro/outro (if present)
  ↓
Status updates throughout process
  ↓
Final video saved to output directory
```

### V1 User Interface

#### Layout Structure

```
┌─────────────────────────────────────────────┐
│ Menu Bar (File, Segment)                    │
├─────────────────────────────────────────────┤
│ Video Import Controls                       │
│ [Import] [View List] [Play/Pause]           │
├─────────────────────────────────────────────┤
│ Intro/Outro Controls                        │
│ [Add Intro] [Add Outro]                     │
├─────────────────────────────────────────────┤
│ Video Display Area (1-4 videos in grid)    │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│ │Video1│ │Video2│ │Video3│ │Video4│         │
│ └──────┘ └──────┘ └──────┘ └──────┘         │
├─────────────────────────────────────────────┤
│ Video Controls                              │
│ [0:00:00] [━━━━━━━━━━━━━━━━] [0:10:00]      │
│ [-30s] [-10s] [-5s] [+5s] [+10s] [+30s]     │
│ [Copy Timestamp]                            │
├─────────────────────────────────────────────┤
│ Settings                                    │
│ Audio: [Track ▼] [Generate Preview] [...]   │
│ Video: [Process Speed ▼]                    │
├─────────────────────────────────────────────┤
│ Timeline (Text Input)                       │
│ ┌─────────────────────────────────────────┐ │
│ │ 1,0:00:00,0:10:00                       │ │
│ │ 2,0:10:00,0:15:05                       │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ Status: ready                               │
├─────────────────────────────────────────────┤
│ [Generate Video] [Quit]                     │
└─────────────────────────────────────────────┘
```

#### Video Playback Synchronization

- All `TkinterVideo` instances are controlled simultaneously
- `play_all()`: Calls `play()` on all video players
- `pause_all()`: Calls `pause()` on all video players
- `seek()`: Seeks all videos to the same timestamp
- Progress slider bound to first video player's duration
- Pygame mixer plays audio preview separately
- Audio position synced with video position on seek/skip

### V1 Utilities and Services

#### VideoUtils (`video_utils.py`)

**Static Methods**:

- `get_video_duration(video)`: Returns duration in seconds (via ffprobe)
- `get_video_resolution(video)`: Returns (width, height) tuple
- `trim_mp4_by_timestamp(...)`: Trims video segment with scaling
- `concatenate_videos(...)`: Combines multiple videos
- `combine_mp4_aac_to_mp4(...)`: Merges video and audio streams
- `get_ffmpeg_preset_value_for_nvenc_h264(...)`: Maps CPU to GPU presets

#### AudioUtils (`audio_utils.py`)

**Static Methods**:

- `generate_mp3_from_mp4(...)`: Creates MP3 preview (for playback)
- `generate_aac_from_mp4(...)`: Extracts AAC audio (for final video)
- `get_audio_duration(audio)`: Returns duration in seconds
- `concatenate_audios(...)`: Combines multiple audio files

#### TimelineUtils (`timeline_utils.py`)

**Static Methods**:

- `parse_timeline(timeline_text)`: Parses text into array of [video, start, end]
- `validate_timeline(timeline_text, video_durations)`: Validates format and bounds
- `generate_random_segments(...)`: Creates random timeline segments
- `generate_youtube_timestamp(...)`: Converts timeline to YouTube format

**Validation Rules**:

- Timeline cannot be empty
- Format: `video_number,start_time,end_time`
- Start time must be before end time
- End time cannot exceed video duration
- Video number must be valid (1-4)

#### TimeUtils (`time_utils.py`)

**Static Methods**:

- `get_current_date()`: Returns `YYYY_MM_DD` format
- `get_current_timestamp()`: Returns `YYYY_MM_DD_HH_MM_SS` format
- `convert_seconds_to_duration(seconds)`: Converts to `H:MM:SS` format
- `convert_duration_to_seconds(duration)`: Parses `H:MM:SS` to seconds

#### FileUtils (`file_utils.py`)

**Static Methods**:

- `clean_up_temp_files()`: Removes temporary MP4, MP3, AAC files
- `escape_file_name(filename)`: Wraps filename in quotes
- `get_bundled_file_path(filename)`: Gets path in PyInstaller bundle
- `get_file_path(filename)`: Gets path in development environment
- `get_latest_version_from_changelog()`: Extracts version from changelog.md

#### SysUtils (`sys_utils.py`)

**Static Methods**:

- `is_running_in_pyinstaller_bundle()`: Checks if running as executable
- `is_win32()`: Platform check for Windows
- `is_macos()`: Platform check for macOS

#### Windows Utilities (`windows.py`)

- `set_dpi_awareness()`: Enables high DPI support on Windows 10+

### V1 Dependencies

#### Core Dependencies (`requirements.txt`)

```
freezegun          # Time mocking for tests
pytest             # Testing framework
pytest-mock        # Mocking utilities
pygame             # Audio playback
tkvideoplayer      # Video playback widget
pyinstaller        # Application packaging
tkinter-tooltip    # Tooltip support
async-tkinter-loop # Async event loop for Tkinter
```

#### External Dependencies

- **FFmpeg**: Video processing (bundled or system-installed)
- **Python 3.9+**: Runtime requirement

#### Bundled Resources

- FFmpeg binaries (platform-specific)
- Application logo (app_logo.ico)
- Changelog (changelog.md)

### V1 Testing

#### Test Files

Located in `video_loom_v1/src/`:

- `test_audio_utils.py`
- `test_file_utils.py`
- `test_sys_utils.py`
- `test_time_utils.py`
- `test_timeline_utils.py`
- `test_video_utils.py`

#### Test Execution

```bash
pytest -vvs
```

### V1 Packaging and Distribution

#### PyInstaller Configuration

**Windows** (`app.win32.spec`):

- One-file executable
- Bundles FFmpeg, changelog, logo
- Console disabled
- UPX compression enabled

**macOS** (`app.macos.spec`):

- Creates .app bundle
- Bundles FFmpeg, changelog, logo
- Console disabled
- UPX compression enabled

#### Build Script (`bundle.sh`)

```bash
./bundle.sh <app.win32.spec|app.macos.spec> <version>
# Example: ./bundle.sh app.win32.spec v1.9.13
```

**Process**:

1. Runs PyInstaller with specified spec file
2. Renames output with version number
3. Windows: `win32_video_loom_1_9_13.exe`
4. macOS: `macos_video_loom_1_9_13.app`

#### Distribution

Executables are placed in `video_loom_v1/src/dist/` directory.

---

## Video Loom v2 (Go/Wails)

### V2 Architecture

The application follows a **client-server architecture** with clear separation between:

- **Backend (Go)**: Business logic, state management, FFmpeg operations
- **Frontend (TypeScript)**: UI components, user interactions, video playback
- **Communication**: Wails bindings (automatic Go ↔ TypeScript bridge)

```
┌─────────────────────────────────────────────────────────┐
│                    Wails Application                    │
│              (Native Desktop Window)                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼─────────────────┐
        │                   │                 │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│   Frontend     │  │   Wails     │  │   Backend       │
│  (TypeScript)  │◄─┤  Bindings   │─►│     (Go)        │
│  HTML/CSS      │  │  (Bridge)   │  │  app.go         │
└────────────────┘  └─────────────┘  └────────┬────────┘
                                               │
                               ┌───────────────┼───────────────┐
                               │               │               │
                    ┌──────────▼───┐  ┌──────▼────┐  ┌──────▼────┐
                    │  VideoUtils   │  │ AudioUtils │  │TimelineUtils│
                    │  FileUtils    │  │  TimeUtils │  │  SysUtils  │
                    └───────────────┘  └────────────┘  └────────────┘
```

### V2 Component Structure

#### Main Application (`main.go`)

**Entry Point**:

- Initializes Wails application
- Configures window (1200x1100)
- Sets up asset server with video file serving middleware
- Binds Go `App` struct to frontend
- Handles video file serving via HTTP endpoint (`/video?path=...`)

#### Backend Service (`app.go`)

**App struct** manages all application state and business logic:

- **State Management**:

  - `videoList`: List of imported video file paths (max 4)
  - `intro`: Optional intro video path
  - `outro`: Optional outro video path
  - `audioTrack`: Selected audio track (1-4)
  - `ffmpegPreset`: FFmpeg encoding preset
  - `timelineText`: Timeline specification text
  - `status`: Current processing status
  - `outputDir`: Output directory (defaults to Downloads)
  - `outputFileName`: Generated output filename

- **Thread Safety**:

  - All state access protected by `sync.RWMutex`
  - Read locks for getters, write locks for setters

- **Key Methods**:
  - `OpenVideoDialog()`: Native file dialog for video selection
  - `AddVideos()`: Adds videos to list (max 4)
  - `RemoveVideo()`: Removes video by index
  - `ClearVideoList()`: Clears all videos and intro/outro
  - `SetIntro()`/`SetOutro()`: Sets intro/outro video paths
  - `GetVideoInfo()`: Returns video duration and resolution
  - `GetVideoDurations()`: Returns durations for all videos
  - `ValidateTimeline()`: Validates timeline against video durations
  - `GenerateRandomSegments()`: Generates random timeline segments
  - `GenerateYouTubeTimestamp()`: Converts timeline to YouTube format
  - `GenerateAudioPreview()`: Creates MP3 preview from selected track
  - `GenerateVideo()`: Main video processing pipeline
  - `SelectOutputDirectory()`: Opens directory selection dialog
  - `OpenOutputDirectory()`: Opens output directory in file manager

#### Frontend Application (`frontend/src/app.ts`)

**App class** manages UI state and user interactions:

- **State Management**:

  - `videoList`: Local copy of video list
  - `videoPlayers`: Array of HTML5 video elements
  - `isPlaying`: Playback state
  - `currentTime`: Current playback position
  - `maxDuration`: Maximum video duration
  - `audioTrack`: Selected audio track
  - `ffmpegPreset`: Selected FFmpeg preset
  - `outputDirectorySelected`: Whether output directory is set

- **Key Methods**:
  - `init()`: Initializes application, loads state, sets up UI
  - `setupUI()`: Creates HTML structure
  - `setupEventListeners()`: Binds event handlers
  - `importVideos()`: Opens file dialog and imports videos
  - `renderVideoPlayers()`: Creates HTML5 video elements for each video
  - `playAll()`/`pauseAll()`: Controls synchronized playback
  - `seek()`/`skip()`: Video seeking controls
  - `generateVideo()`: Initiates video generation
  - `showVideoListModal()`: Displays video list modal
  - `showRandomSegmentsModal()`: Displays random segments modal
  - `showYouTubeTimestampModal()`: Displays YouTube timestamp modal
  - `startStatusUpdates()`: Polls backend status every second

#### UI Components

1. **Video Import Section**

   - Import Videos button
   - View Video List button (shows count)
   - Play/Pause All Videos button
   - Add Intro/Outro buttons

2. **Video Preview Section**

   - Grid layout for up to 4 videos
   - HTML5 video elements with controls
   - Video labels (Video 1, Video 2, etc.)

3. **Video Controls Section**

   - Time display (current/total)
   - Progress slider
   - Skip buttons (-30s, -10s, -5s, +5s, +10s, +30s)
   - Copy Timestamp button

4. **Settings Section**

   - Audio Track selector (1-4)
   - Generate/Remove Audio Preview buttons
   - FFmpeg Preset selector

5. **Timeline Section**

   - Textarea for timeline input
   - Validate Timeline button
   - Create Random Segments button
   - Export YouTube Timestamp button

6. **Status Section**

   - Status text display (polled from backend)

7. **Toolbar Section**
   - Select Output Directory button
   - Generate Video button
   - Open Output Folder button
   - Quit button
   - Output directory path display

#### Modal Dialogs

- **Video List Modal**: Displays all videos, intro, and outro with remove buttons
- **Random Segments Modal**: Inputs for number of videos, segments, and minutes per segment
- **YouTube Timestamp Modal**: Input fields for video labels, copy to clipboard

### V2 Data Flow

#### Video Import Flow

```
User clicks "Import Videos"
  ↓
Frontend: OpenVideoDialog() (Wails binding)
  ↓
Go: runtime.OpenMultipleFilesDialog()
  ↓
User selects files
  ↓
Go: AddVideos(paths)
  ↓
Frontend: refreshVideoList()
  ↓
Frontend: renderVideoPlayers()
  ↓
HTML5 video elements created with /video?path=... URLs
  ↓
Videos displayed in grid layout
```

#### Video Generation Flow

```
User clicks "Generate Video"
  ↓
Frontend: GenerateVideo() (Wails binding)
  ↓
Go: GenerateVideo()
  ↓
1. Clean up temp files
2. Calculate output resolution (max width/height)
3. Get video durations
4. Validate timeline
5. Parse timeline
6. Trim videos (with progress updates)
7. Concatenate trimmed videos (if > 1 segment)
8. Extract audio from selected track
9. Combine video + audio
10. Add intro/outro (if present)
  ↓
Status updates via SetStatus()
  ↓
Frontend polls GetStatus() every second
  ↓
Final video saved to output directory
```

#### Status Updates Flow

```
Backend: SetStatus("Processing...")
  ↓
Frontend: startStatusUpdates() (interval every 1s)
  ↓
Frontend: GetStatus() (Wails binding)
  ↓
Go: GetStatus() returns current status
  ↓
Frontend: Updates status text in UI
```

### V2 User Interface

#### Layout Structure

The v2 UI uses a modern web-based layout with CSS styling:

```
┌─────────────────────────────────────────────┐
│ Header: Video Loom [Version]               │
├─────────────────────────────────────────────┤
│ Video Import Section                       │
│ [Import Videos] [View List (0/4)] [Play]   │
│ [Add Intro] [Add Outro]                     │
├─────────────────────────────────────────────┤
│ Video Preview Section (Grid Layout)        │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │
│ │Video1│ │Video2│ │Video3│ │Video4│       │
│ └──────┘ └──────┘ └──────┘ └──────┘       │
├─────────────────────────────────────────────┤
│ Video Controls                             │
│ [-30s] [-10s] [-5s] [0:00:00] [━━━━] [0:10:00] [+5s] [+10s] [+30s] │
│ [Copy Timestamp]                           │
├─────────────────────────────────────────────┤
│ Settings                                   │
│ Audio: [Track ▼] [Generate Preview] [Remove Preview] │
│ Process Speed: [Preset ▼]                  │
├─────────────────────────────────────────────┤
│ Timeline                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ 1,0:00:00,0:10:00                       │ │
│ │ 2,0:10:00,0:15:05                       │ │
│ └─────────────────────────────────────────┘ │
│ [Validate] [Random Segments] [YouTube Export]│
├─────────────────────────────────────────────┤
│ Status: ready                               │
├─────────────────────────────────────────────┤
│ [Select Output Directory] [Generate Video] │
│ [Open Output Folder] [Quit]                 │
│ Output Directory: ~/Downloads               │
└─────────────────────────────────────────────┘
```

#### Video Playback Synchronization

- All HTML5 video elements controlled via JavaScript
- `playAll()`: Calls `play()` on all video players
- `pauseAll()`: Calls `pause()` on all video players
- `seek()`: Sets `currentTime` on all videos
- Progress slider bound to first video's duration
- Time updates from first video's `timeupdate` event

#### Video File Serving

- Videos served via HTTP endpoint: `/video?path=<encoded_path>`
- Middleware validates file existence
- Sets appropriate headers for video streaming
- Supports range requests for seeking

### V2 Utilities and Services

All utilities are implemented in Go under `internal/utils/`:

#### VideoUtils (`video.go`)

**Methods**:

- `GetVideoDuration(videoPath)`: Returns duration in seconds (via ffprobe)
- `GetVideoResolution(videoPath)`: Returns width, height, error
- `TrimMP4ByTimestamp(...)`: Trims video segment with scaling
- `ConcatenateVideos(...)`: Combines multiple videos
- `CombineMP4AACToMP4(...)`: Merges video and audio streams
- `GetFFmpegPresetValueForNVENCH264(...)`: Maps CPU to GPU presets

#### AudioUtils (`audio.go`)

**Methods**:

- `GenerateMP3FromMP4(...)`: Creates MP3 preview (for playback)
- `GenerateAACFromMP4(...)`: Extracts AAC audio (for final video)
- `GetAudioDuration(audioPath)`: Returns duration in seconds
- `ConcatenateAudios(...)`: Combines multiple audio files

#### TimelineUtils (`timeline.go`)

**Methods**:

- `ParseTimeline(timelineText)`: Parses text into array of Segment structs
- `ValidateTimeline(timelineText, durations)`: Validates format and bounds
- `GenerateRandomSegments(...)`: Creates random timeline segments
- `GenerateYouTubeTimestamp(...)`: Converts timeline to YouTube format

**Segment struct**:

```go
type Segment struct {
    Video int    // Video number (1-4)
    Start string // Start time (H:MM:SS)
    End   string // End time (H:MM:SS)
}
```

#### TimeUtils (`time.go`)

**Methods**:

- `GetCurrentDate()`: Returns `YYYY_MM_DD` format
- `GetCurrentTimestamp()`: Returns `YYYY_MM_DD_HH_MM_SS` format
- `ConvertSecondsToDuration(seconds)`: Converts to `H:MM:SS` format
- `ConvertDurationToSeconds(duration)`: Parses `H:MM:SS` to seconds

#### FileUtils (`file.go`)

**Methods**:

- `CleanUpTempFiles()`: Removes temporary MP4, MP3, AAC files
- `EscapeFileName(filename)`: Wraps filename in quotes
- `GetLatestVersionFromChangelog(path)`: Extracts version from changelog.md

#### SysUtils (`sys.go`)

**Methods**:

- `IsWin32()`: Platform check for Windows
- `IsMacOS()`: Platform check for macOS
- `IsLinux()`: Platform check for Linux

**Process Attributes**:

- `sysproc.go`: Windows-specific process attributes (CREATE_NO_WINDOW)
- `sysproc_unix.go`: Unix-specific process attributes

### V2 Dependencies

#### Backend Dependencies (`go.mod`)

- **Wails v2**: Desktop application framework
- **Standard Go libraries**: `os`, `os/exec`, `path/filepath`, `sync`, `time`, `context`, `fmt`

#### Frontend Dependencies (`frontend/package.json`)

- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Wails bindings**: Auto-generated TypeScript bindings for Go methods

#### External Dependencies

- **FFmpeg**: Video processing (system-installed, not bundled)
- **Go 1.18+**: Runtime requirement
- **Node.js 16+**: Frontend build requirement

### V2 Testing

#### Test Files

Located in `video_loom_v2/internal/utils/`:

- `audio_test.go`
- `file_test.go`
- `sys_test.go`
- `time_test.go`
- `timeline_test.go`
- `video_test.go`
- `test_helpers.go`: Shared test utilities

#### Test Execution

```bash
# Run all tests
go test ./...

# Run tests with verbose output
go test -v ./...

# Run specific test
go test -v ./internal/utils -run TestFunctionName
```

### V2 Packaging and Distribution

#### Wails Build Configuration (`wails.json`)

```json
{
  "name": "video_loom_v2",
  "outputfilename": "video_loom_v2",
  "frontend:install": "npm install",
  "frontend:build": "npm run build",
  "frontend:dev:watcher": "npm run dev"
}
```

#### Build Commands

**Development**:

```bash
wails dev
```

**Production Build**:

```bash
wails build
```

**Output**:

- macOS: `build/bin/video_loom_v2.app`
- Windows: `build/bin/video_loom_v2.exe`
- Linux: `build/bin/video_loom_v2`

#### Build Process

1. Frontend build: `npm run build` (TypeScript → JavaScript, bundles assets)
2. Go compilation: Compiles Go code with embedded frontend assets
3. Platform-specific packaging:
   - macOS: Creates .app bundle with Info.plist
   - Windows: Creates .exe with manifest
   - Linux: Creates binary executable

---

## Video Processing Pipeline

### FFmpeg Integration

Both v1 and v2 use FFmpeg via subprocess/exec calls for all video operations:

- **v1**: FFmpeg binaries bundled with application

  - Windows: `ffmpeg-5.1.2/win32/ffmpeg.exe`
  - macOS: `ffmpeg-5.1.2/darwin/ffmpeg`

- **v2**: FFmpeg must be system-installed (not bundled)

### Processing Steps

#### 1. Video Trimming

**Windows (GPU-accelerated)**:

```bash
ffmpeg -hwaccel cuvid -c:v h264_cuvid -i <input> \
  -c:v h264_nvenc -ss <start> -to <end> \
  -vf scale_cuda=<width>:<height> \
  -c:a copy -preset <preset> <output>
```

**macOS/Linux (CPU)**:

```bash
ffmpeg -i <input> -ss <start> -to <end> \
  -vf scale=<width>:<height> \
  -c:a copy -preset <preset> <output>
```

**Key Points**:

- Windows uses NVIDIA GPU acceleration (NVENC) when available
- All videos scaled to maximum resolution found in input videos
- Audio stream copied (no re-encoding)

#### 2. Video Concatenation

```bash
ffmpeg -i <video1> -i <video2> ... \
  -filter_complex concat=n=<count>:v=1:a=1 \
  -c:v libx264 -c:a aac \
  -preset <preset> -vsync 2 <output>
```

**Key Points**:

- Uses FFmpeg concat filter
- Re-encodes video (libx264) and audio (aac)
- `vsync 2` ensures frame rate consistency

#### 3. Audio Extraction

```bash
ffmpeg -i <video> -vn -acodec copy \
  -shortest -preset <preset> <output.aac>
```

**Key Points**:

- Extracts audio without re-encoding (`copy`)
- `-shortest` ensures output matches shortest input

#### 4. Video + Audio Combination

```bash
ffmpeg -i <video> -i <audio> \
  -c:v copy -map 0:v -map 1:a \
  -shortest -preset <preset> <output>
```

**Key Points**:

- Video stream copied (no re-encoding)
- Audio stream mapped from separate file
- `-shortest` ensures synchronization

### Resolution Handling

The application automatically determines output resolution:

1. Iterates through all imported videos
2. Uses `ffprobe` to get width/height of each
3. Sets output resolution to maximum width and maximum height
4. All trimmed segments scaled to this resolution

### Preset System

FFmpeg presets control encoding speed vs. quality:

- **CPU presets**: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
- **GPU presets (NVENC)**: fast, medium, slow (mapped from CPU presets)

The `VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264()` / `GetFFmpegPresetValueForNVENCH264()` method translates CPU presets to GPU equivalents.

---

## Platform Support

### Windows

**Features**:

- GPU acceleration via NVIDIA NVENC (when available)
- High DPI awareness (v1 only)
- Console window suppression (`CREATE_NO_WINDOW` flag)
- Window size: 1200x1100

**Requirements**:

- FFmpeg installed (v2) or bundled (v1)
- NVIDIA driver 522.25+ for NVENC (optional)
- Python 3.9+ (v1) or Go 1.18+ (v2)

**FFmpeg Commands**:

- Uses `h264_cuvid` for decoding
- Uses `h264_nvenc` for encoding
- Uses `scale_cuda` for GPU-accelerated scaling

### macOS

**Features**:

- CPU-based encoding
- Window size: 1000x900 (v1) or 1200x1100 (v2)
- Native .app bundle support

**Requirements**:

- FFmpeg installed (system-installed for v2, bundled for v1)
- Python 3.9+ (v1) or Go 1.18+ (v2)

**FFmpeg Commands**:

- Standard CPU encoding (libx264)
- Standard scaling filter

### Linux

**Features**:

- Basic functionality (v2 fully supported, v1 minimal)
- Window size: 1000x1000 (v1) or 1200x1100 (v2)

**Limitations**:

- No GPU acceleration
- May require X11/Wayland configuration

**Requirements**:

- FFmpeg installed
- Python 3.9+ (v1) or Go 1.18+ (v2)

---

## Known Limitations and Technical Debt

### Current Limitations

1. **Video Synchronization**:

   - No frame-perfect synchronization guarantee
   - v1: Relies on TkinterVideo's internal timing
   - v2: Relies on HTML5 video element timing
   - Audio preview may drift from video

2. **GPU Acceleration**:

   - Only available on Windows with NVIDIA GPUs
   - No fallback detection (assumes NVENC available)
   - No CPU/GPU toggle option

3. **Video Format Support**:

   - Primarily designed for MP4 files
   - No format validation on import

4. **Error Handling**:

   - Some operations may fail silently
   - Limited user feedback on FFmpeg errors
   - v2: Better error propagation via Wails bindings

5. **Performance**:

   - Video processing is synchronous (blocks UI)
   - v2: Status polling provides better feedback
   - Large files may cause UI freezing

6. **Platform Support**:
   - v1: Linux support is minimal
   - v1: No ARM macOS support (Intel-only)
   - v2: Full Linux support
   - v2: ARM macOS support (via Go cross-compilation)

### Technical Debt

#### v1 Specific

1. **Code Organization**:

   - Some utility methods could be consolidated
   - Modal frames not following ComponentInterface pattern
   - Hardcoded paths in spec files

2. **Error Handling**:

   - Inconsistent error handling patterns
   - Some methods return None on error, others raise exceptions
   - Limited error recovery mechanisms

3. **Testing**:

   - No integration tests
   - Limited UI testing
   - No FFmpeg operation tests

4. **Configuration**:

   - Hardcoded values (max videos, window sizes)
   - No configuration file support
   - No user preferences persistence

5. **Async Operations**:
   - Video processing blocks main thread
   - No background task management
   - Limited use of async-tkinter-loop

#### v2 Specific

1. **Frontend**:

   - Status polling could be replaced with events/websockets
   - No audio preview playback in browser
   - Video file serving could be optimized

2. **Error Handling**:

   - Could provide more detailed error messages
   - Better error recovery mechanisms needed

3. **Testing**:

   - Frontend tests not yet implemented
   - Integration tests needed
   - E2E tests needed

4. **Configuration**:

   - No user preferences persistence
   - Output directory selection could be remembered

5. **Performance**:
   - Video processing still blocks (could use goroutines)
   - No progress percentage, only status messages

### Recommended Improvements

1. **Architecture**:

   - v2: Implement event-based status updates instead of polling
   - v2: Use goroutines for video processing to avoid blocking
   - Add progress reporting system with percentages

2. **Platform Support**:

   - Unified GPU acceleration detection
   - Better cross-platform path handling
   - ARM macOS support (v2 already supports via Go)

3. **User Experience**:

   - Progress bars for video processing
   - Better error messages
   - Undo/redo functionality
   - Project save/load

4. **Code Quality**:

   - Comprehensive test coverage
   - Consistent error handling
   - Configuration management
   - Better documentation

5. **Performance**:
   - Background video processing (v2: use goroutines)
   - Caching of video metadata
   - Optimized FFmpeg command generation

---

## Conclusion

Video Loom is a functional desktop application for video editing available in two versions:

- **v1 (Python/Tkinter)**: Mature, stable version with component-based architecture. Well-tested and production-ready.

- **v2 (Go/Wails)**: Modern rewrite with improved architecture, better separation of concerns, and cross-platform support. Uses web technologies for UI, providing a more modern user experience.

Both versions effectively handle multi-video import, synchronized playback, and timeline-based video generation using FFmpeg. The v2 architecture provides a better foundation for future improvements with its client-server model, thread-safe state management, and modern web-based UI.
