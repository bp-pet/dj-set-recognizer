from src.tools import delete_folder_contents
from src.settings import raw_dir

import yt_dlp

def download_audio(url:str) -> None:
    print(f"Starting to download from {url}")
    delete_folder_contents(raw_dir)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{raw_dir}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Finished downloading")