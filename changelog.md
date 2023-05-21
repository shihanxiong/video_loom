# Versions

### v1.6.3

- improved app error handling
- combined play / pause buttons into a single button

### v1.6.2

- fix the encoder issue on macos (use `ffmpeg encoders` to find all availabe encoders)
- now allows trimming a single segment
- fix the error when audio is shorter than output.mp4

### v1.6.1

- adjusted segment modal size
- ffmpeg now uses GPU acceleration instead of CPU for video trimming
- fixed an issue when video is paused, switching audio track does not play the audio preview

### v1.6.0

- added application menu
- now application supports random :game_die: timeline generation with
  - number of videos
  - minutes per segment
  - total number of segments

### v1.5.1

- application now disables play / pause buttons to dis-allow double clicking
- fixed the issue where removing audio preview is not allowed once audio mixer is loaded
- fixed the issue when filenames are not escaped while generating audios

### v1.5.0

- updated readme w/ updated UI
- application now supports audio preview while playing videos

### v1.4.3

- newer logo design
- enabled app resizing, this will allow videos display to enlarge/shrink
- auto displays current application version per changelog
- adjusted layout

### v1.4.2

- shows error message when timeline text is blank

### v1.4.1

- fixed the dropdown menu font size issue in windows system

### v1.4.0

- audio track selection is now a dropdown control, the list in the dropdown is based on the number of videos imported

### v1.3.0

- now allows user to select a video processing speed (higher speed leads to more quality loss)

### v1.2.2

- fixed a output naming issue

### v1.2.1

- fixed the issue when timeline parse incorrectly when extra spaces / EOL were included

### v1.2.0

- added logging system, now all app info can be viewed in the log files
- application will no longer have a terminal running the background

### v1.1.0

- added timeline validation (video processing will be skipped if timeline is invalid)

### v1.0.1

- :file_folder: added user documentation

### v1.0.0

- :loudspeaker: official release of video loom v1.0.0
- when copy the current timestamp, auto-formats to time delta format

### v0.9.3-beta

- solved the app portability issue in Win32 (:heavy_check_mark: win32 tested)
- fixed path issue on macOS (:heavy_check_mark: macOS tested)

### v0.9.2-beta

- fixed the issue when ffmpeg file path could be unidentified in Win32
- fixed the issue when imported filenames are too long that caused rendering section to be cutoff
- bundle script now accepts specific os spec files

### v0.9.1-beta

- fixed the issue when the output video has resolution loss
- using ffmpeg instead of moviepy for video processing

### v0.9.0-beta

- added time progress bar to display current video duration
- added start time / end time
- added skip buttons to jump +/- 5 seconds
- added support to copy current timestamp into clipboard

### v0.8.1-beta

- added default resolution for Linux system (now app supports Win, MacOS, and Linux)

### v0.8.0-beta

- application now can render up to 4 videos in preview
- adjusted app resolution to ensure video ratio is unchanged in preview

### v0.7.0-beta

- application now supports up to 4 video tracks + 4 audio tracks
- application can generate video splicing using timeline text

### v0.6.0-alpha

- application now can only render 2 videos simutaneously
