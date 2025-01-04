import os
from yt_dlp import YoutubeDL

def download_playlist_as_mp3(playlist_url, destination_directory):
    # Obtén la carpeta de Descargas del usuario
    downloads_folder = os.path.join(os.path.expanduser("~"), destination_directory)
    
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
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Asegura que se use downloads_folder
        'noplaylist': False,  # Procesa listas de reproducción completas
        'quiet': True,  # Reduce la salida en consola
    }

    with YoutubeDL(ydl_opts) as ydl:
        # Obtén la información de los videos en la playlist
        playlist_info = ydl.extract_info(playlist_url, download=False)
        videos = playlist_info.get('entries', [])
        
        print(f"\nDescargando playlist: {playlist_info.get('title', 'Sin título')}")
        print("El proceso puede demorar un poco, sea paciente.\n")
        
        for video in videos:
            video_title = video.get('title')
            video_id = video.get('id')
            if not video_title or not video_id:
                print("No se pudo obtener información del video. Saltando...")
                continue
            
            # Nombre del archivo esperado
            mp3_filename = os.path.join(downloads_folder, f"{video_title}.mp3")
            
            if os.path.exists(mp3_filename):
                print(f"[SKIP] Ya descargado: {video_title}")
                continue  # Saltar al siguiente video
            
            print(f"[DESCARGANDO] {video_title}")
            try:
                # Descarga y convierte el video a MP3
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                print(f"[COMPLETADO] {video_title}")
            except Exception as e:
                print(f"[ERROR] No se pudo descargar {video_title}: {e}")

# URL de la playlist de YouTube
destination_directory = "Downloads/Music"
link = input("\nIngrese la playlist que desea descargar: ")
download_playlist_as_mp3(link, destination_directory)
print("\nLa descarga ha finalizado.\n")