FROM python:3.10-slim

# প্রয়োজনীয় সিস্টেম ডিপেনডেন্সি ও ffmpeg ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt-lists/*

WORKDIR /app

# পাইথন প্যাকেজ ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

# Gunicorn দিয়ে ফ্লাস্ক সার্ভার রান করা
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
