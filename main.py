import asyncio

from src.download import download_audio
from src.cut import cut_audio
from src.recognize import recognize_all, recognize_segment

with open("url.txt", 'r') as f:
    url = f.read()

download_audio(url)
cut_audio(segment_length_seconds=10, gap_length_seconds=480)

loop = asyncio.get_event_loop()
result = loop.run_until_complete(recognize_all())
print(result)