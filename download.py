from os.path import expanduser
from pytube import YouTube
import ffmpeg
import sys
import os

def path_reformat(path): return path.replace('\\', '/')
home = f'{path_reformat(expanduser("~"))}/Desktop'

def illegal_chars(title):
  for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
    title = title.replace(c, '-')
  return title

def download(url, path):
  yt = YouTube(url)
  print(yt.title, "\n\nDownloading...")
  title, path = illegal_chars(yt.title), path_reformat(path)
  vidtag = yt.streams.order_by('resolution').desc()[0].itag
  audtag = yt.streams.filter(progressive=False, file_extension='webm')[-1].itag
  yt.streams.get_by_itag(vidtag).download(output_path='merge/', filename='vidsync.webm')
  yt.streams.get_by_itag(audtag).download(output_path='merge/', filename='audsync.webm')
  print('Downloaded\n')
  vidpath, audpath = 'merge/vidsync.webm', 'merge/audsync.webm'
  ffmpeg.concat(ffmpeg.input(vidpath), ffmpeg.input(audpath), v=1, a=1).output(f'{path}/{title}.mp4').run()
  for p in [vidpath, audpath]: os.remove(p)


if __name__ == "__main__":
  download(sys.argv[1], home) if sys.argv[1] else print("Invalid argument")