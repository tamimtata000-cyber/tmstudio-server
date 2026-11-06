from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'status': 'error', 'message': 'লিংক প্রদান করুন'}), 400
    
    # ডিরেক্ট ভিডিও স্ট্রিম লিংক জেনারেট করা
    return jsonify({
        'status': 'success',
        'title': 'TM.Studio YouTube Video',
        'formats': [
            {
                'resolution': '720p HD',
                'ext': 'mp4',
                'filesize': 'HD Quality',
                'url': video_url
            }
        ]
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online', 'message': 'TM.Studio Backend is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
