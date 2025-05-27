from flask import Flask, request, jsonify, send_file, render_template
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [{
                'format_id': f['format_id'],
                'ext': f['ext'],
                'resolution': f.get('resolution') or f.get('height'),
                'filesize': f.get('filesize')
            } for f in info['formats'] if f.get('ext') in ['mp4', 'webm']]
        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    format_id = request.json.get('format_id')
    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': 'downloads/video.%(ext)s'
        }
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})
