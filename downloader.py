import os
from yt_dlp import YoutubeDL

def download_playlist_as_mp3(playlist_url):
    # Dentro de la carpeta de Descargas del usuario, se va a crear la carpeta Music
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads\Music")
    
    # Crea la carpeta si no existe
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'noplaylist': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

# URL de la playlist de YouTube
link = input("Ingrese la playlist que desea descargar: ")
download_playlist_as_mp3(link)
