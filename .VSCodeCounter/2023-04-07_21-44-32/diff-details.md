# Diff Details

Date : 2023-04-07 21:44:32

Directory /Users/shihanxiong/dev/video_loom

Total : 54 files,  69 codes, -49 comments, 30 blanks, all 50 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 86 | 0 | 39 | 125 |
| [changelog.md](/changelog.md) | Markdown | 44 | 0 | 33 | 77 |
| [src/app.macos.spec](/src/app.macos.spec) | Ruby | 44 | 1 | 6 | 51 |
| [src/app.py](/src/app.py) | Python | 70 | 11 | 14 | 95 |
| [src/app.win32.spec](/src/app.win32.spec) | Ruby | 35 | 1 | 6 | 42 |
| [src/audio_setting_frame.py](/src/audio_setting_frame.py) | Python | 25 | 2 | 9 | 36 |
| [src/bundle.sh](/src/bundle.sh) | Shell Script | 5 | 4 | 4 | 13 |
| [src/file_utils.py](/src/file_utils.py) | Python | 15 | 0 | 5 | 20 |
| [src/sandbox/app_logging.py](/src/sandbox/app_logging.py) | Python | 16 | 2 | 7 | 25 |
| [src/sandbox/sandbox_filepath.py](/src/sandbox/sandbox_filepath.py) | Python | 3 | 0 | 2 | 5 |
| [src/sandbox/sandbox_macos.py](/src/sandbox/sandbox_macos.py) | Python | 42 | 10 | 13 | 65 |
| [src/sandbox/sandbox_win32.py](/src/sandbox/sandbox_win32.py) | Python | 21 | 4 | 7 | 32 |
| [src/settings_frame.py](/src/settings_frame.py) | Python | 20 | 4 | 7 | 31 |
| [src/status_frame.py](/src/status_frame.py) | Python | 18 | 3 | 9 | 30 |
| [src/test_file_utils.py](/src/test_file_utils.py) | Python | 4 | 0 | 3 | 7 |
| [src/test_time_utils.py](/src/test_time_utils.py) | Python | 10 | 0 | 5 | 15 |
| [src/test_timeline_utils.py](/src/test_timeline_utils.py) | Python | 47 | 3 | 14 | 64 |
| [src/time_utils.py](/src/time_utils.py) | Python | 8 | 0 | 5 | 13 |
| [src/timeline_frame.py](/src/timeline_frame.py) | Python | 22 | 3 | 9 | 34 |
| [src/timeline_utils.py](/src/timeline_utils.py) | Python | 32 | 0 | 10 | 42 |
| [src/toolbar_frame.py](/src/toolbar_frame.py) | Python | 22 | 2 | 9 | 33 |
| [src/video_frame.py](/src/video_frame.py) | Python | 145 | 24 | 38 | 207 |
| [src/video_import_frame.py](/src/video_import_frame.py) | Python | 54 | 1 | 12 | 67 |
| [src/video_renderer_frame.py](/src/video_renderer_frame.py) | Python | 30 | 3 | 7 | 40 |
| [src/video_select_frame.py](/src/video_select_frame.py) | Python | 66 | 4 | 18 | 88 |
| [src/video_setting_frame.py](/src/video_setting_frame.py) | Python | 25 | 2 | 9 | 36 |
| [src/windows.py](/src/windows.py) | Python | 6 | 0 | 1 | 7 |
| [e:/dev/github/video_loom/README.md](/e:/dev/github/video_loom/README.md) | Markdown | -83 | 0 | -36 | -119 |
| [e:/dev/github/video_loom/changelog.md](/e:/dev/github/video_loom/changelog.md) | Markdown | -36 | 0 | -25 | -61 |
| [e:/dev/github/video_loom/src/app.macos.spec](/e:/dev/github/video_loom/src/app.macos.spec) | Ruby | -44 | -1 | -6 | -51 |
| [e:/dev/github/video_loom/src/app.py](/e:/dev/github/video_loom/src/app.py) | Python | -71 | -10 | -14 | -95 |
| [e:/dev/github/video_loom/src/app.win32.spec](/e:/dev/github/video_loom/src/app.win32.spec) | Ruby | -34 | -1 | -6 | -41 |
| [e:/dev/github/video_loom/src/audio_setting_frame.py](/e:/dev/github/video_loom/src/audio_setting_frame.py) | Python | -29 | -2 | -8 | -39 |
| [e:/dev/github/video_loom/src/bundle.sh](/e:/dev/github/video_loom/src/bundle.sh) | Shell Script | -5 | -4 | -4 | -13 |
| [e:/dev/github/video_loom/src/file_utils.py](/e:/dev/github/video_loom/src/file_utils.py) | Python | -15 | 0 | -5 | -20 |
| [e:/dev/github/video_loom/src/reference/ffmpeg.py](/e:/dev/github/video_loom/src/reference/ffmpeg.py) | Python | 0 | -12 | -1 | -13 |
| [e:/dev/github/video_loom/src/reference/moviepy.py](/e:/dev/github/video_loom/src/reference/moviepy.py) | Python | 0 | -42 | -2 | -44 |
| [e:/dev/github/video_loom/src/sandbox/app_logging.py](/e:/dev/github/video_loom/src/sandbox/app_logging.py) | Python | -16 | -2 | -7 | -25 |
| [e:/dev/github/video_loom/src/sandbox/sandbox_filepath.py](/e:/dev/github/video_loom/src/sandbox/sandbox_filepath.py) | Python | -3 | 0 | -2 | -5 |
| [e:/dev/github/video_loom/src/sandbox/sandbox_macos.py](/e:/dev/github/video_loom/src/sandbox/sandbox_macos.py) | Python | -42 | -10 | -13 | -65 |
| [e:/dev/github/video_loom/src/sandbox/sandbox_win32.py](/e:/dev/github/video_loom/src/sandbox/sandbox_win32.py) | Python | -21 | -4 | -7 | -32 |
| [e:/dev/github/video_loom/src/status_frame.py](/e:/dev/github/video_loom/src/status_frame.py) | Python | -18 | -3 | -9 | -30 |
| [e:/dev/github/video_loom/src/test_file_utils.py](/e:/dev/github/video_loom/src/test_file_utils.py) | Python | -4 | 0 | -3 | -7 |
| [e:/dev/github/video_loom/src/test_time_utils.py](/e:/dev/github/video_loom/src/test_time_utils.py) | Python | -10 | 0 | -5 | -15 |
| [e:/dev/github/video_loom/src/test_timeline_utils.py](/e:/dev/github/video_loom/src/test_timeline_utils.py) | Python | -23 | -3 | -8 | -34 |
| [e:/dev/github/video_loom/src/time_utils.py](/e:/dev/github/video_loom/src/time_utils.py) | Python | -8 | 0 | -5 | -13 |
| [e:/dev/github/video_loom/src/timeline_frame.py](/e:/dev/github/video_loom/src/timeline_frame.py) | Python | -34 | -6 | -11 | -51 |
| [e:/dev/github/video_loom/src/timeline_utils.py](/e:/dev/github/video_loom/src/timeline_utils.py) | Python | -30 | 0 | -10 | -40 |
| [e:/dev/github/video_loom/src/toolbar_frame.py](/e:/dev/github/video_loom/src/toolbar_frame.py) | Python | -22 | -2 | -9 | -33 |
| [e:/dev/github/video_loom/src/video_frame.py](/e:/dev/github/video_loom/src/video_frame.py) | Python | -142 | -23 | -37 | -202 |
| [e:/dev/github/video_loom/src/video_import_frame.py](/e:/dev/github/video_loom/src/video_import_frame.py) | Python | -54 | -1 | -12 | -67 |
| [e:/dev/github/video_loom/src/video_renderer_frame.py](/e:/dev/github/video_loom/src/video_renderer_frame.py) | Python | -30 | -3 | -7 | -40 |
| [e:/dev/github/video_loom/src/video_select_frame.py](/e:/dev/github/video_loom/src/video_select_frame.py) | Python | -66 | -4 | -18 | -88 |
| [e:/dev/github/video_loom/src/windows.py](/e:/dev/github/video_loom/src/windows.py) | Python | -6 | 0 | -1 | -7 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details