import os
import subprocess
from tkinter import (DISABLED, Button, Entry, Frame, Label, StringVar, Tk,
                     filedialog, font)

import pyperclip
import yaml

from .paths import resource_path
from .logic import DownloadThread
from .strings import STRINGS


def gui_setup():

    with open(resource_path('config.yaml'), 'r') as f:
        config = yaml.safe_load(f)

    root = Tk()
    root.title('{} - by {}'.format(config['app']['title'], config['app']['by']))
    root.geometry('{}x{}'.format(config['app']['start_geometry']['width'],
                                 config['app']['start_geometry']['height']))

    #this variable will contain the link inserted by the user
    link_text = StringVar()
    folder_text = StringVar()
    st_min = StringVar()
    st_sec = StringVar()
    en_min = StringVar()
    en_sec = StringVar()
    out = StringVar()

    # Define functions
    def start_download_audio():
        y = DownloadThread('audio', entry_url, text, folder_text, 
                           st_min, st_sec, en_min, en_sec, 
                           out, dl_button_audio, dl_button_video)
        y.start()

    def start_download_video():
        y = DownloadThread('video', entry_url, text, folder_text, 
                            st_min, st_sec, en_min, en_sec, 
                            out, dl_button_audio, dl_button_video)
        y.start()

    def paste():
        entry_url.delete(0, 'end')
        entry_url.insert(0, pyperclip.paste())

    def select_folder():
        folder_text.set(filedialog.askdirectory(initialdir=folder_text.get(), 
            title=STRINGS['ASK_DIR_STR'][config['app']['lang']]).replace('/', os.sep))
        
    def open_folder():
        subprocess.call('explorer "{}"'.format(folder_text.get()))

    # Define fonts
    default_font = font.Font(
        family=config['app']['fonts']['family'], 
        size=int(config['app']['fonts']['size']), 
        weight=config['app']['fonts']['weight'])
    stronger_font = font.Font(
        family=config['app']['fonts']['family'],
        size=int(config['app']['fonts']['size'])+2,
        weight='bold'
    )
    large_font = font.Font(
        family=config['app']['fonts']['family'], 
        size=int(config['app']['fonts']['size'])+4, 
        weight=config['app']['fonts']['weight'])

    # Start defining the GUI
    #creating the instruction label
    link_frame = Frame(root)
    link_frame.pack(pady=10, padx=5, expand=True, fill='x')

    label = Label(link_frame, 
                  text=STRINGS['PASTE_LABEL_STR'][config['app']['lang']], 
                  font=default_font)
    label.pack(side='left', ipadx=5, ipady=5)

    #create the paste button
    pt_button = Button(link_frame, 
                       text=STRINGS['PASTE_BUTTON_STR'][config['app']['lang']], 
                       command=paste, 
                       bg=config['app']['colors']['bg'], 
                       fg=config['app']['colors']['fg'],
                       font=default_font)
    pt_button.pack(side='right', padx=15, ipadx=5, ipady=5)

    #creating the input space (entry)
    entry_url = Entry(link_frame, textvariable=link_text, width=70, font=default_font,
                      relief='sunken')
    entry_url.pack(side='right', padx=20, ipadx=5, ipady=5, expand=True, fill='x')

    #creating the time selectors
    time_select_frame = Frame(root)
    time_select_frame.pack(padx=50, pady=1, expand=True, fill='x')
    label = Label(time_select_frame, text=STRINGS['FROM_LABEL_STR'][config['app']['lang']], font=default_font)
    label.pack(side='left')
    entry = Entry(time_select_frame, textvariable=st_min, width=5, relief='sunken')
    entry.pack(side='left', padx=10, ipadx=5, ipady=5)
    label = Label(time_select_frame, text='-', font=default_font)
    label.pack(side='left', padx=10, ipadx=5, ipady=5)
    entry = Entry(time_select_frame, textvariable=st_sec, width=5, relief='sunken')
    entry.pack(side='left', padx=10, ipadx=5, ipady=5)
    label = Label(time_select_frame, text='')
    label.pack(side='left', padx=10, expand=True, fill='x')
    label = Label(time_select_frame, text=STRINGS['TO_LABEL_STR'][config['app']['lang']], font=default_font)
    label.pack(side='left')
    entry = Entry(time_select_frame, textvariable=en_min, width=5, relief='sunken')
    entry.pack(side='left', padx=10, ipadx=5, ipady=5)
    label = Label(time_select_frame, text='-', font=default_font)
    label.pack(side='left', padx=10, ipadx=5, ipady=5)
    entry = Entry(time_select_frame, textvariable=en_sec, width=5, relief='sunken')
    entry.pack(side='left', padx=10, ipadx=5, ipady=5)

    #creating the output folder label and entry
    folder_frame = Frame(root)
    folder_frame.pack(pady=5, padx=5, expand=True, fill='x')

    label = Label(folder_frame, 
                  text=STRINGS['DESTINATION_LABEL_STR'][config['app']['lang']], 
                  font=default_font)
    label.pack(side='left', ipadx=5, ipady=5)

    #create the choose folder button
    choose_fold_button = Button(folder_frame, 
                                text=STRINGS['SELECT_LABEL_STR'][config['app']['lang']], 
                                command=select_folder, 
                                bg=config['app']['colors']['bg'], 
                                fg=config['app']['colors']['fg'],
                                font=default_font)
    choose_fold_button.pack(side='right', padx=5, ipadx=5, ipady=5)

    #initialize folder text
    folder_text.set(os.getcwd())
    entry_folder = Entry(folder_frame, textvariable=folder_text, width=70, font=default_font,
                      relief='sunken')
    entry_folder.pack(side='right', padx=20, ipadx=5, ipady=5, expand=True, fill='x')

    # Create the download buttons
    download_frame = Frame(root)
    download_frame.pack(pady=10, padx=5, expand=True, fill='x')

    dl_button_video = Button(   download_frame, 
                                text=STRINGS['DOWNLOAD_VIDEO_STR'][config['app']['lang']], 
                                command=start_download_video, 
                                bg=config['app']['colors']['bg'], 
                                fg=config['app']['colors']['fg'],
                                font=stronger_font)
    dl_button_video.pack(side='right', padx=25, ipadx=8, ipady=8)

    #create the visualize folder button
    open_fold_button = Button(  download_frame, 
                                text=STRINGS['OPEN_LABEL_STR'][config['app']['lang']], 
                                command=open_folder, 
                                bg=config['app']['colors']['bg'], 
                                fg=config['app']['colors']['fg'],
                                font=default_font)
    open_fold_button.pack(side='right', padx=5, ipadx=2, ipady=2, expand=True)

    dl_button_audio = Button(   download_frame, 
                                text=STRINGS['DOWNLOAD_AUDIO_STR'][config['app']['lang']], 
                                command=start_download_audio, 
                                bg=config['app']['colors']['bg'], 
                                fg=config['app']['colors']['fg'],
                                font=stronger_font)
    dl_button_audio.pack(side='right', padx=25, ipadx=8, ipady=8)

    #creating the out text label
    out_frame = Frame(root)
    out_frame.pack(pady=2, padx=5, ipady=10, expand=True, fill='both')
    text = Label(out_frame, textvariable=out, width=80, font=large_font)
    text.pack(expand=True, fill='both')
    text.config(state=DISABLED)

    return root