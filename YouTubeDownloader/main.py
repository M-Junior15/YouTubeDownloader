import os

from time import sleep
from pytube import YouTube, Playlist
from http_exceptions import HTTPException
from flask import Flask, abort, redirect, render_template, request


app = Flask(__name__)

# Function to get the download path
def get_download_path(word):
    """Returns the default downloads path for linux or windows"""
    # Download path for windows
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    # Download path for linux
    else:
        download_path = os.path.join(os.path.expanduser('~'))
        # Try to download the file in the given path
        try:
            folder_path = download_path + '/' + word + '/' + folder_name
            os.mkdir(folder_path)
        except FileExistsError:
            sleep(1)
    return folder_path

# Function to download video
def download_vid(url, answ_PS):
    install_here = get_download_path("Videos")
    # Download a single video
    if answ_PS == 'S':
        YouTube(url).streams.get_by_itag(137).download(install_here)
    # Download a playlist of videos
    elif answ_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: arq.streams.get_by_itag(137).first().download(install_here)

# Function to download audio
def download_aud(url, answ_PS):
    install_here = get_download_path("Music")
    # Download a single audio
    if answ_PS == 'S':
        YouTube(url).streams.get_by_itag(251).download(install_here)
    # Download a playlist of audios
    elif answ_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: 
            arq.streams.get_by_itag(251).download(install_here)

# Function to choose some options
def choose(url, answ_PS, answ_VA):
    # If the option is video
    if answ_VA == 'V':
        download_vid(url, answ_PS)
    # If the option is audio
    elif answ_VA == 'A':
        download_aud(url, answ_PS)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        url = request.form.get('url')

        global folder_name
        folder_name = request.form.get('foldername')

        answ_PS = request.form['choosePS']
        answ_VA = request.form['chooseVA']

        if not url:
            raise HTTPException.from_status_code(status_code=406)(message="ERROR")
        elif not folder_name:
            raise HTTPException.from_status_code(status_code=406)(message="ERROR")
        elif not answ_PS:
            raise HTTPException.from_status_code(status_code=406)(message="ERROR")
        elif not answ_VA:
            raise HTTPException.from_status_code(status_code=406)(message="ERROR")

        if 'submit_button' in request.form:
            choose(url, answ_PS, answ_VA)
        return redirect("/")
    else:
        return render_template('index.html')   

# The main program
if __name__ == "__main__":
    app.run()
