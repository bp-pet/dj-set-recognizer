from src.settings import cut_dir, output_dir, shazam_timeout_seconds, use_deprecated_recognize
from src.tools import list_files_in_directory

import os
import json
import asyncio
from tqdm.asyncio import tqdm

from shazamio import Shazam

shazam = Shazam()

completed_counter = 0
lock = asyncio.Lock()
progress_bar = None

def run_recognize():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(recognize_all())

def get_ts_from_dir(path):
    start_ts = path.split('__')[1].split('_')[0]
    end_ts = path.split('__')[1].split('_')[1].split('.')[0]
    return start_ts, end_ts

async def recognize_all():
    global progress_bar
    file_dirs = sorted(list_files_in_directory(cut_dir))
    num_segments = len(file_dirs)
    progress_bar = tqdm(total=num_segments, desc="Completed recognizing segments")
    results_all = await asyncio.gather(*[tracked_recognize_segment(os.path.join(cut_dir, file_dir), num_segments) for file_dir in file_dirs])
    num_errors = sum('-' not in r for r in results_all)
    progress_bar.close()
    print(f'Recognized {num_segments - num_errors} out of {len(file_dirs)} segments')

    with open(os.path.join(output_dir, 'recognized_tracks.txt'), 'w') as f:
        for line, path in zip(results_all, file_dirs):
            start_ts, end_ts = get_ts_from_dir(path)
            f.write(f"{start_ts} - {line}\n")

async def tracked_recognize_segment(path, num_segments):
    """Wrapper for keeping track of progress"""
    global completed_counter
    global progress_bar
    try:
        return await recognize_segment(path)
    except Exception as e:
        return f'___{e.__class__.__name__}___'
    finally:
        async with lock:
            completed_counter += 1
            if progress_bar:
                progress_bar.update(1)


async def recognize_segment(path: str, save_json: bool=False) -> str:
    
    if use_deprecated_recognize:
        out = await asyncio.wait_for(shazam.recognize_song.__wrapper__(shazam, path), timeout=shazam_timeout_seconds)
        # wrapped for ignoring deprecation decorator
    else:
        out = await asyncio.wait_for(shazam.recognize(path), timeout=shazam_timeout_seconds)

    if save_json:
        with open(os.path.join(output_dir, f"shazam_output.json"), 'w') as f:
            json.dump(out, f, indent=4)

    if out['matches'] == []:
        return '___No matches___'

    track = out['track']['title']
    artist = out['track']['subtitle']
    return f'{artist} - {track}'