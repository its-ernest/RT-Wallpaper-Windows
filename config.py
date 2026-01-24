import os
import webview
from helper import load_ini, save_ini, pick_video_file

APP_NAME = "Live Wallpaper Setup"
CONFIG_FILE = "config.ini"
HTML_FILE = "config.html"

class API:
    def load_config(self):
        return load_ini(CONFIG_FILE)

    def browse_video(self):
        return pick_video_file()

    def save_config(self, video_path):
        save_ini(CONFIG_FILE, {
            "video": video_path
        })
        return True

    def close(self):
        webview.windows[0].destroy()

    def start_live(self):
        # start live 'start.exe' process
        import subprocess
        config = load_ini(CONFIG_FILE)
        video_path = config.get("video", "")
        if video_path and os.path.exists(video_path):
            subprocess.Popen(['live-ui-process.exe'], shell=True)
            return True
        return False

def main():
    api = API()

    window = webview.create_window(
        APP_NAME,
        HTML_FILE,
        width=520,
        height=320,
        resizable=False,
        frameless=False,
        js_api=api
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
