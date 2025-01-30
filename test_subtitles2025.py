from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import re

# URL de la lista de reproducción
playlist_url = 'https://www.youtube.com/watch?v=B22rWZ0MeQ0&list=PL-wEE8VmWaJ2gObUANi6vASSuWVjlB_Gb'

# Crea una instancia de Playlist
playlist = Playlist(playlist_url)

# Formateador para convertir la transcripción a JSON
formatter = JSONFormatter()

# Directorio para guardar los archivos JSON
directorio = "C:/Users/monkm/Music/mafu/"

# Recorre cada video en la lista de reproducción
for video in playlist.videos:
    video_id = video.video_id
    video_title = video.title

    # Limpia el título para usarlo como nombre de archivo
    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", video_title)  # Elimina caracteres inválidos para nombres de archivo

    print(f'Procesando video: {video_title} (ID: {video_id})')

    try:
        # Obtener los subtítulos en español, si están disponibles
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
        json_transcript = formatter.format_transcript(transcript)

        # Ruta del archivo con el nombre del video
        file_path = directorio + titulo_limpio + ' ' + '[' + video_id + '].json'

        # Escribir el JSON a un archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_transcript)
        print(f"Subtítulos guardados en '{file_path}'.")

    except Exception as e:
        print(f"No se pudieron obtener los subtítulos para: {video_title} (ID: {video_id}). Error: {e}")

print("Proceso completado.")
