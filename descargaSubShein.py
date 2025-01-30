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


directorio = "C:/Users/monkm/Music/mafu/"#directorio para guardado de subtitulos
links_lista = []
prefijo_youtube = 'https://www.youtube.com/watch?v='
def obtener_lista(url):
    df = pd.DataFrame()  # Inicializa df para asegurar su existencia
    try:
        links_lista = Playlist(url)
        links = Playlist(url)
        print(links_lista)
        if links:
            for link in links_lista:
                try:
                    posicion = link.find(s) + 1
                    url_actual = link[posicion:]
                    video_actual = YouTube(prefijo_youtube + url_actual)
                    transcripcion = YouTubeTranscriptApi.get_transcript(video_actual.video_id, languages=['es'])
                    formateador = JSONFormatter()
                    json_formateador = formateador.format_transcript(transcripcion)
                    titulo_actual = video_actual.title
                    titulo_actual = re.sub(r'\|', '｜', titulo_actual)
                    print("Descargando: " + titulo_actual + ".json")
                    with open(directorio + str(titulo_actual) + ' ' + '[' + str(video_actual.video_id) + ']' + '.json', 'w', encoding='utf-8') as archivo_json:
                        archivo_json.write(json_formateador)
                        print("Se ha descargado correctamente: " + str(titulo_actual) + ".json")
                    json_name.append(str(titulo_actual) + '.json')
                    mp4_name.append(str(titulo_actual) + ' ' + '[' + str(video_actual.video_id) + ']' + '.mp4')
                except Exception as e:
                    print(e)
                    continue
                a = np.array(json_name)
                b = np.array(mp4_name)
                df = pd.DataFrame({"json": a, "mp4": b})
                json_name.clear()
                mp4_name.clear()
            if not df.empty:
                df.to_csv('ruta_para_guardar.csv', index=False)  # Asegúrate de proporcionar una ruta válida aquí
        else:
            print("Error al obtener la lista de reproducción")
    except Exception as e:
        raise Exception("Error al obtener la lista de reproducción")  # Lanza correctamente la excepción

#obtener_lista("https://www.youtube.com/watch?v=7JGurIQYm90&list=PL-wEE8VmWaJ1XfDoFFkVfxuwVRgBMIiNO&ab_channel=GobiernodeM%C3%A9xico")   
obtener_lista("https://www.youtube.com/watch?v=B22rWZ0MeQ0&list=PL-wEE8VmWaJ2gObUANi6vASSuWVjlB_Gb")