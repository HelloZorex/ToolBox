import os
import ffmpeg
import multiprocessing as mp
from pytube import YouTube

def search_title(title):
    illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for i in range(len(title)):
        if title[i] in illegal_chars:
            title = title[:i] + "-" + title[i+1:]
    return title

def path_reformat(path):
    path = path.replace("\\", "/")
    return path

def combine(title, path):
    VideoSync, AudioSync = ffmpeg.input('temp\\VideoSync.webm'), ffmpeg.input('temp\\AudioSync.webm')
    ffmpeg.concat(VideoSync, AudioSync, v=1, a=1).output(f"""{path}\\{title}.mp4""").run()

def dl(url, path):
    yt = YouTube(url)
    title = yt.title
    print(title + "\n")
    title = search_title(title)
    print(title)
    path = path_reformat(path)
    # Vitag = yt.streams.filter(progressive=False, file_extension='webm')[0].itag
    Vitag = yt.streams.order_by('resolution').desc()[0].itag
    Aitag = yt.streams.filter(progressive=False, file_extension='webm')[-1].itag
    print(yt.streams.get_by_itag(Vitag))
    print(yt.streams.get_by_itag(Aitag), "\n")
    yt.streams.get_by_itag(Vitag).download(output_path="""temp\\""", filename="VideoSync.webm")
    yt.streams.get_by_itag(Aitag).download(output_path="""temp\\""", filename="AudioSync.webm")
    print("Downloaded\n")
    combine(title, path)
    os.remove("temp\\VideoSync.webm")
    os.remove("temp\\AudioSync.webm")

def dl_execute(url, path):
    new_process = mp.Process(target=dl, args=(url, path))
    new_process.start()