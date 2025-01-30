import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import re

# URL de la lista de reproducción
playlist_url = 'https://www.youtube.com/watch?v=B22rWZ0MeQ0&list=PL-wEE8VmWaJ2gObUANi6vASSuWVjlB_Gb&ab_channel=GobiernodeM%C3%A9xico'


# Opciones para yt-dlp
ydl_opts = {
    'quiet': False,
    'extract_flat': 'in_playlist',
}

# Arrays para almacenar los nombres y los IDs
video_names = []
video_ids = []

# Extraer nombres e IDs usando yt-dlp
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(playlist_url, download=False)
    if 'entries' in result:
        for video in result['entries']:
            video_id = video.get('id')
            video_title = video.get('title')
            video_names.append(video_title)
            video_ids.append(video_id)

# Directorio para guardar los archivos JSON
directorio = "C:/Users/monkm/Music/mafu/"

# Descargar y guardar los subtítulos
formatter = JSONFormatter()
for video_title, video_id in zip(video_names, video_ids):
    # Limpiar el nombre del video para usarlo como nombre de archivo y añadir el ID
    safe_title = re.sub(r'[\\/*?:"<>|]', "", video_title)  # Elimina caracteres no válidos
    filename = f"{safe_title} [{video_id}]"  # Concatenación del título y el ID entre corchetes

    try:
        # Obtener los subtítulos en español, si están disponibles
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
        json_transcript = formatter.format_transcript(transcript)
        
        # Guardar el archivo JSON
        file_path = f"{directorio}{filename}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_transcript)
        print(f"Subtítulos guardados en '{file_path}'.")
    except Exception as e:
        print(f"No se pudieron obtener los subtítulos para: {filename}. Error: {e}")

print("Proceso completado.")
