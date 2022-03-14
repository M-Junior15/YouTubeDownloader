import os
from pytube import YouTube, Playlist
from time import sleep

def get_download_path(word):
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        folder_name = input("Enter your folder name: ")
        download_path = os.path.join(os.path.expanduser('~'))
        try:
            folder_path = download_path + '/' + word + '/' + folder_name
            os.mkdir(folder_path)
        except FileExistsError:
            print("FOLDER ALREADY EXISTS")
            sleep(1)
        return folder_path

def infos(inst):
    print(f"Your songs will be in {inst}")
    print("Wait some seconds")

def download_vid(url, answ_PS):
    install_here = get_download_path("Videos")
    print("DOWNLOADING THE BEST VIDEO QUALITY...")
    infos(install_here)
    if anws_PS == 'S':
        YouTube(url).streams.get_by_itag(137).download(install_here)
    elif anws_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: arq.streams.get_by_itag(137).first().download(install_here)

def download_aud(url, answ_PS):
    install_here = get_download_path("Music")
    print("DOWNLOADING THE BEST AUDIO QUALITY...")
    infos(install_here)
    if anws_PS == 'S':
        YouTube(url).streams.get_by_itag(251).download(install_here)
    elif anws_PS == 'P':
        playlist = Playlist(url)
        for arq in playlist.videos: arq.streams.get_by_itag(251).download(install_here)

def choose():
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
    while True:
        anws_PS = str(input("What do You Want to Download: \nPLAYLIST [P] \nSINGLE [S]\n").upper())
        if anws_PS[0] == 'P' or anws_PS[0] == 'S':
            break
        else:
            print("Wrong input! Try again.")
            sleep(2)
    return anws_VA, anws_PS

if __name__ == "__main__":
    url = input("Enter the URL: ")
    anws_VA, anws_PS = choose()
    os.system('clear')
    if anws_VA == 'V':
        download_vid(url, anws_PS)
    elif anws_VA == 'A':
        download_aud(url, anws_PS)
