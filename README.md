### RT-Wallpaper-Windows
# Real Time Wallpaper For Windows (Live Wallpaper for Windows)

A Python application that lets you run **live, interactive wallpapers** on your Windows desktop.  
Draws directly onto the desktop using system APIs.

## Features
- Runs on Windows
- Draws dynamic content directly on the desktop
- Uses a lightweight web interface via Flask + PyWebview
- Supports image manipulation with Pillow

## Tech Stack
- Python 3.x
- [PyWebview](https://github.com/r0x0r/pywebview) – GUI layer
- [PyWin32](https://github.com/mhammond/pywin32) – Desktop integration
- [Flask](https://flask.palletsprojects.com/) – Web server for UI
- [Pillow](https://python-pillow.org/) – Image processing

## Installation (Prebuilt software)

## Installation (Access source code)
```bash
git clone https://github.com/its-ernest/rt-wallpaper-windows.git
cd rt-wallpaper-windows
pip install -r requirements.txt
python main.py
