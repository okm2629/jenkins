import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def scrape_news():
    # 改用 Google News 的 RSS Feed 網址 (這是 XML 格式，不需要 JS 渲染)
    url = "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    # 雖然是 RSS，加上 User-Agent 還是比較保險
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    # 使用 xml 解析器 (如果沒安裝 lxml，html.parser 也可以處理簡單的 RSS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 準備輸出目錄
    output_dir = "/app/data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{output_dir}/google_news_{date_str}.csv"
    html_filename = f"{output_dir}/google_news_{date_str}.html"

    print(f"開始爬取 RSS Feed: {url} ...")
    
    news_items = []
    
    # 在 RSS 中，每一則新聞都被包在 <item> 標籤裡
    items = soup.find_all('item')
    print(f"找到 {len(items)} 則新聞項目，開始處理...")
    
    for item in items:
        title = item.title.text if item.title else "No Title"
        link = item.link.text if item.link else "#"
        pub_date = item.pubdate.text if item.pubdate else ""
        
        # 簡單過濾一下廣告或空標題
        if title and link:
            news_items.append({
                "title": title, 
                "link": link,
                "date": pub_date
            })
            
        if len(news_items) >= 20: # 限制抓取前 20 則
            break

    if not news_items:
        print("警告：未找到任何新聞項目，請檢查網路或解析邏輯。")
    else:
        print(f"成功抓取 {len(news_items)} 則新聞！")

    # --- 1. 輸出 CSV ---
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "PubDate"])
        for item in news_items:
            writer.writerow([item['title'], item['link'], item['date']])
    
    print(f"CSV 儲存完畢: {csv_filename}")

    # --- 2. 輸出 HTML (Google 風格) ---
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google News Digest - {date_str}</title>
        <style>
            body {{ font-family: 'Roboto', 'Noto Sans TC', sans-serif; background-color: #f8f9fa; padding: 20px; margin: 0; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.12); border-radius: 8px; }}
            h1 {{ color: #202124; font-size: 24px; margin-bottom: 5px; display: flex; align-items: center; }}
            h1 span {{ color: #4285F4; margin-right: 5px; }}
            .timestamp {{ color: #5f6368; font-size: 0.85em; margin-bottom: 20px; border-bottom: 1px solid #e8eaed; padding-bottom: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 15px 10px; text-align: left; border-bottom: 1px solid #f1f3f4; }}
            th {{ background-color: #fff; color: #5f6368; font-weight: 500; text-transform: uppercase; font-size: 0.8em; }}
            tr:hover {{ background-color: #f8f9fa; }}
            a {{ text-decoration: none; color: #1a73e8; font-weight: 500; font-size: 1.1em; line-height: 1.4; }}
            a:hover {{ text-decoration: underline; color: #174ea6; }}
            .date {{ color: #5f6368; font-size: 0.8em; white-space: nowrap; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.8em; color: #9aa0a6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span>G</span>oogle News 台灣焦點 (RSS Source)</h1>
            <div class="timestamp">自動生成時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
            
            <table>
                <thead>
                    <tr>
                        <th width="50">#</th>
                        <th>新聞標題</th>
                        <th>發布時間</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for index, item in enumerate(news_items, 1):
        html_content += f"""
                    <tr>
                        <td>{index}</td>
                        <td><a href="{item['link']}" target="_blank">{item['title']}</a></td>
                        <td class="date">{item['date'][5:16]}</td> </tr>
        """

    html_content += """
                </tbody>
            </table>
            <div class="footer">
                Powered by Jenkins CI/CD & Docker • Automated RSS Parser
            </div>
        </div>
    </body>
    </html>
    """

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML 報表儲存完畢: {html_filename}")

if __name__ == "__main__":
    scrape_news()