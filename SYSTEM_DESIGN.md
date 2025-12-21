# Video Loom System Design Document

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Component Structure](#component-structure)
4. [Data Flow](#data-flow)
5. [Video Processing Pipeline](#video-processing-pipeline)
6. [User Interface](#user-interface)
7. [Utilities and Services](#utilities-and-services)
8. [Platform Support](#platform-support)
9. [Dependencies](#dependencies)
10. [Testing](#testing)
11. [Packaging and Distribution](#packaging-and-distribution)
12. [Known Limitations and Technical Debt](#known-limitations-and-technical-debt)

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
- Cross-platform support (Windows, macOS)

### Technology Stack

- **GUI Framework**: Tkinter with async-tkinter-loop
- **Video Playback**: tkVideoPlayer (TkinterVideo)
- **Audio Playback**: Pygame mixer
- **Video Processing**: FFmpeg (via subprocess)
- **Packaging**: PyInstaller
- **Testing**: pytest

---

## Architecture

### High-Level Architecture

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

---

## Component Structure

### Main Application (`app.py`)

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

### UI Components

#### 1. MenuFrame (`menu_frame.py`)

- Provides application menu bar
- Menu items:
  - **File**: Exit
  - **Segment**: Create random segments, Export YouTube timestamp
- Manages modal dialogs for advanced features

#### 2. VideoFrame (`video_frame.py`)

**Core component** managing video import, playback, and processing.

**Sub-components**:

- `VideoImportFrame`: Import/clear videos, play/pause controls
- `VideoIntroOutroFrame`: Import intro/outro videos
- `VideoRendererFrame`: Multi-video display (up to 4)
- `VideoControlFrame`: Playback controls (seek, skip, timestamp)

**State Management**:

- `video_list`: List of imported video file paths (max 4)
- `intro`: Optional intro video path
- `outro`: Optional outro video path
- `trimmed_video_list`: Temporary trimmed video segments
- `output_directory`: Output file location (current working directory)
- `output_file_name`: Generated output filename (timestamp-based)
- `output_width/height`: Calculated output resolution

**Key Methods**:

- `generate_video_with_ffmpeg()`: Main video processing pipeline
- `calculate_output_resolutions()`: Determines max width/height from inputs
- `calculate_video_durations()`: Extracts duration for each video
- `process_trimmed_videos()`: Trims videos based on timeline
- `concatenate_trimmed_videos()`: Combines trimmed segments
- `process_audio()`: Extracts audio from selected video track
- `finalize_video()`: Combines video and audio
- `add_intro_outro()`: Prepends/appends intro/outro if present

#### 3. SettingsFrame (`settings_frame.py`)

Container for audio and video settings:

- `AudioSettingFrame`: Audio track selection, preview generation
- `VideoSettingFrame`: FFmpeg preset selection (processing speed)

#### 4. TimelineFrame (`timeline_frame.py`)

- Text input area for timeline specification
- Format: `video_number,start_time,end_time` (one per line)
- Example:
  ```
  1,0:00:00,0:10:00
  2,0:10:00,0:15:05
  ```

#### 5. StatusFrame (`status_frame.py`)

- Displays current processing status
- Logs status messages to both UI and log file

#### 6. ToolbarFrame (`toolbar_frame.py`)

- "Generate Video" button (enabled when videos are imported)
- "Quit" button

### Modal Dialogs

#### VideoListModalFrame (`video_list_modal_frame.py`)

- Displays imported videos, intro, and outro
- Allows removal of individual items or clearing entire list

#### CreateRandomSegmentsModalFrame (`create_random_segments_modal_frame.py`)

- Generates random timeline segments
- Parameters: number of videos, segments, minutes per segment
- Inserts generated timeline into TimelineFrame

#### ExportYoutubeTimestampModalFrame (`export_youtube_timestamp_modal_frame.py`)

- Converts timeline to YouTube timestamp format
- Allows custom labels for each video
- Handles intro offset automatically
- Copies result to clipboard

---

## Data Flow

### Video Import Flow

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

### Video Generation Flow

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

### Timeline Processing Flow

```
Timeline text input
  ↓
TimelineUtils.parse_timeline()
  → Returns: [[video_num, start, end], ...]
  ↓
TimelineUtils.validate_timeline()
  → Checks: empty, format, start < end, end <= duration
  ↓
VideoUtils.trim_mp4_by_timestamp()
  → Creates trimmed_{idx}.mp4 for each segment
  ↓
VideoUtils.concatenate_videos()
  → Combines all trimmed segments
```

---

## Video Processing Pipeline

### FFmpeg Integration

The application uses FFmpeg via subprocess calls for all video operations. FFmpeg binaries are bundled with the application:

- Windows: `ffmpeg-5.1.2/win32/ffmpeg.exe`
- macOS: `ffmpeg-5.1.2/darwin/ffmpeg`

### Processing Steps

#### 1. Video Trimming (`VideoUtils.trim_mp4_by_timestamp()`)

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

#### 2. Video Concatenation (`VideoUtils.concatenate_videos()`)

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

#### 3. Audio Extraction (`AudioUtils.generate_aac_from_mp4()`)

```bash
ffmpeg -i <video> -vn -acodec copy \
  -shortest -preset <preset> <output.aac>
```

**Key Points**:

- Extracts audio without re-encoding (`copy`)
- `-shortest` ensures output matches shortest input

#### 4. Video + Audio Combination (`VideoUtils.combine_mp4_aac_to_mp4()`)

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

The `VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264()` method translates CPU presets to GPU equivalents.

---

## User Interface

### Layout Structure

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
│ Video Display Area (1-4 videos in grid)     │
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

### Video Playback Synchronization

**Synchronization Mechanism**:

- All `TkinterVideo` instances are controlled simultaneously
- `play_all()`: Calls `play()` on all video players
- `pause_all()`: Calls `pause()` on all video players
- `seek()`: Seeks all videos to the same timestamp
- Progress slider bound to first video player's duration

**Audio Synchronization**:

- Pygame mixer plays audio preview separately
- Audio position synced with video position on seek/skip
- Audio preview generated from selected video track (MP3)

**Limitations**:

- Synchronization relies on TkinterVideo's internal timing
- No frame-perfect synchronization guarantee
- Audio preview may drift slightly from video

### Component Refresh Pattern

Components implement `refresh()` to update their state based on application data:

- Called after any state change (import, removal, etc.)
- Ensures UI consistency
- Components can enable/disable buttons, update labels, recreate widgets

---

## Utilities and Services

### VideoUtils (`video_utils.py`)

**Static Methods**:

- `get_video_duration(video)`: Returns duration in seconds (via ffprobe)
- `get_video_resolution(video)`: Returns (width, height) tuple
- `trim_mp4_by_timestamp(...)`: Trims video segment with scaling
- `concatenate_videos(...)`: Combines multiple videos
- `combine_mp4_aac_to_mp4(...)`: Merges video and audio streams
- `get_ffmpeg_preset_value_for_nvenc_h264(...)`: Maps CPU to GPU presets

### AudioUtils (`audio_utils.py`)

**Static Methods**:

- `generate_mp3_from_mp4(...)`: Creates MP3 preview (for playback)
- `generate_aac_from_mp4(...)`: Extracts AAC audio (for final video)
- `get_audio_duration(audio)`: Returns duration in seconds
- `concatenate_audios(...)`: Combines multiple audio files

### TimelineUtils (`timeline_utils.py`)

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

### TimeUtils (`time_utils.py`)

**Static Methods**:

- `get_current_date()`: Returns `YYYY_MM_DD` format
- `get_current_timestamp()`: Returns `YYYY_MM_DD_HH_MM_SS` format
- `convert_seconds_to_duration(seconds)`: Converts to `H:MM:SS` format
- `convert_duration_to_seconds(duration)`: Parses `H:MM:SS` to seconds

### FileUtils (`file_utils.py`)

**Static Methods**:

- `clean_up_temp_files()`: Removes temporary MP4, MP3, AAC files
- `escape_file_name(filename)`: Wraps filename in quotes
- `get_bundled_file_path(filename)`: Gets path in PyInstaller bundle
- `get_file_path(filename)`: Gets path in development environment
- `get_latest_version_from_changelog()`: Extracts version from changelog.md

### SysUtils (`sys_utils.py`)

**Static Methods**:

- `is_running_in_pyinstaller_bundle()`: Checks if running as executable
- `is_win32()`: Platform check for Windows
- `is_macos()`: Platform check for macOS

### Windows Utilities (`windows.py`)

- `set_dpi_awareness()`: Enables high DPI support on Windows 10+

---

## Platform Support

### Windows

**Features**:

- GPU acceleration via NVIDIA NVENC (when available)
- High DPI awareness
- Console window suppression (`CREATE_NO_WINDOW` flag)
- Window size: 1200x1100

**Requirements**:

- FFmpeg installed (or bundled)
- NVIDIA driver 522.25+ for NVENC (optional)
- Python 3.9+

**FFmpeg Commands**:

- Uses `h264_cuvid` for decoding
- Uses `h264_nvenc` for encoding
- Uses `scale_cuda` for GPU-accelerated scaling

### macOS

**Features**:

- CPU-based encoding
- Window size: 1000x900
- Native .app bundle support

**Requirements**:

- FFmpeg installed (or bundled)
- Python 3.9+

**FFmpeg Commands**:

- Standard CPU encoding (libx264)
- Standard scaling filter

### Linux (Partial Support)

**Features**:

- Basic functionality (not fully tested)
- Window size: 1000x1000

**Limitations**:

- No GPU acceleration
- May require X11/Wayland configuration

---

## Dependencies

### Core Dependencies (`requirements.txt`)

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

### External Dependencies

- **FFmpeg**: Video processing (bundled or system-installed)
- **Python 3.9+**: Runtime requirement

### Bundled Resources

- FFmpeg binaries (platform-specific)
- Application logo (app_logo.ico)
- Changelog (changelog.md)

---

## Testing

### Test Files

Located in `src/test/`:

- `test_audio_utils.py`
- `test_file_utils.py`
- `test_sys_utils.py`
- `test_time_utils.py`
- `test_timeline_utils.py`
- `test_video_utils.py`

### Test Execution

```bash
pytest -vvs
```

### Test Data

Located in `src/test/`:

- Sample video files
- Sample audio files

---

## Packaging and Distribution

### PyInstaller Configuration

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

### Build Script (`bundle.sh`)

```bash
./bundle.sh <app.win32.spec|app.macos.spec> <version>
# Example: ./bundle.sh app.win32.spec v1.9.13
```

**Process**:

1. Runs PyInstaller with specified spec file
2. Renames output with version number
3. Windows: `win32_video_loom_1_9_13.exe`
4. macOS: `macos_video_loom_1_9_13.app`

### Distribution

Executables are placed in `src/dist/` directory.

---

## Known Limitations and Technical Debt

### Current Limitations

1. **Video Synchronization**:

   - No frame-perfect synchronization guarantee
   - Relies on TkinterVideo's internal timing
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

5. **Performance**:

   - Video processing is synchronous (blocks UI)
   - No progress indication during processing
   - Large files may cause UI freezing

6. **Platform Support**:
   - Linux support is minimal
   - No ARM macOS support (Intel-only)

### Technical Debt

1. **Code Organization**:

   - Some utility methods could be consolidated (e.g., `get_video_duration` and `get_audio_duration`)
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

4. **Documentation**:

   - Limited inline documentation
   - No API documentation
   - Some methods have TODO comments

5. **Configuration**:

   - Hardcoded values (max videos, window sizes)
   - No configuration file support
   - No user preferences persistence

6. **Async Operations**:
   - Video processing blocks main thread
   - No background task management
   - Limited use of async-tkinter-loop

### Recommended Improvements for v2

1. **Architecture**:

   - Separate business logic from UI (MVC/MVP pattern)
   - Implement proper async/await for video processing
   - Add progress reporting system

2. **Platform Support**:

   - Unified GPU acceleration detection
   - Better cross-platform path handling
   - ARM macOS support

3. **User Experience**:

   - Progress bars for video processing
   - Better error messages
   - Undo/redo functionality
   - Project save/load

4. **Code Quality**:

   - Comprehensive test coverage
   - Type hints throughout
   - Consistent error handling
   - Configuration management

5. **Performance**:
   - Background video processing
   - Caching of video metadata
   - Optimized FFmpeg command generation

---

## Conclusion

Video Loom v1 is a functional desktop application for video editing with a component-based architecture. The system effectively handles multi-video import, synchronized playback, and timeline-based video generation using FFmpeg. While the current implementation works well for its intended use case, there are opportunities for improvement in architecture, error handling, and user experience for v2.
