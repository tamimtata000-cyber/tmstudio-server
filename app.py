from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
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

    # বিকল্প এবং আরও একটি ফ্রি পাবলিক ডাউনলোডার এপিআই
    api_endpoint = "https://p.oceansaver.in/ajax/download.php"
    
    try:
        # ওশনসেভার বা অন্যান্য ফ্রি এপিআই মেথড রিকোয়েস্ট
        params = {'button': '1', 'urls': video_url, 'v': 'mp4'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0'}
        
        response = requests.get("https://loader.to/ajax/download.php", params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                download_url = data.get('download_url')
                formats = [{
                    'format_id': 'best',
                    'resolution': 'HD / Best Quality',
                    'ext': 'mp4',
                    'filesize': 'N/A',
                    'url': download_url
                }]
                
                return jsonify({
                    'status': 'success',
                    'title': 'TM.Studio Downloaded Video',
                    'thumbnail': '',
                    'duration': 'N/A',
                    'embedUrl': video_url,
                    'formats': formats
                })

        # যদি প্রথম এপিআই কাজ না করে, কোবাল্ট ব্যাকআপ এপিআই ট্রাই করা
        backup_endpoint = "https://co.wuk.sh/api/json"
        payload = {'url': video_url, 'vQuality': '720', 'isAudioOnly': False}
        backup_headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        
        backup_res = requests.post(backup_endpoint, json=payload, headers=backup_headers, timeout=15)
        if backup_res.status_code == 200:
            b_data = backup_res.json()
            if b_data.get('status') == 'stream' or b_data.get('status') == 'redirect':
                formats = [{
                    'format_id': 'best',
                    'resolution': 'HD / Best Quality',
                    'ext': 'mp4',
                    'filesize': 'N/A',
                    'url': b_data.get('url')
                }]
                return jsonify({
                    'status': 'success',
                    'title': b_data.get('filename', 'TM.Studio Video'),
                    'thumbnail': '',
                    'duration': 'N/A',
                    'embedUrl': video_url,
                    'formats': formats
                })

        raise Exception("All APIs failed")

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '⚠️ সার্ভারে ছোট্ট একটি যান্ত্রিক ত্রুটি দেখা দিয়েছে। আমরা এটি ঠিক করার কাজ করছি, দয়া করে কিছুক্ষণ ধৈর্য ধরে একটু পরে আবার চেষ্টা করুন।'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online', 'message': 'TM.Studio Multi-API Backend is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
