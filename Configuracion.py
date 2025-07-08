import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("mas.webp",60,60,420,200)
boton_resta = crear_elemento_juego("menos.webp",60,60,20,200)
boton_mute = crear_elemento_juego("mute_on.png", 60, 60, 220, 400)
boton_unmute = crear_elemento_juego("mute_off.png", 60, 60, 220, 400)

boton_volver = crear_elemento_juego("Respuesta.jpg",100,40,10,10)
fondo_ajustes = pygame.transform.scale(pygame.image.load("Fondo_Configuracion.jpeg"), PANTALLA)


def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
            pass
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
                elif boton_mute["rectangulo"].collidepoint(evento.pos) or boton_unmute["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    datos_juego["musica_activada"] = not datos_juego["musica_activada"]
                    if datos_juego["musica_activada"]:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    else:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.set_volume(0)
    
    pantalla.blit(fondo_ajustes, (0, 0))

    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])

    if datos_juego["musica_activada"]:
        pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])
    else:
        pantalla.blit(boton_unmute["superficie"], boton_unmute["rectangulo"])

    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']} %", (200, 200), FUENTE_VOLUMEN, COLOR_NEGRO)

    if datos_juego["musica_activada"]:
        estado_musica = "MUSICA ACTIVADA"
    else:
        estado_musica = "MUSICA MUTEADA"

    mostrar_texto(pantalla, estado_musica, (160, 370), FUENTE_RESPUESTA, COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_NEGRO)

    return retorno

#def manejar_botones_ajustes()