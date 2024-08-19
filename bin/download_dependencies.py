import os
import urllib.request
import zipfile
import shutil

if __name__ == '__main__':

    if os.path.exists('ffmpeg'):
        shutil.rmtree("ffmpeg")
    if os.path.exists('yt-dlp.exe'):
        os.remove('yt-dlp.exe')
    if os.path.exists('upx'):
        shutil.rmtree('upx')

    print("Downloading ffmpeg...")
    urllib.request.urlretrieve('https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove('ffmpeg.zip')
    os.rename('ffmpeg-master-latest-win64-gpl', 'ffmpeg')
    shutil.rmtree(os.path.join("ffmpeg", "doc"))

    print("Downloading yt-dlp...")
    urllib.request.urlretrieve('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', 'yt-dlp.exe')
    
    print("Downloading UPX (for compressed builds)")
    urllib.request.urlretrieve('https://github.com/upx/upx/releases/download/v4.2.4/upx-4.2.4-win64.zip', 'upx.zip')
    with zipfile.ZipFile('upx.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove('upx.zip')
    os.rename('upx-4.2.4-win64', 'upx')
