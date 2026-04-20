#!/usr/bin/env python3

import yt_dlp
from yt_dlp.utils import DownloadError
import signal
import sys


# when ^C is pressed exit program nicely
def handler(signum, frame):
    print("\n^C was pressed. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


def get_int_input(prompt, valid_range):
    """Safely read an integer from stdin, re-prompting on invalid input."""
    while True:
        try:
            n = int(input(prompt))
            if n in valid_range:
                return n
        except ValueError:
            pass
        print(f"Invalid input. Please enter a number between {min(valid_range)} and {max(valid_range)}.")


# asks for URL of video to download
url = input("URL: ")
while not url.startswith('https://'):
    print("Not HTTPS or bad link.")
    url = input("URL: ")

# checks if video is from playlist
playlist = False
if '&list' in url:
    print("This video is from a playlist.")
    vip = input("[v]ideo or [p]laylist?: ")
    while vip not in ('v', 'p'):
        vip = input("[v]ideo or [p]laylist?: ")
    if vip == 'v':
        url = url.split("&list", 1)[0]
    else:
        playlist = True

# prints title / playlist name
quiet_opts = {'quiet': True, 'no_warnings': True}
with yt_dlp.YoutubeDL(quiet_opts) as ydl_info:
    info = ydl_info.extract_info(url, download=False)
    if info:
        if playlist:
            print("\nPlaylist:", info.get('title', 'Unknown playlist'))
        else:
            print("\nTitle:", info.get('title', 'Unknown title'))

if "soundcloud.com" in url:
    audio_format = 'http_mp3_128'
else:
    audio_format = '140'

# skip quality menu for YouTube Music
if "music.youtube.com" in url:
    n = 7
else:
    print("\n[1] 144\n[2] 240\n[3] 360\n[4] 480\n[5] 720\n[6] 1080\n[7] Audio\n")
    n = get_int_input("Number: ", range(1, 8))

res_map = {1: "144", 2: "240", 3: "360", 4: "480", 5: "720", 6: "1080"}

common_opts = {
    'ignoreerrors': True,
    'compat_opts': {'no-youtube-unavailable-videos'},
    'extract_flat': 'discard_in_playlist',
    'abort_on_unavailable_fragments': True,
    'outtmpl': '%(title)s.%(ext)s',
}

audio_opts = {
    'format': audio_format,
    'format_sort': ['ext'],
    'merge_output_format': ['mp3'],
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        },
        {
            'key': 'FFmpegMetadata',
            'add_chapters': False,
            'add_metadata': True
        },
        {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False
        }
    ]
}

if n == 7:  # audio
    ydl_opts = {**common_opts, **audio_opts}
else:
    format_sort = 'res:' + res_map[n]
    video_opts = {
        'format_sort': [format_sort, 'vext:mp4', 'aext:m4a', '+size'],
    }
    ydl_opts = {**common_opts, **video_opts}

# download file using settings with error exception
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([url])
    except DownloadError as e:
        print(f"Download error: {e}")
