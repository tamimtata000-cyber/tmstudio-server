const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// সিকিউরিটি ও ক্রস-অরিজিন পারমিশন
app.use(cors());
app.use(express.json());

// মূল ভিডিও প্রসেসিং এন্ডপয়েন্ট
app.get('/api/download', (req, res) => {
    const videoUrl = req.query.url;

    if (!videoUrl) {
        return res.status(400).json({ 
            status: 'error', 
            message: 'অনুগ্রহ করে একটি সঠিক ইউটিউব ভিডিও লিঙ্ক প্রদান করুন।' 
        });
    }

    // yt-dlp ব্যবহার করে ফাস্ট JSON ডাটা এক্সট্রাক্ট করা
    const command = `yt-dlp -j --no-playlist "${videoUrl}"`;

    exec(command, { maxBuffer: 1024 * 1024 * 15 }, (error, stdout, stderr) => {
        if (error) {
            console.error(`yt-dlp Error: ${error.message}`);
            return res.status(500).json({ 
                status: 'error', 
                message: 'ভিডিওটি লোড করা সম্ভব হয়নি। লিঙ্কটি সঠিক আছে কিনা চেক করুন অথবা সার্ভার আপডেট দিন।' 
            });
        }

        try {
            const videoData = JSON.parse(stdout);

            // ফরম্যাট ও রেজুলেশন ফিল্টার করা
            const formats = (videoData.formats || []).map(f => ({
                format_id: f.format_id,
                resolution: f.format_note || f.resolution || 'Unknown',
                ext: f.ext,
                filesize: f.filesize ? (f.filesize / (1024 * 1024)).toFixed(2) + ' MB' : 'Size N/A',
                url: f.url
            })).filter(f => f.url); // শুধু যেগুলোর ডাউনলোড লিঙ্ক আছে

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

// সার্ভার স্ট্যাটাস চেক করার রুট
app.get('/', (req, res) => {
    res.json({ status: 'online', message: 'TM.Studio Backend Server is running smoothly!' });
});

app.listen(PORT, () => {
    console.log(`TM.Studio Server is running on port ${PORT}`);
});
