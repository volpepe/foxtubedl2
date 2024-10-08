import datetime
import os
import subprocess
import threading
import time
from tkinter import DISABLED, NORMAL

import yaml

from .paths import resource_path
from .strings import STRINGS


class OutShowThread(threading.Thread):
    def __init__(self, text, out, config): 
        threading.Thread.__init__(self) 
        self.config = config
        self.running = False
        self.text_label = text
        self.out_label = out
    
    def run(self):
        self.running = True
        count=0
        while(self.running):
            self.text_label.config(state=NORMAL)
            self.out_label.set(
                STRINGS['OUT_DOWNLOAD_STR'][self.config['app']['lang']] + "."*count)
            count = count+1 if count < 5 else 0
            self.text_label.config(state=DISABLED)
            time.sleep(0.8)
    
    def stop(self):
        self.running = False


class DownloadThread(threading.Thread):
    def __init__(self, dl_type, entry_url, text_label, 
                 folder_text_label,
                 st_min, st_sec, en_min, en_sec, 
                 out_label, dl_button_audio, dl_button_video): 
        threading.Thread.__init__(self)
        with open(resource_path('config.yaml'),'r') as f:
            self.config = yaml.safe_load(f)
        self.dl_type = dl_type
        self.entry_url_label = entry_url
        self.text_label = text_label
        self.folder_text_label = folder_text_label
        self.st_min = st_min
        self.st_sec = st_sec
        self.en_min = en_min
        self.en_sec = en_sec
        self.out_label = out_label
        self.running = False
        self.out_show_thread = OutShowThread(
            self.text_label, self.out_label, self.config)
        self.type = dl_type
        self.dl_button_audio = dl_button_audio
        self.dl_button_video = dl_button_video
        self.out_show_thread.start()

    def run(self):
        self.running = True

        self.dl_button_audio['state'] = 'disabled'
        self.dl_button_video['state'] = 'disabled'

        start, end = self.check_timings()
        start_string = str(start).replace(':', '_')
        end_string = str(end).replace(':','_')

        try:
            title = self.get_title()
        except subprocess.CalledProcessError:
            self.stop_execution(STRINGS['ERR_TITLE_STR'][self.config['app']['lang']])
            return
        
        # add time strings to title
        if start > datetime.timedelta(seconds=0) or end > datetime.timedelta(seconds=0):
            title = '_'.join([title, start_string, end_string])
        print("Title: {}".format(title))

        command = self.build_download_command(start, end, title)
        print(command)

        # Run download
        status_string = ''
        try:
            subprocess.call(command, shell=True)
            status_string = STRINGS['DONE_STR'][self.config['app']['lang']]
        except subprocess.CalledProcessError:
            status_string = STRINGS['ERR_DOWNLOAD_STR'][self.config['app']['lang']]

        self.stop_execution(status_string)

    def get_title(self):
        # get title of the final video/audio file
        command_title = '{} --get-filename {}'.format(resource_path(os.path.join('bin', 'yt-dlp.exe')), 
                                                      self.entry_url_label.get())
        # will ignore any non-utf-8 chars in title
        title = subprocess.check_output(command_title, shell=True).decode("utf-8", 'ignore').rstrip()[:-4]
        return title

    def build_download_command(self, start, end, title):
        if self.type == 'audio':
            command = '{} -x {} --audio-format {} --audio-quality {} -o "{}%(ext)s" {}'.format(
                resource_path(os.path.join('bin','yt-dlp.exe')),
                self.add_time_commands(start, end, 'ffmpeg_pre'), 
                self.config['formats']['audio'], 
                self.config['quality']['audio'],
                os.path.join(self.folder_text_label.get(), title), 
                self.entry_url_label.get())
        elif self.type == 'video':
            command = '{} {} -f {} --merge-output-format {} --remux-video {} -o "{}%(ext)s" {}'.format(
                resource_path(os.path.join('bin','yt-dlp.exe')),
                self.add_time_commands(start, end, 'ffmpeg_pre'), 
                self.config['quality']['video'],
                self.config['formats']['video'],
                self.config['formats']['video'],  
                os.path.join(self.folder_text_label.get(), title), 
                self.entry_url_label.get()
            )
        return command

    def check_timings(self):
        start = end = datetime.timedelta(seconds=0)
        #starting minute, starting second, ending minute, ending second
        timings =  list(map(lambda x: int(0 if x == '' else x), [self.st_min.get(), 
            self.st_sec.get(), self.en_min.get(), self.en_sec.get()]))
        s_start = 60*timings[0] + timings[1]
        s_end = 60*timings[2] + timings[3]
        if s_start > 0:
            start += datetime.timedelta(seconds=s_start)
        if s_end > 0:
            end += datetime.timedelta(seconds=s_end)
        print("Starting time: " + str(start))
        print("Ending time: " + str(end))
        return start, end

    def add_time_commands(self, start, end, style):
        com = ''
        if style == 'ffmpeg_pre' and (start.seconds > 0 or end.seconds > 0):
            com += '--postprocessor-args "'
        if start.seconds > 0:
            com += " {} {} ".format("-ss", str(start))
        if end.seconds > 0:
            com += " {} {} ".format("-to", str(end))
        if style == 'ffmpeg_pre' and (start.seconds > 0 or end.seconds > 0):
            com += '"'
        return com

    def stop_execution(self, status_string):
        self.out_show_thread.stop()
        self.out_show_thread.join()
        self.running = False

        self.dl_button_audio['state'] = NORMAL
        self.dl_button_video['state'] = NORMAL

        # clean slate
        self.text_label.config(state=NORMAL)
        self.out_label.set(status_string)
        self.text_label.config(state=DISABLED)