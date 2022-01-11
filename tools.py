import os
import ffmpeg
from pytube import YouTube

def combine(title):
    VideoSync, AudioSync = ffmpeg.input('temp\\VideoSync.webm'), ffmpeg.input('temp\\AudioSync.webm')
    ffmpeg.concat(VideoSync, AudioSync, v=1, a=1).output(f"""videos\\{title}.mp4""").run()

def dl(url):
    yt = YouTube(url)
    title = yt.title
    Vitag = yt.streams.filter(progressive=False, file_extension='webm')[0].itag
    Aitag = yt.streams.filter(progressive=False, file_extension='webm')[-1].itag
    print(yt.streams.get_by_itag(Vitag))
    print(yt.streams.get_by_itag(Aitag))
    yt.streams.get_by_itag(Vitag).download(output_path="""temp\\""", filename="VideoSync.webm")
    yt.streams.get_by_itag(Aitag).download(output_path="""temp\\""", filename="AudioSync.webm")
    combine(title)
    os.remove("temp\\VideoSync.webm")
    os.remove("temp\\AudioSync.webm")

newurl = """https://youtu.be/NxNi0vDs5tc"""
dl(newurl)
