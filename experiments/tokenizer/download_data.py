
import os
import urllib.request

def download_file_if_absent(url, filename, search_dirs):
    for directory in search_dirs:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            print(f"{filename} already exists in {file_path}")
            return file_path

    target_path = os.path.join(search_dirs[0], filename)
    try:
        with urllib.request.urlopen(url) as response, open(target_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"Downloaded {filename} to {target_path}")
    except Exception as e:
        print(f"Failed to download {filename}. Error: {e}")
    return target_path

verdict_path = download_file_if_absent(
    url=(
         "https://raw.githubusercontent.com/rasbt/"
         "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
         "the-verdict.txt"
    ),
    filename="the-verdict.txt",
    search_dirs="."
)

with open(verdict_path, "r", encoding="utf-8") as f: # added ../01_main-chapter-code/
    text = f.read()