import os
from pytube import YouTube, Playlist
from time import sleep
from flask import Flask, render_template, request, Response


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
        # Ask for a folder to download the file
        folder_name = input("Enter your folder name: ")
        download_path = os.path.join(os.path.expanduser('~'))
        # Try to download the file in the given path
        try:
            folder_path = download_path + '/' + word + '/' + folder_name
            os.mkdir(folder_path)
        except FileExistsError:
            print("FOLDER ALREADY EXISTS")
            sleep(1)
    return folder_path

# Function to print some information
def infos(inst):
    print(f"Your songs will be in {inst}")
    print("Wait some seconds")

# Function to download video
def download_vid(url, answ_PS):
    install_here = get_download_path("Videos")
    print(install_here)
    print("DOWNLOADING THE BEST VIDEO QUALITY...")
    infos(install_here)
    # Download a single video
    if anws_PS == 'S':
        YouTube(url).streams.get_by_itag(137).download(install_here)
    # Download a playlist of videos
    elif anws_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: arq.streams.get_by_itag(137).first().download(install_here)

# Function to download audio
def download_aud(url, answ_PS):
    install_here = get_download_path("Music")
    print("DOWNLOADING THE BEST AUDIO QUALITY...")
    infos(install_here)
    # Download a single audio
    if anws_PS == 'S':
        YouTube(url).streams.get_by_itag(251).download(install_here)
    # Download a playlist of audios
    elif anws_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: 
            arq.streams.get_by_itag(251).download(install_here)

# Function to choose some options
def choose():
    # Choose between audio or video
    while True:
        anws_VA = str(input("What do You Want to Download: \nVIDEO [V] \nAUDIO [A] \
                        \nQUIT  [Q]\n").upper())
        if anws_VA[0] == 'V' or anws_VA[0] == 'A':
            break
        elif anws_VA == 'Q':
            quit()
        else:
            print("Wrong input! Try again.")
            sleep(2)
    os.system('clear')
    # Choose between single file or a playlist
    while True:
        anws_PS = str(input("What do You Want to Download: \nPLAYLIST [P] \nSINGLE [S]\n").upper())
        if anws_PS[0] == 'P' or anws_PS[0] == 'S':
            break
        else:
            print("Wrong input! Try again.")
            sleep(2)
    return anws_VA, anws_PS


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if request.form.get("url"):
            pass
    else:
        return render_template("index.html")   


# The main program
if __name__ == "__main__":
    app.run()
    
    # Ask for the URL
    url = input("Enter the URL: ")

    # Function return two values
    anws_VA, anws_PS = choose()
    os.system('clear')

    # If the option is video
    if anws_VA == 'V':
        download_vid(url, anws_PS)
    # If the option is audio
    elif anws_VA == 'A':
        download_aud(url, anws_PS)
