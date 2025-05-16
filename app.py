from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

@app.route('/', methods=['GET', 'POST'])
def index():
    video_path = None
    error = None
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            error = "Please enter a valid URL."
        else:
            try:
                video_id = str(uuid.uuid4())
                output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.%(ext)s")
                ydl_opts = {
                    'outtmpl': output_path,
                    'format': 'best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.download([url])
                    # Get actual file path
                    downloaded_file = ydl.prepare_filename(ydl.extract_info(url, download=False))
                    video_path = downloaded_file
            except Exception as e:
                error = f"Download failed: {e}"

    return render_template('index.html', video_path=video_path, error=error)

@app.route('/download')
def download():
    path = request.args.get('path')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
