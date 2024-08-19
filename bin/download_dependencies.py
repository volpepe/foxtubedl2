import os
import urllib.request
import zipfile
import shutil

if __name__ == '__main__':

    print("Downloading ffmpeg...")
    urllib.request.urlretrieve('https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove('ffmpeg.zip')
    os.rename('ffmpeg-master-latest-win64-gpl', 'ffmpeg')
    shutil.rmtree(os.path.join("ffmpeg", "doc"))
    
    print("Downloading yt-dlp...")
    urllib.request.urlretrieve('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp', 'yt-dlp')
