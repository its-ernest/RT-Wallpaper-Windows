import os
import pythoncom
from PIL import Image
import win32gui
import win32ui
import win32con
from win32com.shell import shell

import os
import configparser
import webview
import logging

logging.basicConfig(
    filename='wallpaper.log',
    filemode='w',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
)

ICON_SIZE = 64
ICONS_FOLDER = os.path.join(os.getcwd(), "temp_icons")
os.makedirs(ICONS_FOLDER, exist_ok=True)

GENERIC_FILE_ICON = "__file.png"
GENERIC_FOLDER_ICON = "__folder.png"

def extract_icon(exe_path, save_path, size=64):
    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        hicon = None
        if large:
            hicon = large[0]
        elif small:
            hicon = small[0]
        if not hicon:
            logging.info(f"No icon found in {exe_path}")
            return False

        # --- create bitmap ---
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, size, size)
        memdc = hdc.CreateCompatibleDC()
        memdc.SelectObject(hbmp)
        memdc.FillSolidRect((0, 0, size, size), 0)

        # --- draw the icon ---
        win32gui.DrawIconEx(memdc.GetSafeHdc(), 0, 0, hicon, size, size, 0, 0, win32con.DI_NORMAL)

        # --- convert to PIL image ---
        # --- convert bitmap to PIL image correctly ---
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)

        # create PIL image directly ---
        img = Image.frombytes('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA')

        # --- resize to ICON_SIZE if needed ---
        if bmpinfo['bmWidth'] != size or bmpinfo['bmHeight'] != size:
            img = img.resize((size, size), Image.LANCZOS)

        img.save(save_path)


        # --- cleanup ---
        for h in large:
            win32gui.DestroyIcon(h)
        for h in small:
            win32gui.DestroyIcon(h)
        memdc.DeleteDC()
        hdc.DeleteDC()
        win32gui.DeleteObject(hbmp.GetHandle())
        logging.info(f"Saved icon: {save_path}")
        return True
    except Exception as e:
        logging.info(f"Failed to extract icon: {e}")
        return False

# --- resolve shortcut target ---
def resolve_shortcut(path):
    try:
        if path.lower().endswith(".lnk"):
            pythoncom.CoInitialize()

            link = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

            persist_file = link.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Load(path)
            target = link.GetPath(shell.SLGP_UNCPRIORITY)[0]
            return target if target else path
    except Exception:
        return path
    return path

# --- wrapper function --- 
def get_icon_path(full_path): 
    resolved = resolve_shortcut(full_path) 
    logging.info(f"Resolved {full_path} to {resolved}") 

    if os.path.isdir(resolved): 
        return GENERIC_FOLDER_ICON 
    
    ext = os.path.splitext(resolved)[1].lower() 
    if ext == ".exe": 
        save_path = os.path.join(ICONS_FOLDER, os.path.basename(resolved) + ".png")
        if extract_icon(resolved, save_path):
            return save_path.replace("\\", "/")
        else: 
            return GENERIC_FILE_ICON
    return GENERIC_FILE_ICON

# --- ini utils for config.py ---
def load_ini(path):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        return {}

    config.read(path)

    data = {}
    if "Wallpaper" in config:
        data.update(config["Wallpaper"])

    return data


def save_ini(path, values: dict):
    config = configparser.ConfigParser()
    config["Wallpaper"] = values

    with open(path, "w", encoding="utf-8") as f:
        config.write(f)


def pick_video_file():
    result = webview.windows[0].create_file_dialog(
        webview.OPEN_DIALOG,
        allow_multiple=False,
        file_types=("Video Files (*.mp4;*.webm;*.mkv)",)
    )

    if result:
        return result[0]
    return ""
