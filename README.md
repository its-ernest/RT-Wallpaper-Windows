# RT-Wallpaper-Windows
## Real-Time Wallpaper for Windows

A Python application that lets you run **live, interactive wallpapers** on your Windows desktop.  
Draws directly onto the desktop using system APIs, providing a dynamic and customizable desktop experience.

---

## Demo
Watch demo:

![RT-Wallpaper Demo](assets/demo.gif) 

---

## Features
- Real-time wallpapers on Windows
- Draws dynamic content directly onto the desktop
- Lightweight web interface via Flask + PyWebview
- Image manipulation and processing using Py Win32 API and Pillow module
- Fully customizable animations and images

---

## Tech Stack
- Python 3.12.8
- [PyWebview](https://github.com/r0x0r/pywebview) – GUI layer for lightweight web UI  
- [PyWin32](https://github.com/mhammond/pywin32) – Win32 API - Desktop integration for drawing  
- [Flask](https://flask.palletsprojects.com/) – Web server to handle UI and controls  
- [Pillow](https://python-pillow.org/) – Image processing library  

---

## Installation (Prebuilt Software)
1. [Download the latest](https://github.com/its-ernest/RT-Wallpaper-Windows/releases/download/v1.0/app.zip) or select version from [Releases page](https://github.com/its-ernest/rt-wallpaper-windows/releases)
2. Extract app.zip into an empty folder.
3. Open the folder and run 'start-live.exe' to setup live wallpaper
4. Choose a video and hit Set as wallpaper
5. Click on run.

---

## Installation (From Source)
```bash
git clone https://github.com/its-ernest/rt-wallpaper-windows.git
cd rt-wallpaper-windows
pip install -r requirements.txt
python main.py
