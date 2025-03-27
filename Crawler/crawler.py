import sys
import subprocess
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_vietnamese_podcasts(query="podcast việt", max_results=10):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append({"title": title, "url": f"https://www.youtube.com/watch?v={video_id}"})
    
    return videos

podcasts = search_vietnamese_podcasts(max_results=20)
# Save podcasts to a text file
with open('podcasts.txt', 'w', encoding='utf-8') as f:
    for podcast in podcasts:
        f.write(f"Title: {podcast['title']}\nURL: {podcast['url']}\n\n")

def download_youtube_podcast(video_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--write-auto-sub", "--sub-lang",  "vi,vi[auto]",
        "--convert-subs", "srt",
        "-o", f"{output_dir}/%(title)s.%(ext)s",
        video_url
    ]

    subprocess.run(command)

def download_all(links):
    for link in links:
        download_youtube_podcast(link["url"])
download_all(podcasts)

