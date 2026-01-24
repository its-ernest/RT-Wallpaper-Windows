import os
import subprocess
import webview
import time
import win32api
import threading
import logging

logging.basicConfig(
    filename='wallpaper.log',
    filemode='w',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
)

from helper import get_icon_path, load_ini
from media_server import register_media, start_media_server

# --- constants ---
BASE_DIR = os.getcwd()
ICONS_FOLDER = os.path.join(BASE_DIR, "temp_icons")
CONFIG_FILE = "config.ini"
HTML_FILE = "wallpaper.html"
GENERIC_FILE_ICON = "__file.png"
GENERIC_FOLDER_ICON = "__folder.png"

os.makedirs(ICONS_FOLDER, exist_ok=True)

config = load_ini(CONFIG_FILE)
VIDEO_PATH = config.get("video")
if not VIDEO_PATH or not os.path.exists(VIDEO_PATH):
    raise RuntimeError("Wallpaper video not configured. Run config.py first.")

threading.Thread(
    target=lambda: start_media_server(host="127.0.0.1", port=8000),
    daemon=True
).start()
time.sleep(0.5)  # allow media server to start

video_url = register_media(VIDEO_PATH)

icons_cache = []

def get_desktop_icons():
    global icons_cache
    if icons_cache:
        return icons_cache

    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    icons_cache = []

    for file in os.listdir(desktop):
        full_path = os.path.join(desktop, file)

        if os.path.isdir(full_path):
            icon_filename = GENERIC_FOLDER_ICON
        else:
            icon_path = get_icon_path(full_path)
            if os.path.exists(icon_path):
                icon_filename = os.path.basename(icon_path)
            else:
                icon_filename = GENERIC_FILE_ICON

        icon_url = f"http://127.0.0.1:8000/icons/{icon_filename}"

        icons_cache.append({
            "name": file,
            "path": full_path,
            "icon": icon_url
        })

    logging.info(f"Loaded {len(icons_cache)} icons")
    return icons_cache

class API:
    def get_icons(self):
        return get_desktop_icons()

    def get_wallpaper_video(self):
        return video_url.replace("\\", "/")

    def launch_icon(self, path):
        try:
            if not os.path.exists(path):
                subprocess.Popen(['explorer', os.path])

            if os.path.isdir(path):
                subprocess.Popen(['explorer', path])
            else:
                subprocess.Popen(f'start "" "{path}"', shell=True)
                #subprocess.Popen(['explorer', f'/select,{path}'])
        except Exception as e:
            logging.info(f"Failed to launch {path}: {e}")

    def open_file_location(self, path):
        try:
            if not os.path.exists(path):
                subprocess.Popen(['explorer', os.path])

            folder = os.path.dirname(path)
            subprocess.Popen(['explorer', folder])
        except Exception as e:
            logging.info(f"Failed to open file location for {path}: {e}")

    def open_properties(self, path):
        try:
            if not os.path.exists(path):
                subprocess.Popen(['explorer', os.path])

            subprocess.Popen(['rundll32.exe', 'shell32.dll,Options_RunDLL', path])
        except Exception as e:
            logging.info(f"Failed to open properties for {path}: {e}")

api = API()

window = webview.create_window(
    "Live Wallpaper",
    HTML_FILE,
    frameless=True,
    transparent=True,
    resizable=False,
    js_api=api,
    easy_drag=False
)

def on_loaded():
    time.sleep(0.3)
    monitor = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))["Work"]
    x, y, right, bottom = monitor
    width = right - x
    height = bottom - y

    window.move(x, y)
    window.resize(width, height)
    logging.info(f"Wallpaper window fitted to work area: {width}x{height}")

webview.start(on_loaded, debug=False)
