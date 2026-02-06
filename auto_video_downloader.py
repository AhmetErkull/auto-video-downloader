import requests
import xml.etree.ElementTree as ET
import subprocess
import time
from datetime import datetime

config_file = "config.txt"

try:
    with open(config_file, "r", encoding="utf-8") as f:
        config = {key.strip(): value.strip() for key, value in (line.split(":") for line in f.readlines())}
except FileNotFoundError:
    print("There is no config file exist.")


channel_id = config["channel_id"]
rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

title_prefix = config["title_prefix"]
title_contains = config["title_contains"]
title_postfix =  config["title_postfix"]
delay = int(config["delay"])

print(f'\nChannel ID: {channel_id}\nTitle: "{title_prefix}" .. "{title_contains}" .. "{title_postfix}"\n\nDelay: {delay} seconds ({delay/3600} hours)', end="\n\n")

downloaded_file = "downloaded_videos.txt"

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

        if title.startswith(title_prefix) and title_contains in title and title.endswith(title_postfix):
            continue
        
        if title in downloaded_titles:
                print(f"The video has already been downloaded: {title}")
                break

        print(f"New video found: {title}")
        
        subprocess.run([
            r"\yt-download\yt-dlp.exe",
            "-f", "bv*+ba[ext=m4a]/b",
            "--merge-output-format", "mp4",
            "-o", r"Videos\%(title)s.%(ext)s",
            link
        ])
        
        with open(downloaded_file, "a", encoding="utf-8") as f:
            f.write(title + "\n")
            print("Video downloaded.")
        downloaded_titles.add(title)

while True:
    print(f"{datetime.now()}: Checking for new videos...")
    try:
        check_and_download()
    except Exception as e:
        print("Error occurred:", e)
    
    time.sleep(delay)

