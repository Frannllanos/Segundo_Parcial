import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("Respuesta.jpg", 100, 40, 10, 10)
fondo_ajustes = pygame.transform.scale(pygame.image.load("Fondo_Preguntados.jpeg"), PANTALLA)

def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], lista_rankings: list) -> str:
    retorno = "rankings"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    pantalla.blit(fondo_ajustes, (0, 0))
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    mostrar_texto(pantalla, "TOP 10 PARTIDAS", (80, 50), FUENTE_TITULO_RANKING, COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_NEGRO)

    pos_y = 130
    for i in range(len(lista_rankings)):
        partida = lista_rankings[i]
        nombre = partida["nombre"][:12]
        fecha = partida["fecha"][:16]
        texto = f"{i + 1}. {nombre} - {partida['puntuacion']} pts - {fecha}"

        if i == 0:
            color = COLOR_ORO
        elif i == 1:
            color = COLOR_PLATA
        elif i == 2:
            color = COLOR_BRONCE
        else:
            color = COLOR_BLANCO

        mostrar_texto_con_contorno(pantalla, texto, (50, pos_y), FUENTE_RANKING, color, COLOR_NEGRO)
        pos_y += 55

    return retorno