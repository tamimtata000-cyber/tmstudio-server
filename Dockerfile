FROM node:18-slim

# পাইথন, পিপ এবং এফএফmpeg ইনস্টল করা (যা ভিডিও প্রসেস করতে লাগে)
RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg
RUN pip3 install --no-cache-dir --upgrade yt-dlp

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD [ "node", "server.js" ]
