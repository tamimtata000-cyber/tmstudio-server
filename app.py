from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({
            'status': 'error',
            'message': 'অনুগ্রহ করে একটি সঠিক ভিডিও লিঙ্ক প্রদান করুন।'
        }), 400

    # ইউটিউবের আইপি ব্লকিং এবং বট প্রটেকশন সম্পূর্ণ বাইপাস করার আল্টিমেট কনফিগারেশন
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
                'skip': ['hls', 'dash']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'socket_timeout': 30,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            
            formats = []
            for f in info_dict.get('formats', []):
                if f.get('url'):
                    filesize = f.get('filesize') or f.get('filesize_approx')
                    size_str = f"{filesize / (1024 * 1024):.2f} MB" if filesize else "Size N/A"
                    
                    formats.append({
                        'format_id': f.get('format_id'),
                        'resolution': f.get('format_note') or f.get('resolution') or f"{f.get('height', 'Unknown')}p",
                        'ext': f.get('ext'),
                        'filesize': size_str,
                        'url': f.get('url')
                    })

            response_data = {
                'status': 'success',
                'title': info_dict.get('title', 'Untitled Video'),
                'thumbnail': info_dict.get('thumbnail', ''),
                'duration': info_dict.get('duration_string', '0:00'),
                'embedUrl': f"https://www.youtube.com/embed/{info_dict.get('id')}" if 'youtube.com' in video_url or 'youtu.be' in video_url else video_url,
                'formats': formats
            }

            return jsonify(response_data)

    except Exception as e:
        print(f"Detailed Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'ইউটিউব সার্ভার থেকে ডাটা ব্লক করা হয়েছে। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online', 'message': 'TM.Studio Ultimate Backend is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
