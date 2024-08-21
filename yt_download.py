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
    'ffmpeg_location': "D:\\Code\\ytDownload\\ffmpeg.exe"
}
dlfolder = str(Path.home() / "Downloads")


links = []
playlists = []
print("Get links from text file? (y/N)")
if input().lower() == 'y':
    # Get links from text file
    with open('D:\\Code\\ytDownload\\links.txt', 'r') as f:
        for line in f.read().split('\n'):
            links.append(line)

else:
    # Get links from user input
    print('Enter YouTube URLs:')
    n = 1
    while True:
        link = input(f'{n}. ')
        if not link:
            break
        links.append(link)
        n += 1

for i in range(len(links)):
    li = links[i]
    if '&list=' in li:
        video_url = li.split("&list=")[0]
        playlist_id = li.split("&list=")[1].split("&index=")[0]

        print(f"Download playlist {playlist_id}? (Y/n)")
        if input().lower() == 'n':
            links[i] = video_url
            continue


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
