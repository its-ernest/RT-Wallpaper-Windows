import os
import mimetypes
from flask import Flask, send_file, abort
import logging

logging.basicConfig(
    filename='wallpaper.log',
    filemode='w',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
)


app = Flask(__name__)
MEDIA_MAP = {}  # video/media map
ICONS_FOLDER = os.path.join(os.getcwd(), "temp_icons")
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

def register_media(abs_path):
    abs_path = os.path.abspath(abs_path)
    key = os.path.basename(abs_path)
    MEDIA_MAP[key] = abs_path
    full_url = f"http://{SERVER_HOST}:{SERVER_PORT}/media/{key}"
    logging.info(f"Registered media: {abs_path} -> {full_url}")
    return full_url

@app.route("/media/<key>")
def serve_media(key):
    path = MEDIA_MAP.get(key)
    logging.info(f"Request for media key: {key} -> path: {path}")
    if not path or not os.path.exists(path):
        abort(404)
    
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "application/octet-stream"

    return send_file(path, mimetype=mime)

@app.route("/icons/<filename>")
def serve_icon(filename):
    path = os.path.join(ICONS_FOLDER, filename)
    if not os.path.exists(path):
        abort(404)
    
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "image/png"
    logging.info(f"Serving icon: {filename} → {path}")
    return send_file(path, mimetype=mime)

def start_media_server(host="127.0.0.1", port=5000):
    global SERVER_HOST, SERVER_PORT
    SERVER_HOST, SERVER_PORT = host, port
    logging.info(f"Starting media server at http://{host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)
