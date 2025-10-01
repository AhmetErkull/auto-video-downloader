import requests
import xml.etree.ElementTree as ET
import subprocess
import time
from datetime import datetime

rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC0XZpoAPTm_1UJvFQiVg_hg"

title_prefix = "Müge Anlı ile Tatlı Sert |"
season_suffix = "- 18. Sezon"

downloaded_file = r"D:\yt-download\downloaded_videos.txt"


try:
    with open(downloaded_file, "r", encoding="utf-8") as f:
        downloaded_titles = set(line.strip() for line in f.readlines())
except FileNotFoundError:
    downloaded_titles = set()

def check_and_download():
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']

        # title format kontrolü
        if title.startswith(title_prefix) and title.endswith(season_suffix):
            if title not in downloaded_titles:
                print(f"Yeni video bulundu: {title}")
                
                subprocess.run([
                    r"D:\yt-download\yt-dlp.exe",
                    "-f", "bv*+ba[ext=m4a]/b",
                    "--merge-output-format", "mp4",
                    "-o", r"D:\movies\%(title)s.%(ext)s",
                    link
                ])
                
                with open(downloaded_file, "a", encoding="utf-8") as f:
                    f.write(title + "\n")
                    print("Video indirildi.")
                downloaded_titles.add(title)
            else:
                print(f"Video zaten indirilmiş: {title}")

while True:
    print(f"{datetime.now()}: Kontrol ediliyor...")
    try:
        check_and_download()
    except Exception as e:
        print("Hata oluştu:", e)
    
    # 1 saat bekle
    time.sleep(3600)
