import sys
import os
import ffmpeg
from os.path import expanduser
import multiprocessing as mp
from pytube import YouTube


def path_reformat(path):
    path = path.replace("\\", "/")
    return path

def search_title(title):
    illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for i in range(len(title)):
        if title[i] in illegal_chars:
            title = title[:i] + "-" + title[i+1:]
    return title

def combine(title, path):
    VideoSync, AudioSync = ffmpeg.input('merge\\VideoSync.webm'), ffmpeg.input('merge\\AudioSync.webm')
    ffmpeg.concat(VideoSync, AudioSync, v=1, a=1).output(f"""{path}\\{title}.mp4""").run()

home = path_reformat(expanduser("~"))

def dl(url, path=f"{home}/Desktop"):
    yt = YouTube(url)
    title = yt.title
    print(title, "\nDownloading...")
    title = search_title(title)
    path = path_reformat(path)
    Vitag = yt.streams.order_by('resolution').desc()[0].itag
    Aitag = yt.streams.filter(progressive=False, file_extension='webm')[-1].itag
    yt.streams.get_by_itag(Vitag).download(output_path="""merge\\""", filename="VideoSync.webm")
    yt.streams.get_by_itag(Aitag).download(output_path="""merge\\""", filename="AudioSync.webm")
    print("Downloaded\n")
    combine(title, path)
    os.remove("merge\\VideoSync.webm")
    os.remove("merge\\AudioSync.webm")

def dl_execute(url, path):
    new_process = mp.Process(target=dl, args=(url, path))
    new_process.start()
    new_process.join()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dl(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        dl(sys.argv[1])
    else:
        print("Invalid argument")
