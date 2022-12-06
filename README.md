This Python code uses the yt_dlp library to download videos from 
YouTube. The user is prompted to enter a YouTube URL, which is then 
validated to ensure that it starts with https:// and is a 
valid link. If the URL is part of a playlist, the user is asked whether 
they want to download the whole playlist or just the individual video. 
The user is then prompted to select the desired video resolution, and 
the appropriate options are set in the ydl_opts dictionary. Finally, the video is downloaded using these options.
