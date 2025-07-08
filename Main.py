import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configuracion import *
from Funciones import *
from Rankings import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS 114")
icono = pygame.image.load("Icono_Preguntados.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
corriendo = True
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":TIEMPO_JUEGO,"volumen_musica":20,"indice":0,"racha_correctas":0,"musica_activada": True, "x2_activado": False, "x2_usado": False, "pasar_usado": False, "bomba_usada": False, "bomba_activada": False, "doble_chance_usada": False, "doble_chance_activada": False, "esperando_segundo_intento": False, "respuesta_incorrecta_1": None, "indice_ocultos_bomba": []}

lista_rankings = []
reloj = pygame.time.Clock()
ventana_actual = "menu"
ventana_anterior = ""

bandera_juego = False
lista_preguntas = []

if leer_csv_preguntas("Preguntas.csv", lista_preguntas):
    mezclar_lista(lista_preguntas)
else:
    print("Error: no se pudo leer el archivo de preguntas.")

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "salir":
        corriendo = False
    if ventana_actual == "rankings":
        lista_rankings = obtener_top_10()
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, lista_rankings)
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "juego":
        if bandera_juego == False:
            pygame.mixer.init()
            pygame.mixer.music.load("videoplayback-_1_.mp3")
            if datos_juego["musica_activada"]:
                pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            else:
                pygame.mixer.music.set_volume(0)
            pygame.mixer.music.play(-1)
            bandera_juego = True

        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego,lista_preguntas)

    elif ventana_actual == "terminado":
        if bandera_juego == True:
            bandera_juego = False
            pygame.mixer.music.stop()

        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego)

    pygame.display.flip()

pygame.quit()