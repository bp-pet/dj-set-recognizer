import os

import librosa
import soundfile as sf

from src.tools import delete_folder_contents, list_files_in_directory
from src.settings import cut_dir, raw_dir

def format_seconds(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def cut_audio(filename: str=None, segment_length_seconds: int=10, gap_length_seconds: int=60) -> None:
    if filename is None:
        files = list_files_in_directory(raw_dir)
        if len(files) != 1:
            raise Exception("Invalid contents of raw audio folder; must be just one file")
        filename = files[0]
    
    print(f"Starting to cut file {filename} into segments of {segment_length_seconds}s with gaps of {gap_length_seconds}s")

    delete_folder_contents(cut_dir)

    waveform, sample_rate = librosa.load(os.path.join(raw_dir, filename), sr=None)
    samples_per_segment = segment_length_seconds * sample_rate
    samples_per_gap = gap_length_seconds * sample_rate


    counter = 0
    for i in range(0, len(waveform), samples_per_segment + samples_per_gap):
        segment = waveform[i:i + samples_per_segment]
        segment_index = i // (samples_per_segment + samples_per_gap) + 1

        start_ts = format_seconds(i // sample_rate)
        end_ts = format_seconds((i + samples_per_segment) // sample_rate)
        
        sf.write(os.path.join(cut_dir, f"{filename}_segment_{segment_index:05}__{start_ts}_{end_ts}.flac"), segment, sample_rate)
        counter += 1

    print(f"Audio successfully split into {counter} segments")