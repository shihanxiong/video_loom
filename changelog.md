# Changelog

## v2.0.0 (unreleased)

- Complete rewrite in Wails v2 (Go + TypeScript)
- Modern web-based UI with improved UX
- Native file dialogs for video and directory selection
- Enhanced status updates with detailed progress tracking
- Improved video playback with custom HTTP handler
- Better error handling and user feedback
- Cross-platform support (macOS, Windows, Linux)

## v1.8.0

- Added support for audio concatenation
- Updated README with dependencies installation guide
- Updated bundle script to accept version as argument

## v1.7.3

- YouTube timestamp export now auto-offsets when intro is included

## v1.7.2

- Fixed issue where console windows pop up during video/audio processing on Windows

## v1.7.1

- Display error when end time exceeds video duration
- Fixed performance issue during video concatenation
- Code refactoring
  - Moved modals into separate frames

## v1.7.0

- Added support for exporting timeline in YouTube format
- Implemented dynamic sizing for modals (Windows/macOS)
- Added video list viewer with ability to remove videos from imported list
- Added support for customized intro/outro imports

## v1.6.4

- Added support for +/- 10 seconds and +/- 30 seconds control buttons

## v1.6.3

- Improved application error handling
- Combined play/pause buttons into a single toggle button

## v1.6.2

- Fixed encoder issue on macOS (use `ffmpeg encoders` to find all available encoders)
- Added support for trimming a single segment
- Fixed error when audio is shorter than output video

## v1.6.1

- Adjusted segment modal size
- FFmpeg now uses GPU acceleration instead of CPU for video trimming
- Fixed issue where audio preview doesn't play when switching audio track while video is paused

## v1.6.0

- Added application menu
- Added random timeline generation feature with:
  - Number of videos
  - Minutes per segment
  - Total number of segments

## v1.5.1

- Disabled play/pause buttons to prevent double-clicking
- Fixed issue where audio preview cannot be removed once audio mixer is loaded
- Fixed issue where filenames are not escaped during audio generation

## v1.5.0

- Updated README with updated UI documentation
- Added audio preview support while playing videos

## v1.4.3

- Updated logo design
- Enabled application resizing (allows video display to enlarge/shrink)
- Auto-display current application version from changelog
- Adjusted layout

## v1.4.2

- Display error message when timeline text is blank

## v1.4.1

- Fixed dropdown menu font size issue on Windows

## v1.4.0

- Changed audio track selection to dropdown control (list based on number of imported videos)

## v1.3.0

- Added video processing speed selection (higher speed leads to more quality loss)

## v1.2.2

- Fixed output naming issue

## v1.2.1

- Fixed issue where timeline parsed incorrectly when extra spaces or EOL characters were included

## v1.2.0

- Added logging system (all application info can be viewed in log files)
- Application no longer requires a terminal running in the background

## v1.1.0

- Added timeline validation (video processing will be skipped if timeline is invalid)

## v1.0.1

- Added user documentation

## v1.0.0

- Official release of Video Loom v1.0.0
- Auto-format current timestamp to time delta format when copying to clipboard

## v0.9.3-beta

- Fixed application portability issue on Windows (tested)
- Fixed path issue on macOS (tested)

## v0.9.2-beta

- Fixed issue where FFmpeg file path could be unidentified on Windows
- Fixed issue where long imported filenames caused rendering section to be cut off
- Bundle script now accepts specific OS spec files

## v0.9.1-beta

- Fixed issue where output video had resolution loss
- Switched from MoviePy to FFmpeg for video processing

## v0.9.0-beta

- Added time progress bar to display current video duration
- Added start time and end time display
- Added skip buttons to jump +/- 5 seconds
- Added support for copying current timestamp to clipboard

## v0.8.1-beta

- Added default resolution for Linux system (application now supports Windows, macOS, and Linux)

## v0.8.0-beta

- Application can now render up to 4 videos in preview
- Adjusted application resolution to ensure video aspect ratio is unchanged in preview

## v0.7.0-beta

- Application now supports up to 4 video tracks and 4 audio tracks
- Application can generate video splicing using timeline text

## v0.6.0-alpha

- Application can now render 2 videos simultaneously
