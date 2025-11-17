# scraper.py
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def scrape_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 準備輸出目錄 (確保容器內有這個資料夾)
    output_dir = "/app/data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 檔名加上日期
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{output_dir}/news_{date_str}.csv"

    story_links = soup.select(".titleline > a")
    
    print(f"開始爬取 {url} ...")
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Date"]) # Header
        
        for link in story_links[:10]: # 只抓前 10 筆示範
            title = link.get_text()
            href = link['href']
            writer.writerow([title, href, date_str])
            print(f"抓取: {title}")

    print(f"爬取完成！檔案已儲存至: {filename}")

if __name__ == "__main__":
    scrape_news()