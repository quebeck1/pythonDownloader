#!/usr/bin/env python3

import yt_dlp
import signal
import sys

def handler(signum, frame):
    print(" was pressed. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

url = input("Link: ")

while not url.startswith('https://'):
    print("Not HTTPS or bad link.")
    url = input("Link: ")

if '&list' in url:
    print("This video is from playlist.")
    vip = input("[v]ideo or [p]laylist?: ")
    while vip != 'v' and vip != 'p':
        vip = input("[v]ideo or [p]laylist?: ")
    if vip == 'v':
        url = url.split("&list", 1)[0]

print("""
[1] 144
[2] 240
[3] 360
[4] 480
[5] 720
[6] 1080
[7] Audio
""")
n = int(input("Number: "))

res = [144, 240, 360, 480, 720, 1080, "Audio"]
format_sort = 'res:' + str(res[n - 1])

while n not in range(1, 8):
    n = int(input("Number: "))

if n == 7:
    ydl_opts = {
        'format': '139',
        'format_sort': ['ext'],
        'ignoreerrors': True,
        'writethumbnail': True,
        'abort_on_unavailable_fragments': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a'
            },
            {
                'key': 'SponsorBlock',
                'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'interaction', 'music_offtopic']
            },
            {
                'key': 'ModifyChapters',
                'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'interaction', 'music_offtopic']
            }
            # {
                # 'key': 'MetadataParser',
                # 'when': 'pre_process',
                # 'actions': [{MetadataParserPP.Actions.INTERPRET, 'descriptionk'}]
            # }
        ]
    }
else:
    ydl_opts = {
        'format_sort': [format_sort, 'vext:mp4', 'aext:m4a', '+size'],
        'ignoreerrors': True,
        'abort_on_unavailable_fragments': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'SponsorBlock',
                'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'interaction']
            },
            {
                'key': 'ModifyChapters',
                'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'interaction']
            }
        ]
    }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
