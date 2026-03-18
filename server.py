import os
from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

def get_valid_cookie_file():
    cookie_path = 'cookies.txt'
    if not os.path.exists(cookie_path):
        return None
    # Dosya içeriğinin placeholder olup olmadığını kontrol edelim
    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            content = f.read(100)
            if 'This is a placeholder file' in content:
                return None
    except Exception:
        pass
    return cookie_path

def get_audio_url(url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'cookiefile': get_valid_cookie_file(),
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get('title'),
            "url": info.get('url')
        }

def get_playlist_info(url):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'cookiefile': get_valid_cookie_file(),
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = []
        for video in info.get('entries', []):
            entries.append({
                "title": video.get('title'),
                "url": video.get('url')
            })
        return entries

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    
    if not data or 'url' not in data or 'type' not in data:
        return jsonify({"error": "Missing 'url' or 'type' parameter"}), 400
    
    url = data['url']
    extract_type = data['type'] # 'link' or 'list'
    
    try:
        if extract_type == 'link':
            result = get_audio_url(url)
            return jsonify(result)
        elif extract_type == 'list':
            result = get_playlist_info(url)
            return jsonify(result)
        else:
            return jsonify({"error": "Invalid type. Use 'link' or 'list'"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Railway sets the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    print(f"Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
