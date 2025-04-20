import os

import ffmpeg

from src.tools import delete_folder_contents, list_files_in_directory
from src.settings import cut_dir, raw_dir


def get_audio_duration(filename: str) -> float:
    """Get duration of audio file in seconds."""
    try:
        probe = ffmpeg.probe(filename, v='error', select_streams='a:0', show_entries='format=duration')
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Error occurred while fetching audio duration: {e}")
        return 0.0

def format_seconds(seconds: float) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def cut_audio(input_filename: str=None, segment_length_seconds: int=10, gap_length_seconds: int=60) -> None:
    if input_filename is None:
        files = list_files_in_directory(raw_dir)
        if len(files) != 1:
            raise Exception("Invalid contents of raw audio folder; must be just one file")
        input_filename = files[0]
    
    print(f"Starting to cut file {input_filename} into segments of {segment_length_seconds}s with gaps of {gap_length_seconds}s")

    delete_folder_contents(cut_dir)

    input_path = os.path.join(raw_dir, input_filename)

    total_duration_sec = int(get_audio_duration(input_path))

    suffix = input_path.split('.')[-1]

    counter = 0
    for start_sec in range(0, total_duration_sec, segment_length_seconds + gap_length_seconds):
        counter += 1
        end_sec = start_sec + segment_length_seconds
        if end_sec > total_duration_sec:
            break

        start_ts = format_seconds(start_sec)
        end_ts = format_seconds(end_sec)

        output_path = os.path.join(cut_dir, f"{input_filename}_segment_{counter:05}__{start_ts}_{end_ts}.{suffix}")

        ffmpeg.input(input_path, ss=start_sec, t=segment_length_seconds).output(output_path, acodec='copy').run(quiet=True)

    print(f"Audio successfully split into {counter} segments")