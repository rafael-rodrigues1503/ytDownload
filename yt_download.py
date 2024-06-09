from pathlib import Path
import yt_dlp
import glob
import os
import re


def rename_mp3_file() -> None:
    for filename in glob.glob('*.mp3'):
        pattern = re.compile(r' [(\[](?:Remaster|Remastered|Ft|Ft\.|Feat\.|Feat|Official|\d).*[\[)]')
        fo = re.search(pattern, filename)

        if fo:
            new_filename = re.sub(pattern, '', filename)
            os.rename(filename, new_filename)
            print(f'Renamed {filename} to {new_filename}')


class YTDownload:
    def __init__(self, settings: dict, dlfolder: str = str(Path.home() / "Downloads")) -> None:
        self.settings = settings
        self.dlfolder = dlfolder
        self.links = []

    def _check_playlists(self) -> None:
        for i in range(len(self.links)):
            link = self.links[i]
            if '&list=' in link:
                video_url = link.split("&list=")[0]
                playlist = link.split("&list=")[1].split("&index=")[0]
                print(f"Download playlist {playlist}? (Y/n)")

                if input().lower() == 'n':
                    self.links[i] = video_url

    def get_links(self):
        print('Enter YouTube URLs:')
        n = 1
        while True:
            link = input(f'{n}. ')
            if not link:
                break
            self.links.append(link)
            n += 1

    def download(self) -> None:
        self._check_playlists()
        os.chdir(self.dlfolder)
        for link in self.links:
            with yt_dlp.YoutubeDL(self.settings) as ydl:
                try:
                    ydl.cache.remove()
                    ydl.download([link])
                    rename_mp3_file()
                except yt_dlp.DownloadError:
                    print(f"Couldn't download {link}")


if __name__ == "__main__":
    settings_ = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],
        'outtmpl': '/%(title)s.%(ext)s',
        'ffmpeg_location': os.path.join(os.getcwd(), 'ffmpeg.exe')
    }

    ytd = YTDownload(settings_)
    ytd.get_links()
    ytd.download()
