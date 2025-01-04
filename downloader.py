import os
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor

def download_video_as_mp3(video_info, music_folder):
    video_title = video_info.get('title')
    video_id = video_info.get('id')
    if not video_title or not video_id:
        print("No se pudo obtener información del video. Saltando...")
        return

    mp3_filename = os.path.join(music_folder, f"{video_title}.mp3")
    if os.path.exists(mp3_filename):
        print(f"[SKIP] Ya descargado: {video_title}")
        return

    print(f"[DESCARGANDO] {video_title}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(music_folder, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        print(f"[COMPLETADO] {video_title}")
    except Exception as e:
        print(f"[ERROR] No se pudo descargar {video_title}: {e}")

def download_playlist_as_mp3(playlist_url: str, destination_folder: str):
    music_folder = os.path.join(os.path.expanduser("~"), destination_folder)

    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        videos = playlist_info.get('entries', [])

    print(f"\nDescargando playlist: {playlist_info.get('title', 'Sin título')} con {len(videos)} videos.\n")

    with ThreadPoolExecutor(max_workers=5) as executor:
        for video_info in videos:
            executor.submit(download_video_as_mp3, video_info, music_folder)

destination_folder = "Downloads/Music"
link = input("\nIngrese la playlist que desea descargar: ")
download_playlist_as_mp3(link, destination_folder)
print("\nLa descarga ha finalizado.\n")