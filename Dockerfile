FROM node:18-slim

# প্রয়োজনীয় সিস্টেম ডিপেনডেন্সি ও পাইথন ইনস্টল
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt-lists/*

# ভার্চুয়াল এনভায়রনমেন্ট তৈরি করা
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# পাইথন এবং সেটআপ টুলস আপডেট করা
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# সরাসরি গিটহাব থেকে yt-dlp এর একদম লেটেস্ট মাস্টার ভার্সন ইনস্টল করা (বট প্রটেকশন বাইপাস করার জন্য)
RUN pip install --no-cache-dir --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --only=production

COPY . .

EXPOSE 3000
CMD [ "node", "server.js" ]
