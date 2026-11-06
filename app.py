from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = FlaskName := Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({
            'status': 'error',
            'message': 'অনুগ্রহ করে একটি সঠিক ভিডিও লিঙ্ক প্রদান করুন।'
        }), 400

    # ফ্রি এবং বিশ্বস্ত পাবলিক ডাউনলোডার এপিআই ব্যবহার
    api_endpoint = f"https://co.wuk.sh/api/json"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0'
    }
    payload = {
        'url': video_url,
        'vQuality': '720',
        'isAudioOnly': False
    }

    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=15)
        
        # যদি এপিআই কাজ না করে বা লিমি트 শেষ হয়ে যায়
        if response.status_code != 200:
            raise Exception("API Limit Exceeded or Server Busy")
            
        data = response.json()
        
        # সফলভাবে ডেটা আসলে তা সাজিয়ে পাঠানো
        if data.get('status') == 'stream' or data.get('status') == 'redirect':
            formats = [{
                'format_id': 'best',
                'resolution': 'HD / Best Quality',
                'ext': 'mp4',
                'filesize': 'N/A',
                'url': data.get('url')
            }]
            
            return jsonify({
                'status': 'success',
                'title': data.get('filename', 'TM.Studio Download Video'),
                'thumbnail': '', # এপিআই থেকে থাম্বনেইল না আসলে ফন্টএন্ড ডিফল্ট দেখাবে
                'duration': 'N/A',
                'embedUrl': video_url,
                'formats': formats
            })
        else:
            raise Exception("Invalid response structure")

    except Exception as e:
        print(f"Server Error: {str(e)}")
        # আপনার চাওয়া সেই সুন্দর ও মার্জিত এরর ম্যাসেজ যা ইউজারদের বিরক্ত হতে দেবে না
        return jsonify({
            'status': 'error',
            'message': '⚠️ সার্ভারে ছোট্ট একটি যান্ত্রিক ত্রুটি দেখা দিয়েছে। আমরা এটি ঠিক করার কাজ করছি, দয়া করে কিছুক্ষণ ধৈর্য ধরে একটু পরে আবার চেষ্টা করুন।'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online', 'message': 'TM.Studio Smart Backend is running smoothly!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
