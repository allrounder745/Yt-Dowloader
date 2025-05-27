from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

# Make sure downloads directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # Use your exported cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
