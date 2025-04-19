import os

import librosa
import soundfile as sf

from src.tools import delete_folder_contents, list_files_in_directory
from src.settings import cut_dir, raw_dir


def cut_audio(filename: str=None, segment_length_seconds: int=10, gap_length_seconds: int=60) -> None:
    if filename is None:
        files = list_files_in_directory(raw_dir)
        if len(files) != 1:
            raise Exception("Invalid contents of raw audio folder; must be just one file")
        filename = files[0]
    
    print(f"Starting to cut file {filename} into segments of {segment_length_seconds}s with gaps of {gap_length_seconds}s")

    delete_folder_contents(cut_dir)

    waveform, sample_rate = librosa.load(f"{raw_dir}\\{filename}", sr=None)
    samples_per_segment = segment_length_seconds * sample_rate
    samples_per_gap = gap_length_seconds * sample_rate


    counter = 0
    for i in range(0, len(waveform), samples_per_segment + samples_per_gap):
        segment = waveform[i:i + samples_per_segment]
        sf.write(f"{cut_dir}\\{filename}_segment_{i // (samples_per_segment + samples_per_gap) + 1}.flac", segment, sample_rate)
        counter += 1

    print(f"Audio successfully split into {counter} segments")