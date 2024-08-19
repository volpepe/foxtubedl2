import subprocess
import os
import sys

from src import gui_setup


if __name__ == '__main__':

    sys.path.append(os.path.abspath('bin/ffmpeg/bin'))

    print("VIDEO-MUSIC-DOWNLOAD")
    print("-----------------------------------\n\nControllo aggiornamenti...\n\n")
    subprocess.call([os.path.join('.', 'bin', 'yt-dlp'), "-U"])
    print("-----------------------------------\n\nOK.\n\n")

    root_app = gui_setup()
    root_app.mainloop()