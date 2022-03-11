import os
from pytube import YouTube, streams

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def download_vid(url):
    stream = url.streams.get_by_itag(137)
    stream.download(get_download_path())

def download_aud(url):
    stream = url.streams.get_by_itag(251)
    stream.download(get_download_path())

def anws_vid_aud(anws):
    url = YouTube(input("Enter the URL: "))
    if anws[0] == 'v':
        download_vid(url)
    elif anws[0] == 'a':
        download_aud(url)
    else:
        print("Wrong input! Try again.")

def main():
    anws_vid_aud(str(input("You want to download a video or audio? ").lower()))

if __name__ == "__main__":
    main()
