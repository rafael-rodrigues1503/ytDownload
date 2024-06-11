from pathlib import Path
import yt_dlp
import glob
import os
import re


settings = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320'
    }],
    'outtmpl': '/%(title)s.%(ext)s',
    'ffmpeg_location': os.path.join(os.getcwd(), 'ffmpeg.exe')
}
dlfolder = str(Path.home() / "Downloads")

# Get links from user input
links = []
playlists = []
print('Enter YouTube URLs:')
n = 1
while True:
    link = input(f'{n}. ')
    if not link:
        break

    if '&list=' in link:
        video_url = link.split("&list=")[0]
        playlist = link.split("&list=")[1].split("&index=")[0]

        print(f"Download playlist {playlist}? (Y/n)")
        if input().lower() == 'n':
            links.append(video_url)
            n += 1
            continue

    links.append(link)
    n += 1

# Download the songs
os.chdir(dlfolder)
for link in links:
    with yt_dlp.YoutubeDL(settings) as ydl:
        try:
            ydl.cache.remove()
            ydl.download([link])
        except yt_dlp.DownloadError:
            print(f"Couldn't download {link}")

# Rename .mp3 files
for filename in glob.glob('*.mp3'):
    pattern = re.compile(r' [(\[](?:Remaster|Remastered|Ft|Ft\.|Feat\.|Feat|Official|\d).*[\[)]')
    fo = re.search(pattern, filename)

    if fo:
        new_filename = re.sub(pattern, '', filename)
        os.rename(filename, new_filename)
        print(f'Renamed {filename} to {new_filename}')