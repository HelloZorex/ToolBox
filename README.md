### Tiny Youtube Downloader
Command-line based youtube video downloader.

## Setup
```
git clone https://github.com/grantcary/TinyYTDL.git
cd TinyYTDL
pip3 install -r requirements.txt
```

## Command-line usage
```
usage: python3 download.py [--url] [--out]

options:
    --url (req)  # any valid youtube url
    --out        # any valid folder path
```
Note: This program merges video and audio streams together using ffmpeg-python concat function. Concat has a very slow execution rates, expect slow merge times.