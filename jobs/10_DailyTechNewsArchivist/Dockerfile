# Dockerfile
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝依賴庫
RUN pip install requests beautifulsoup4 lxml

# 複製爬蟲程式到容器內
COPY scraper.py .

# 建立數據存放目錄
RUN mkdir data

# 預設執行指令
CMD ["python", "scraper.py"]