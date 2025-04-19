from src.settings import cut_dir, output_dir, save_json, shazam_timeout_seconds
from src.tools import list_files_in_directory

import json
import asyncio

from shazamio import Shazam, Serialize

completed_counter = 0
lock = asyncio.Lock()

async def recognize_all():
    file_dirs = list_files_in_directory(cut_dir)
    file_dirs = [i for i in file_dirs if '2.' in i]
    num_segments = len(file_dirs)
    print(f'Starting recognition on {num_segments} segments')
    results_all = await asyncio.gather(*[tracked_recognize_segment(f"{cut_dir}\\{file_dir}", num_segments) for file_dir in file_dirs], return_exceptions=True)

    results_final = set([r for r in results_all if not isinstance(r, Exception)])
    num_errors = sum(isinstance(r, Exception) for r in results_all)
    print(f'Recognized {num_segments - num_errors} out of {len(file_dirs)} segments')

    return set(results_final)

async def tracked_recognize_segment(path, num_segments):
    """Wrapper for keeping track of progress"""
    global completed_counter
    try:
        return await recognize_segment(path)
    except Exception as e:
        print(e)
    finally:
        async with lock:
            completed_counter += 1
            if completed_counter % 5 == 0:
                print(f"Progress: {completed_counter}/{num_segments}")


async def recognize_segment(path: str) -> str:
    shazam = Shazam() # TODO move to setup
    
    # # try with deprecated function
    # with open(path, 'rb') as f:
    #     sound_bytes = f.read()
    # out = await asyncio.wait_for(shazam.recognize_song(sound_bytes), timeout=shazam_timeout_seconds)
    
    out = await asyncio.wait_for(shazam.recognize(path), timeout=shazam_timeout_seconds)

    if save_json:
        id = path.split('.')[-2][-1]
        with open(f'{output_dir}\\shazam_output_{id}.json', 'w') as f:
            json.dump(out, f, indent=4)

    if out['matches'] == []:
        return

    track = out['track']['title']
    artist = out['track']['subtitle']
    # print(path, track, artist, '\n')
    return f'{artist} - {track}'