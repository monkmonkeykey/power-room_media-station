# -*- coding: utf-8 -*-
from pytube import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import time
import numpy as np
import pandas as pd
import os
import urllib.parse
import re
s = '='
contador = 0
json_name = []
mp4_name = []


directorio = "C:/Users/luzma/Videos/power_room/subSheinES/json/"#directorio para guardado de subtitulos
links_lista = []
prefijo_youtube = 'https://www.youtube.com/watch?v='
def obtener_lista(url):
    try:
        links_lista = Playlist(url)
        if not links_lista:
            raise Exception("La lista de reproducción está vacía o la URL no es válida.")

        df = pd.DataFrame(columns=["json", "mp4"])  # Inicializar DataFrame vacío

        for link in links_lista:
            try:
                posicion = link.find("=") + 1
                url_actual = link[posicion:]
                video_actual = YouTube(prefijo_youtube + url_actual)
                transcripcion = YouTubeTranscriptApi.get_transcript(video_actual.video_id, languages=['es'])
                formateador = JSONFormatter()
                json_formateador = formateador.format_transcript(transcripcion)

                titulo_actual = re.sub(r'\|', '｜', video_actual.title)
                print("Descargando: " + titulo_actual + ".json")

                with open(directorio + titulo_actual + ' [' + video_actual.video_id + '].json', 'w', encoding='utf-8') as archivo_json:
                    archivo_json.write(json_formateador)
                    print("Se ha descargado correctamente: " + titulo_actual + ".json")

                json_name.append(titulo_actual + '.json')
                mp4_name.append(titulo_actual + ' [' + video_actual.video_id + '].mp4')

            except Exception as e:
                print(f"Error con {link}: {e}")
                continue

        # Verifica si hay datos antes de intentar guardarlos
        if json_name and mp4_name:
            df = pd.DataFrame({"json": json_name, "mp4": mp4_name})
            df.to_csv("output.csv", index=False)  # Guarda en un archivo válido

    except Exception as e:
        raise Exception("Error al obtener la lista de reproducción: " + str(e))

# Llamada a la función
obtener_lista("https://www.youtube.com/watch?v=B22rWZ0MeQ0&list=PL-wEE8VmWaJ2gObUANi6vASSuWVjlB_Gb")
