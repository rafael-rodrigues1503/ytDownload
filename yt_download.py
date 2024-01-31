from pathlib import Path
import yt_dlp
import glob
import os
import re


def rename_files(folder: str = os.getcwd()) -> None:
    for filename in glob.glob(os.path.join(folder, '*.mp3')):
        pattern = re.compile(r' [(\[](?:Remaster|Remastered|Ft|Ft\.|Feat\.|Feat|Official|\d).*[\[)]')
        fo = re.search(pattern, filename)

        if fo:
            new_filename = re.sub(pattern, '', filename)
            os.rename(filename, new_filename)
            print(f'Renamed {filename} to {new_filename}')


class YTDownload:
    def __init__(self, settings: dict, dlfolder: str) -> None:
        self.settings = settings
        self.dlfolder = dlfolder

        os.chdir(self.dlfolder)

        self.links = []
        n = 1
        print('Enter YouTube URLs:')
        while True:
            link = input(f'{n}. ')
            if not link:
                break
            self.links.append(link)
            n += 1

        self.check_playlists()
        self.download()
        rename_files()

    def check_playlists(self) -> None:
        for i in range(len(self.links)):
            link = self.links[i]
            if '&list=' in link:
                video_url = link.split("&list=")[0]
                playlist = link.split("&list=")[1].split("&index=")[0]
                print(f"Download playlist {playlist}? (Y/N)")

                if input().lower() == 'n':
                    self.links[i] = video_url

    def download(self) -> None:
        for link in self.links:
            with yt_dlp.YoutubeDL(self.settings) as ydl:
                try:
                    ydl.cache.remove()
                    ydl.download([link])
                except yt_dlp.DownloadError:
                    print(f"Couldn't download {link}")


if __name__ == "__main__":
    dlfolder_ = str(Path.home() / "Downloads")
    settings_ = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '/%(title)s.%(ext)s'
    }

    ytd = YTDownload(settings_, dlfolder_)
