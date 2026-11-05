const express = require('express');
const cors = require('cors');
const { execFile } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/api/download', (req, res) => {
    const videoUrl = req.query.url;

    if (!videoUrl) {
        return res.status(400).json({ 
            status: 'error', 
            message: 'অনুগ্রহ করে একটি সঠিক ইউটিউব ভিডিও লিঙ্ক প্রদান করুন।' 
        });
    }

    // exec-এর বদলে execFile ব্যবহার করে কমান্ড ইনজেকশন রোধ ও ৩০MB পর্যন্ত বাফার হ্যান্ডলিং
    const args = ['-j', '--no-playlist', '--no-warnings', videoUrl];

    execFile('yt-dlp', args, { maxBuffer: 1024 * 1024 * 30 }, (error, stdout, stderr) => {
        if (error) {
            console.error(`yt-dlp Execution Error: ${error.message}`);
            return res.status(500).json({ 
                status: 'error', 
                message: 'ভিডিও ডাটা ফেচ করা সম্ভব হয়নি। লিঙ্কটি ঠিক আছে কিনা বা ভিডিওটি প্রাইভেট কিনা চেক করুন।' 
            });
        }

        try {
            const videoData = JSON.parse(stdout);

            const formats = (videoData.formats || []).map(f => ({
                format_id: f.format_id,
                resolution: f.format_note || f.resolution || (f.height ? `${f.height}p` : 'Unknown'),
                ext: f.ext,
                filesize: f.filesize ? (f.filesize / (1024 * 1024)).toFixed(2) + ' MB' : (f.filesize_approx ? (f.filesize_approx / (1024 * 1024)).toFixed(2) + ' MB (approx)' : 'Size N/A'),
                url: f.url
            })).filter(f => f.url);

            const responseData = {
                status: 'success',
                title: videoData.title || 'Untitled Video',
                thumbnail: videoData.thumbnail || '',
                duration: videoData.duration_string || '0:00',
                embedUrl: `https://www.youtube.com/embed/${videoData.id}`,
                formats: formats
            };

            res.json(responseData);

        } catch (parseError) {
            console.error('JSON Parse Error:', parseError);
            res.status(500).json({ 
                status: 'error', 
                message: 'সার্ভারে ডাটা প্রসেস করার সময় সমস্যা হয়েছে।' 
            });
        }
    });
});

app.get('/', (req, res) => {
    res.json({ status: 'online', message: 'TM.Studio Backend Server is running smoothly!' });
});

app.listen(PORT, () => {
    console.log(`TM.Studio Server is running on port ${PORT}`);
});
