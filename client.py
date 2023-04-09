import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
import os
import time
import ntpath
from ftplib import FTP
from tkinter import filedialog
from pathlib import Path
from playsound import playsound
import pygame
from pygame import mixer



SERVER = None
PORT = 8050
IP_ADDRESS = '127.0.0.1'
BUFFER_SIZE = 4096

global song_counter
song_counter = 0

name = None
listbox = None
filePathLabel = None


def play():
    global song_selected
    
    song_selected = listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/' + song_selected)
    mixer.music.play()

    if(song_selected != ""):
        infoLabel.configure(text = "Now Playing: " + song_selected)
    else:
        infoLabel.configure(text="")

def stop():
    global song_selected

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text = "")

def pause():
    global song_selected

    pygame
    mixer.init()
    mixer.music.load('shared_files/' + song_selected)
    mixer.music.pause()

def resume():
    global song_selected

    pygame
    mixer.init()
    mixer.music.load('shared_files/' + song_selected)
    mixer.music.play()

def browseFiles():
    global listbox
    global song_counter
    global infoLabel

    try:
        filename = filedialog.askopenfilename()

        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)

        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()

        infoLabel.configure(text = filename)
        listbox.insert(song_counter, fname)
        song_counter = song_counter + 1

    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    global listbox
    global infoLabel
    global song_selected
    
    song_to_download = listbox.get(ANCHOR)
    infoLabel.configure(text = "Downloading " + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads" 
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path,song_to_download)
    file = open(local_filename, "wb")
    ftp_server.retrbinary("RETR " + song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text = "Download Complete")

    if(song_selected != ""):
        infoLabel.configure(text = "Now playing " + song_selected)
    else:
        infoLabel.configure(text = "")

def musicWindow(): 

    global listbox
    global infoLabel
    global song_counter
    global filePathLabel
   
    window = Tk()
    window.title('MUSIC WINDOW')
    window.geometry("300x300")
    window.configure(bg="black")

    selectSongLabel = Label(window, text = "Select Song", bg = 'white', font = ('Calibri', 8))
    selectSongLabel.place(x=120,y=1)

    listbox = Listbox(window, height = 10, width = 39, activestyle="dotbox",bg = "LightSkyBlue", borderwidth=2, font = ("Calibri", 10))
    listbox.place(x=10,y=18)

    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter, filename)
        song_counter = song_counter + 1

    scrollBar1 = Scrollbar(listbox)
    scrollBar1.place(relheight = 1,relx=1)
    scrollBar1.config(command = listbox.yview)

    playButton = Button(window, text = "Play", width = 10, bd = 1, bg = "purple", font = ("Calibri", 10),command = play)
    playButton.place(x=30,y=200)

    stopButton = Button(window, text = "Stop", bd = 1, width = 10, bg = "red", font = ("Calibri",10), command = stop)
    stopButton.place(x=200,y=200)

    resumeButton = Button(window, text = "Resume", bd = 1, width = 10, bg = "orange", font = ("Calibri",10), command=resume)
    resumeButton.place(x=30, y=225)

    pauseButton = Button(window, text = "Pause", bd = 1, width = 10, bg = "white", font = ("Calibri",10), command=pause)
    pauseButton.place(x=200, y=225)

    uploadButton = Button(window, text = "Upload", width = 10, bd = 1, bg = "yellow", font = ("Calibri", 10),command=browseFiles)
    uploadButton.place(x=30,y=250)

    downloadButton = Button(window, text = "Download", bd = 1, width = 10,bg = "green", font = ("Calibri",10), command = download)
    downloadButton.place(x=200,y=250)

    infoLabel = Label(window, text = "", fg = "blue", font = ("Calibri",8))
    infoLabel.place(x=4,y=280)

    window.mainloop()

def setup():

    global SERVER
    global PORT
    global IP_ADDRESS
    global song_counter

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    musicWindow()

setup()
