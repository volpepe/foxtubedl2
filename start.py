import subprocess
import os
import sys

import yaml

from src import gui_setup, resource_path


if __name__ == '__main__':

    sys.path.append(os.path.abspath(resource_path(os.path.join('bin', 'ffmpeg', 'bin'))))

    with open(resource_path('config.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    print("\n\n" + config['app']['title'] + " - by " + config['app']['by'])
    print("-----------------------------------\n\nControllo aggiornamenti...\n\n")
    subprocess.call([resource_path(os.path.join('bin', 'yt-dlp.exe')), "-U"])
    print("-----------------------------------\n\nOK.\n\n")

    root_app = gui_setup()
    root_app.mainloop()