import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def scrape_news():
    # Google News 台灣版網址
    url = "https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    base_url = "https://news.google.com"

    # 偽裝成一般瀏覽器 (非常重要，否則會被 Google 擋)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # 準備輸出目錄
    output_dir = "/app/data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{output_dir}/google_news_{date_str}.csv"
    html_filename = f"{output_dir}/google_news_{date_str}.html"

    print(f"開始爬取 {url} ...")
    
    news_items = []
    # 策略：尋找所有 href 開頭為 "./articles/" 的連結
    # 這是最穩定的方法，因為 Google 的 class 名稱 (如 .JtKRv) 常常會變
    articles = soup.find_all('a', href=True)
    
    seen_titles = set() # 用來去除重複的新聞

    for link in articles:
        href = link['href']
        title = link.get_text().strip()

        # 過濾條件：
        # 1. 連結必須是新聞文章 (./articles/...)
        # 2. 標題不能為空
        # 3. 標題不能重複
        if href.startswith("./articles/") and title and title not in seen_titles:
            # 將相對路徑轉為絕對路徑 (去掉開頭的點)
            full_link = base_url + href[1:] 
            
            news_items.append({"title": title, "link": full_link})
            seen_titles.add(title)
            
            if len(news_items) >= 20: # 限制抓取前 20 則
                break

    # --- 1. 輸出 CSV ---
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Date"])
        for item in news_items:
            writer.writerow([item['title'], item['link'], date_str])
    
    print(f"CSV 儲存完畢: {csv_filename}")

    # --- 2. 輸出 HTML (Google 風格配色) ---
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
            h1 span {{ color: #4285F4; margin-right: 5px; }} /* Google Blue */
            .timestamp {{ color: #5f6368; font-size: 0.85em; margin-bottom: 20px; border-bottom: 1px solid #e8eaed; padding-bottom: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 15px 10px; text-align: left; border-bottom: 1px solid #f1f3f4; }}
            th {{ background-color: #fff; color: #5f6368; font-weight: 500; text-transform: uppercase; font-size: 0.8em; }}
            tr:hover {{ background-color: #f8f9fa; }}
            a {{ text-decoration: none; color: #1a73e8; font-weight: 500; font-size: 1.1em; line-height: 1.4; }}
            a:hover {{ text-decoration: underline; color: #174ea6; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.8em; color: #9aa0a6; }}
            .index {{ color: #5f6368; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span>G</span>oogle News 台灣焦點</h1>
            <div class="timestamp">自動生成時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
            
            <table>
                <thead>
                    <tr>
                        <th width="50">#</th>
                        <th>新聞標題</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for index, item in enumerate(news_items, 1):
        html_content += f"""
                    <tr>
                        <td class="index">{index}</td>
                        <td><a href="{item['link']}" target="_blank">{item['title']}</a></td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
            <div class="footer">
                Powered by Jenkins CI/CD & Docker • Automated Crawler
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