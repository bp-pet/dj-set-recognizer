import os
import shutil

def delete_folder_contents(folder_path: str) -> None:
    for filename in os.listdir(folder_path):
        if filename[0] == '.':
            continue
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

def list_files_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f[0] != '.']
    return files