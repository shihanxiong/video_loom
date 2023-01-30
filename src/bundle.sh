#! /bin/bash

pyinstaller app.py --onefile --debug=imports --hidden-import av --hidden-import chardet --log-level=DEBUG # --noconsole
