from __future__ import unicode_literals
from pathlib import Path
import glob
import youtube_dl
import sys
import os
import re


def yt_download(links=()):
    if not links:
        links = sys.argv[1:]

    download_folder = str(Path.home() / "Downloads")
    os.chdir(download_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '/%(title)s.%(ext)s'
    }

    if '&' in links[0]:
        print("Download playlist? (Y/N)")

        if input() == 'N':
            links = [li[:li.index('&')] for li in links]

    for link in links:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.cache.remove()
                ydl.download([link])
            except youtube_dl.DownloadError:
                pass

    for filename in glob.glob('*.mp3'):
        pattern = re.compile(r' [(\[](?:Remaster|Remastered|Ft|Ft\.|Feat\.|Feat|Official|\d).*[\[)]')
        fo = re.search(pattern, filename)

        if fo:
            new_filename = re.sub(pattern, '', filename)
            os.rename(filename, new_filename)
            print(f'Renamed {filename} to {new_filename}')


if __name__ == '__main__':
    yt_download()

# TODO: Use multithreading
