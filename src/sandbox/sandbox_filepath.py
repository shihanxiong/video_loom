import os
import sys

print("Current file location", os.getcwd())
print(os.path.join(os.getcwd(), "src", "output"))

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = sys._MEIPASS
    print('running in a PyInstaller bundle')
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    print('running in a normal Python process')
print("application_path=", application_path)
