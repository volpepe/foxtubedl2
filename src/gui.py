import os
from tkinter import (DISABLED, Button, Entry, Label, StringVar, Tk, W,
                     filedialog)

import pyperclip
import yaml

from .paths import resource_path
from .logic import DownloadThread


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

    #creating the instruction label
    label = Label(root, text='Incolla qui il link:', font=(12), pady=15)
    label.grid(row=0, column=0, padx=5)

    #creating the input space (entry)
    entry_url = Entry(root, textvariable=link_text, width=70)
    entry_url.grid(row=0, column=1, columnspan=4, sticky=W, padx=20)

    #creating the time selectors
    label = Label(root, text='Minuto di inizio:', font=(12), pady=15)
    label.grid(row=1, column=0, padx=5)
    entry = Entry(root, textvariable=st_min, width=4)
    entry.grid(row=1, column=1, sticky=W, padx=10)
    label = Label(root, text='Secondo di inizio:', font=(12), pady=15)
    label.grid(row=1, column=2, padx=5)
    entry = Entry(root, textvariable=st_sec, width=4)
    entry.grid(row=1, column=3, sticky=W, padx=10)
    label = Label(root, text='Minuto di fine:', font=(12), pady=15)
    label.grid(row=1, column=4, padx=5)
    entry = Entry(root, textvariable=en_min, width=4)
    entry.grid(row=1, column=5, sticky=W, padx=10)
    label = Label(root, text='Secondo di fine:', font=(12), pady=15)
    label.grid(row=1, column=6, padx=5)
    entry = Entry(root, textvariable=en_sec, width=4)
    entry.grid(row=1, column=7, sticky=W, padx=10)

    #creating the output folder label and entry
    label = Label(root, text="Destinazione:", font=(12), pady=15)
    label.grid(row=2, column=0, padx=5)
    entry_folder = Entry(root, textvariable=folder_text, width=70)
    entry_folder.grid(row=2, column=1, columnspan=4, sticky=W, padx=20)

    #initialize folder text
    folder_text.set(os.getcwd())

    #creating the text label
    text = Label(root, textvariable=out, width=80, font=(18))
    text.grid(row=3, column=0, columnspan=8, pady=15, padx=20)
    text.config(state=DISABLED)

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
            title="Seleziona Cartella di Destinazione").replace('/', os.sep))

    dl_button_audio = Button(root, text='Download Audio', command=start_download_audio, bg='brown', fg='white')
    dl_button_audio.grid(row=0, column=5)  

    dl_button_video = Button(root, text='Download Video', command=start_download_video, bg='brown', fg='white')
    dl_button_video.grid(row=0, column=6, padx=20)

    #create the paste button
    pt_button = Button(root, text='Incolla', command=paste, bg='brown', fg='white')
    pt_button.grid(row=0, column=7, padx=10)

    #create the choose folder button
    choose_fold_button = Button(root, text="Seleziona...", command=select_folder, bg="brown", fg="white")
    choose_fold_button.grid(row=2, column=5, pady=15, padx=2, sticky=W)

    return root