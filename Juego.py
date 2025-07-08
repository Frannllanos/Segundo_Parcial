import pygame 
from Constantes import *
from Funciones import *
import random

pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load("Fondo_Preguntados.jpeg"), PANTALLA)

cuadro_bomba = crear_elemento_juego("bomba.png", 60, 60, 100, 590)
cuadro_X2 = crear_elemento_juego("icono_x2.png", 60, 60, 190, 590)
cuadro_recargar = crear_elemento_juego("icono_recargar.png", 60, 60, 300, 590)
cuadro_pasar = crear_elemento_juego("icono_pasar.png", 80, 60, 380, 590)

cuadro_pregunta = crear_elemento_juego("Pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 80, 80)
lista_respuestas = crear_lista_respuestas("Respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 125, 245)
evento_tiempo = pygame.USEREVENT 
pygame.time.set_timer(evento_tiempo, 1000)    

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict, lista_preguntas: list) -> str:
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego["indice"]]
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        print("GAME OVER")
        return "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "salir"
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                
                if cuadro_X2["rectangulo"].collidepoint(evento.pos):
                    if not datos_juego["x2_usado"]:
                        datos_juego["x2_activado"] = True
                        datos_juego["x2_usado"] = True
                        EXTRA_SONIDO.play()

                if cuadro_pasar["rectangulo"].collidepoint(evento.pos):
                    if not datos_juego["pasar_usado"]:
                        datos_juego["pasar_usado"] = True
                        datos_juego["indice"] += 1
                        if datos_juego["indice"] >= len(lista_preguntas):
                            datos_juego["indice"] = 0
                            mezclar_lista(lista_preguntas)
                        pregunta_actual = pasar_pregunta(lista_preguntas, datos_juego["indice"], cuadro_pregunta, lista_respuestas)
                        EXTRA_SONIDO.play()

                if cuadro_bomba["rectangulo"].collidepoint(evento.pos):
                    if not datos_juego["bomba_usada"]:
                        datos_juego["bomba_usada"] = True
                        datos_juego["bomba_activada"] = True

                        correcta = int(pregunta_actual["respuesta_correcta"])
                        opciones = []
                        for i in range(4):
                            if (i + 1) != correcta:
                                opciones.append(i)
                        incorrectas_a_ocultar = random.sample(opciones, 2)
                        datos_juego["indice_ocultos_bomba"] = incorrectas_a_ocultar
                        BOMBA_SONIDO.play()

                if cuadro_recargar["rectangulo"].collidepoint(evento.pos):
                    if not datos_juego["doble_chance_usada"]:
                        datos_juego["doble_chance_activada"] = True
                        datos_juego["doble_chance_usada"] = True
                        EXTRA_SONIDO.play()

                for i in range(len(lista_respuestas)):
                    if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                        respuesta = (i + 1)
                        if verificar_respuesta(datos_juego,pregunta_actual,respuesta) == True:
                            CORRECTO_SONIDO.play()
                            puntos_a_sumar = 10 
                            if datos_juego.get("x2_activado"):
                                puntos_a_sumar *= 2
                                datos_juego["x2_activado"] = False
                            datos_juego["puntuacion"] += puntos_a_sumar
                            datos_juego["racha_correctas"] += 1
                            
                            if datos_juego["racha_correctas"] == 5:
                                datos_juego["vidas"] += 1
                                datos_juego["tiempo_restante"] += 15
                                datos_juego["racha_correctas"] = 0

                            avanzar_pregunta(datos_juego, lista_preguntas, cuadro_pregunta, lista_respuestas)

                        else:
                            if datos_juego["doble_chance_activada"] and not datos_juego["esperando_segundo_intento"]:
                                datos_juego["esperando_segundo_intento"] = True
                                datos_juego["respuesta_incorrecta_1"] = respuesta
                                ERROR_SONIDO.play()
                            else:
                                ERROR_SONIDO.play()
                                datos_juego["racha_correctas"] = 0
                                datos_juego["puntuacion"] = max(0, datos_juego["puntuacion"] - 5)
                                datos_juego["esperando_segundo_intento"] = False
                                datos_juego["doble_chance_activada"] = False
                                datos_juego["x2_activado"] = False
                                avanzar_pregunta(datos_juego, lista_preguntas, cuadro_pregunta, lista_respuestas)

                        
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])
    pantalla.blit(cuadro_bomba["superficie"], cuadro_bomba["rectangulo"])
    pantalla.blit(cuadro_X2["superficie"], cuadro_X2["rectangulo"])
    pantalla.blit(cuadro_recargar["superficie"], cuadro_recargar["rectangulo"])
    pantalla.blit(cuadro_pasar["superficie"], cuadro_pasar["rectangulo"])
    
    
    for i in range(len(lista_respuestas)):
        ocultar_por_bomba = datos_juego["bomba_activada"] and i in datos_juego["indice_ocultos_bomba"]
        ocultar_por_doble_chance = datos_juego["esperando_segundo_intento"] and (i + 1) == datos_juego["respuesta_incorrecta_1"]

        if not ocultar_por_bomba and not ocultar_por_doble_chance:
            pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])

    cuadro_pregunta["superficie"] = pygame.transform.scale(pygame.image.load("Pregunta.jpg"), (ANCHO_PREGUNTA, ALTO_PREGUNTA))
    for i in range(4):
        lista_respuestas[i]["superficie"] = pygame.transform.scale(pygame.image.load("Respuesta.jpg"), (ANCHO_BOTON, ALTO_BOTON))

    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual["pregunta"], (15, 15), FUENTE_PREGUNTA, COLOR_NEGRO)
    for i in range(4):
        if not datos_juego["bomba_activada"] or i not in datos_juego["indice_ocultos_bomba"]:
            mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual[f"respuesta_{i+1}"], (15, 15), FUENTE_RESPUESTA, COLOR_NEGRO)


    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 10), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 40), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo_restante']} seg", (275, 10), FUENTE_TEXTO, COLOR_NEGRO)

    if datos_juego["x2_activado"]:
        mostrar_texto(pantalla, "X2 ACTIVADO", (380, 340), FUENTE_TEXTO, COLOR_NEGRO)
        
    if datos_juego["doble_chance_activada"]:
        mostrar_texto(pantalla, "CHANCE ACTIVADA", (380, 400), FUENTE_TEXTO, COLOR_NEGRO)

    return retorno