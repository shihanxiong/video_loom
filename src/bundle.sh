#! /bin/bash

# original bash
# pyinstaller app.py --onefile --debug=imports --hidden-import av --hidden-import chardet --log-level=DEBUG --noconsole

# updated bash script w/ specified .spec file
if [ $# -eq 0 ]; then
  echo "Please provide a spec file (app.win32.spec | app.macos.spec)"
  exit
fi

pyinstaller $1
