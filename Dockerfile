FROM node:18-slim

# প্রয়োজনীয় সিস্টেম ডিপেনডেন্সি ও পাইথন প্যাকেজ ইনস্টল
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt-lists/*

# ভার্চুয়াল এনভায়রনমেন্ট তৈরি করে yt-dlp ইনস্টল ও লেটেস্ট আপডেট নিশ্চিত করা
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir --upgrade yt-dlp

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --only=production

COPY . .

EXPOSE 3000
CMD [ "node", "server.js" ]
