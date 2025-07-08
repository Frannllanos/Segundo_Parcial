import json
from datetime import datetime
import random
from Constantes import *
import pygame
import os

#GENERAL
def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """Muestra texto multilinea con ajuste de linea en una superficie

    Args:
        surface (Surface): superficie destino
        text (str): texto a mostrar
        pos (tuple): posicion x, y inicial
        font (Font): fuente usada
        color (Color, optional): color del texto. Defaults to negro
    """
    words = [word.split(' ') for word in text.splitlines()] 
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0] 
                y += word_height  
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0] 
        y += word_height  

#GENERAL
def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    """Crea un diccionario con superficie y rectangulo para un elemento del juego

    Args:
        textura (str): ruta de la imagen
        ancho (int): ancho de la superficie
        alto (int): alto de la superficie
        pos_x (int): posicion horizontal
        pos_y (int): posicion vertical

    Returns:
        dict: contiene la superficie escalada y su rectangulo
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x,pos_y,ancho,alto)
    return elemento_juego

#GENERAL
def crear_lista_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int):
    """Crea una lista con 4 respuestas graficas usando una textura

    Args:
        textura (str): ruta de la imagen
        ancho (int): ancho de cada respuesta
        alto (int): alto de cada respuesta
        pos_x (int): posicion horizontal inicial
        pos_y (int): posicion vertical inicial

    Returns:
        list: lista con 4 respuestas tipo dict (superficie y rectangulo)
    """
    lista_respuestas = []
    for i in range(4):
        respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 80    
    return lista_respuestas

#ESPECIFICA
def crear_botones_menu() -> list:
    """Crea los botones del menu principal con una textura

    Returns:
        list: lista de botones como diccionarios con superficie y rectangulo
    """
    lista_botones = []
    pos_x = 125
    pos_y = 115
    for i in range(4):
        boton = crear_elemento_juego("Respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,pos_x,pos_y)
        pos_y += 80
        lista_botones.append(boton)
    return lista_botones

#GENERAL
def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int):
    """Restaura la superficie de un elemento con su textura original

    Args:
        elemento_juego (dict): diccionario con superficie y rectangulo
        textura (str): ruta de la imagen
        ancho (int): ancho deseado
        alto (int): alto deseado
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))

#GENERAL
def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    """Verifica si la respuesta es correcta

    Args:
        datos_juego (dict): datos de la partida
        pregunta_actual (dict): pregunta mostrada
        respuesta (int): opcion elegida

    Returns:
        bool: True si es correcta, False si no
    """
    if pregunta_actual["respuesta_correcta"] == respuesta:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO   
        retorno = True         
    else:
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
        datos_juego["vidas"] -= 1
        retorno = False
    return retorno

#GENERAL
def reiniciar_estadisticas(datos_juego:dict):
    """Reinicia las estadisticas del juego

    Args:
        datos_juego (dict): datos de la partida
    """
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = TIEMPO_JUEGO
    datos_juego["racha_correctas"] = 0
    datos_juego["indice"] = 0

#ESPECIFICA
def pasar_pregunta(lista_preguntas:list,indice:int,cuadro_pregunta:dict,lista_respuestas:list) -> dict:
    """Pasa a la siguiente pregunta y limpia superficies

    Args:
        lista_preguntas (list): lista de preguntas
        indice (int): indice actual
        cuadro_pregunta (dict): superficie de la pregunta
        lista_respuestas (list): lista de respuestas

    Returns:
        dict: pregunta actual
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(cuadro_pregunta,"Pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"Respuesta.jpg",ANCHO_BOTON,ALTO_BOTON)
    return pregunta_actual

#GENERAL
def mezclar_lista(lista_preguntas:list) -> None:
    """Mezcla aleatoriamente la lista de preguntas

    Args:
        lista_preguntas (list): lista a mezclar
    """
    random.shuffle(lista_preguntas)

#ESPECIFICA
def leer_csv_preguntas(nombre_archivo: str, lista_preguntas: list, separador: str = ",") -> bool:
    """Lee las preguntaas del archivo csv

    Args:
        nombre_archivo (str): direccion del archivo
        lista_preguntas (list): lista
        separador (str, optional): separador. Defaults to ",".

    Returns:
        bool: un estado
    """
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            archivo.readline() 
            for linea in archivo:
                linea = linea.strip()
                datos = linea.split(separador)
                if len(datos) == 6:
                    pregunta = {
                        "pregunta": datos[0],
                        "respuesta_1": datos[1],
                        "respuesta_2": datos[2],
                        "respuesta_3": datos[3],
                        "respuesta_4": datos[4],
                        "respuesta_correcta": int(datos[5])
                    }
                    lista_preguntas.append(pregunta)
        return True
    else:
        return False

#GENERAL
def guardar_partida(datos_juego:dict) -> None:
    """Guarda los datos de la partida en un archivo JSON

    Args:
        datos_juego (dict): datos de la partida
    """
    nueva_partida = {
        "nombre": datos_juego["nombre"],
        "puntuacion": datos_juego["puntuacion"],
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            partidas = json.load(archivo)
    except FileNotFoundError:
        partidas = []
    partidas.append(nueva_partida)
    with open("partidas.json", "w", encoding="utf-8") as archivo:
        json.dump(partidas, archivo, indent=4)

#ESPECIFICA
def obtener_top_10() -> list:
    """Devuelve la lista con las 10 mejores partidas

    Returns:
        list: lista de partidas ordenadas por puntaje
    """
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            partidas = json.load(archivo)
    except FileNotFoundError:
        return []

    for i in range(len(partidas) - 1):
        for j in range(len(partidas) - 1 - i):
            if partidas[j]["puntuacion"] < partidas[j + 1]["puntuacion"]:
                aux = partidas[j]
                partidas[j] = partidas[j + 1]
                partidas[j + 1] = aux

    return partidas[:10]

#ESPECIFICA
def avanzar_pregunta(datos_juego, lista_preguntas, cuadro_pregunta, lista_respuestas):
    """Pasa a la siguiente pregunta y reinicia los estados

    Args:
        datos_juego (dict): datos del juego
        lista_preguntas (list): lista de preguntas
        cuadro_pregunta (dict): superficie de la pregunta
        lista_respuestas (list): superficies de las respuestas
    """
    datos_juego["indice"] += 1
    if datos_juego["indice"] >= len(lista_preguntas):
        datos_juego["indice"] = 0
        mezclar_lista(lista_preguntas)

    datos_juego["respuesta_incorrecta_1"] = None
    datos_juego["esperando_segundo_intento"] = False
    datos_juego["doble_chance_activada"] = False
    datos_juego["bomba_activada"] = False
    datos_juego["indice_ocultos_bomba"] = []

    pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)

#GENERAL
def mostrar_texto_con_contorno(superficie, texto, posicion, fuente, color_texto, color_contorno, grosor=1):
    """Dibuja un texto con contorno sobre una superficie

    Args:
        superficie (Surface): superficie destino
        texto (str): texto a mostrar
        posicion (tuple): coordenadas x, y
        fuente (Font): fuente usada
        color_texto (tuple): color del texto
        color_contorno (tuple): color del contorno
        grosor (int, optional): grosor del contorno. Defaults to 1.
    """
    x, y = posicion
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx != 0 or dy != 0:
                texto_sombra = fuente.render(texto, True, color_contorno)
                superficie.blit(texto_sombra, (x + dx, y + dy))
    texto_principal = fuente.render(texto, True, color_texto)
    superficie.blit(texto_principal, (x, y))
