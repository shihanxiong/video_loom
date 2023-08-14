#! /bin/bash

# original bash
# pyinstaller app.py --onefile --debug=imports --hidden-import av --hidden-import chardet --log-level=DEBUG --noconsole

# updated bash script w/ specified .spec file
if [ $# -eq 0 ] || [ $1 != "app.win32.spec" ] && [ $1 != "app.macos.spec" ]
then
  echo "Please provide a spec file (app.win32.spec | app.macos.spec)"
  exit
fi

pyinstaller $1

# save bundle.sh location as $SCRIPT_DIR
# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# e.g. convert arg v1.8.0 to 1_8_0
converted_version=$(echo "$2" | sed -e 's/^v//' -e 's/\./_/g')

if [ $1 == "app.macos.spec" ]
then
  mv dist/video_loom.app dist/macos_video_loom_$converted_version.app
  mv dist/video_loom dist/macos_video_loom_$converted_version
elif [ $1 == "app.win32.spec" ]
then
  mv dist/video_loom.exe dist/win32_video_loom_$converted_version.exe
fi


