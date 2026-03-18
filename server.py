from flask import Flask, request, jsonify
from link import get_audio_url
from service import get_playlist_info

app = Flask(__name__)

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
    print("Server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
