# FoxTube Downloader
This is a simple GUI that uses [YT-DLP](https://github.com/yt-dlp/yt-dlp) for downloading videos and audios from YouTube and optionally cuts them into shorter clips.
Fun fact: I had already built a very similar thing years ago but it was old and broken, so I re-made it; hence the "version 2".
## Installation
The release page provides an executable `.exe` file and a `.zip` archive. These were built using [`pyinstaller`](https://pyinstaller.org/en/stable/) (with and without the `--onefile` option respectively).
If you don't trust me, that's more than fair. You can create your own executables by cloning the repo and doing the following:
1) Downloading external dependencies (ffmpeg binaries, yt-dlp and optionally UPX for compressing binaries in the final build). This can be achieved by entering the `bin` folder and running the `download_dependencies.py` script.
```powershell
cd bin
python download_dependencies.py
```
2) Creating a Python virtual environment with `venv` and installing required libraries.
```powershell
python -m venv .env
.env\Scripts\activate
python -m pip install -r requirements.txt
```
3) Building the application through the provided scripts `build.ps1` and `build_onefile.ps1`.
```powershell
.\build.ps1 # or .\build_onefile.ps1
```
Of course, you can also run the application as a Python script using:
```powershell
python start.py
```
## Usage
Simply paste the URL of a YouTube video into the upper entry field, or use the "Paste" button.
Then, select the desired start and end times for the video. 
- If all fields are left empty, the video (or audio) will be downloaded in its entirety
- Otherwise, empty fields are considered zeros
Finally, choose the folder where the video will be downloaded.
The output file will be assigned the video title, an ID and the time indication in its filename.
## Configurations
You can change some elements of the GUI through the `config.yaml` file, even after the build (it will be into the `_internal` folder).
Particularly, you can change the preferred video and audio formats (this is still WIP), the quality of video and audio, as well as colors, fonts and app language (IT or EN).
## Disclaimer
The project is still a huge WIP and uses external libraries extensively, so I don't take any responsibility in case of weird behaviours on your computer.
