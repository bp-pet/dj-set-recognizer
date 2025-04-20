import asyncio

from src.download import download_audio
from src.cut import cut_audio
from src.recognize import run_recognize
from src.tools import read_target_url

# Don't forget to make a url.txt in root and put the URL in it!
url = read_target_url()

# download_audio(url)

# cut_audio(segment_length_seconds=10, gap_length_seconds=60)

run_recognize()