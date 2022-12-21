from tempfile import TemporaryDirectory
from os.path import expanduser
from pytube import YouTube
import argparse
import ffmpeg


def path_reformat(path: str) -> str:
  return path.replace('\\', '/')

def illegal_chars(title: str) -> str:
  for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
    title = title.replace(c, '-')
  return title

def download(url: str, path: str, tmp_file: str) -> str:
  yt = YouTube(url)
  print(f'downloading {yt.title}')
  
  # reformat for illegal characters
  title, path = illegal_chars(yt.title), path_reformat(path)
  
  # get highest possible resolution video and audio file tags
  video_tag = yt.streams.order_by('resolution').desc()[0].itag
  audio_tag = yt.streams.filter(progressive=False, file_extension='webm')[-1].itag
  
  # download seperate video and audio files
  yt.streams.get_by_itag(video_tag).download(output_path=tmp_file, filename='videosync.webm')
  yt.streams.get_by_itag(audio_tag).download(output_path=tmp_file, filename='audiosync.webm')

  # setup file paths
  tmp_video, tmp_audio, out_path = f'{tmp_file}/videosync.webm', f'{tmp_file}/audiosync.webm', f'{path}/{title}.mp4'
  
  # concatenate video and audio files and save to output path
  print('merging video and audio...')
  ffmpeg.concat(ffmpeg.input(tmp_video), ffmpeg.input(tmp_audio), v=1, a=1).output(out_path, preset='veryfast', loglevel='fatal').run()
  
  return out_path

if __name__ == "__main__":
  home = f'{path_reformat(expanduser("~"))}/Desktop'
  
  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--url', required=True, type=str, help="YouTube URL")
  parser.add_argument('--out', type=str, default=home, help="Output destination")
  args = parser.parse_args()

  # create temporary directory
  tmp_dir = TemporaryDirectory()
  tmp = tmp_dir.name

  out = download(args.url, args.out, tmp)

  # close temporary directory
  tmp_dir.cleanup()

  print(f"saved to absolute path: {out}")