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

    # yt-dlp কনফিগারেশন (সকল সোশ্যাল মিডিয়া বাইপাস করার জন্য আল্টিমেট আর্গুমেন্টস)
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'ios', 'web']}},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            
            # ফরম্যাট বা রেজুলেশনগুলো সাজানো
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
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'ভিডিও ডাটা ফেচ করা সম্ভব হয়নি। লিঙ্কটি সঠিক আছে কি না বা ভিডিওটি পাবলিক আছে কি না যাচাই করুন।'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online', 'message': 'TM.Studio Python Backend is running smoothly!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
