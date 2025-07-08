import pygame
from Constantes import *
from Funciones import *

pygame.init()
fuente = pygame.font.SysFont("Arial Narrow",50)
cuadro = crear_elemento_juego("Pregunta.jpg",250,50,125,240)
fondo_ajustes = pygame.transform.scale(pygame.image.load("Fondo_Configuracion.jpeg"),PANTALLA)


def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            
            if evento.key == pygame.K_RETURN:
                if len(datos_juego["nombre"]) >= 3:
                    CLICK_SONIDO.play()
                    guardar_partida(datos_juego)
                    retorno = "menu"
                                
            if letra_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]
                limpiar_superficie(cuadro,"Pregunta.jpg",250,50)
            
            if letra_presionada == "space":
                datos_juego["nombre"] += " "
            
            if len(letra_presionada) == 1:  
                if bloc_mayus != 0:
                    datos_juego["nombre"] += letra_presionada.upper()
                else:
                    datos_juego["nombre"] += letra_presionada
        
    pantalla.blit(fondo_ajustes, (0, 0))   

    pantalla.blit(cuadro["superficie"], cuadro["rectangulo"])
    mostrar_texto(cuadro["superficie"], datos_juego["nombre"], (10, 0), fuente, COLOR_NEGRO)
    mostrar_texto_con_contorno(pantalla, f"Usted obtuvo: {datos_juego['puntuacion']} puntos", (60, 160), fuente, COLOR_BLANCO, COLOR_NEGRO)
    mostrar_texto(pantalla, "Presione ENTER para guardar y volver al menu", (60, 400), fuente, COLOR_NEGRO)

    return retorno