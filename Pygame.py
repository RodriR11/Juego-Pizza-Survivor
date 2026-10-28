import os
import sys
import pygame
import random
import math

# En el ejecutable, usar la carpeta temporal donde PyInstaller extrae los recursos.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

from perro import Perro
from gato import Gato
from pizza import Pizza
from repartidor import Repartidor
from interfaz import Interfaz
from corazon_vida import CorazonVida
from pausa import Pausa
from pizza_extra import PizzaExtra

#Aquí inicializamos pygame
pygame.init()
pygame.mixer.init()

# Cargar los sonidos del juego. La música usa el canal de música de fondo;
# los efectos se reproducen aparte para que puedan sonar encima de ella.
pygame.mixer.music.load("MusicaFondo.mp3")
pygame.mixer.music.set_volume(0.2)
sonido_disparo = pygame.mixer.Sound("disparo.mp3")
sonido_golpe = pygame.mixer.Sound("golpe.mp3")
sonido_vida_perdida = pygame.mixer.Sound("vida_perdida.mp3")

#Crear la pantalla
ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("Pizza Survivor")
icono = pygame.image.load("pizza.png")
pygame.display.set_icon(icono)
interfaz = Interfaz(ancho_pantalla, alto_pantalla)
pausa = Pausa(ancho_pantalla, alto_pantalla)

#Fondo
fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (800,600))

# El objeto agrupa imagen, movimiento, vidas e invulnerabilidad del repartidor.
repartidor = Repartidor(368, 440, sonido_vida_perdida)

# Puntaje y tiempo pertenecen a la partida; su presentación está en Interfaz.
puntos = 0
tiempo_inicio = pygame.time.get_ticks()

# El estado y el tiempo final pertenecen a la lógica de la partida.
estado = "Jugando"
tiempo_final = None

# Intervalos de aparición por etapa: 2.5 s al inicio, 1.5 s desde los
# 30 segundos y 0.5 s desde los 60 segundos en adelante.
INTERVALO_INICIAL_ENEMIGOS = 2.5
INTERVALO_SEGUNDA_ETAPA_ENEMIGOS = 1.5
INTERVALO_MINIMO_ENEMIGOS = 0.50
DURACION_ETAPA_APARICION = 30

# Cada diez enemigos se reduce el intervalo de lanzamiento, hasta medio segundo.
INTERVALO_LANZAMIENTO_INICIAL = 1.75
REDUCCION_LANZAMIENTO_POR_MEJORA = 0.25
REDUCCION_LANZAMIENTO_MAXIMA = 1
ENEMIGOS_POR_MEJORA = 15
DURACION_MENSAJE_MEJORA = 2.5
DURACION_DISPARO_EXTRA = 15
INTERVALO_APARICION_PIZZA_EXTRA = 30


# Perros y gatos comparten la lista y el comportamiento definido en Enemigo.
tipos_enemigo = (Perro, Gato)
enemigos = [random.choice(tipos_enemigo)(random.randint(0, ancho_pantalla - 64), 0)]

#Ataque
pizzas = []
corazones_vida = []
pizzas_extra_suelo = []
tiempo_disparo_extra = 0

def lanzar_pizza():
    if not enemigos:
        return

    rectangulo_repartidor = repartidor.rectangulo
    personaje_centro_x = rectangulo_repartidor.centerx
    personaje_centro_y = rectangulo_repartidor.centery

    objetivo = 0
    distancia_menor = float("inf")

    for pe in range(len(enemigos)):
        rectangulo_enemigo = enemigos[pe].rectangulo
        distancia1 = (
                (rectangulo_enemigo.centerx - personaje_centro_x) ** 2
                + (rectangulo_enemigo.centery - personaje_centro_y) ** 2
        )

        if distancia1 < distancia_menor:
            distancia_menor = distancia1
            objetivo = pe

    rectangulo_objetivo = enemigos[objetivo].rectangulo
    dis_x = rectangulo_objetivo.centerx - personaje_centro_x
    dis_y = rectangulo_objetivo.centery - personaje_centro_y
    distancia1 = math.hypot(dis_x, dis_y)

    if distancia1 > 0:
        pizzas.append(Pizza(
            personaje_centro_x - 16,
            personaje_centro_y - 16,
            dis_x / distancia1 * Pizza.velocidad,
            dis_y / distancia1 * Pizza.velocidad
        ))
        # Reproducir el efecto solo si realmente se lanzó una pizza.
        sonido_disparo.play()

def agregar_enemigo():
    # Elegir el tipo aleatoriamente y usar sus dimensiones al ubicarlo.
    tipo_enemigo = random.choice(tipos_enemigo)
    ancho_enemigo = tipo_enemigo.imagen.get_width()
    alto_enemigo = tipo_enemigo.imagen.get_height()
    bordes = {
        "arriba": (
            (0, ancho_pantalla - ancho_enemigo),
            (-alto_enemigo, -alto_enemigo)
        ),
        "abajo": (
            (0, ancho_pantalla - ancho_enemigo),
            (alto_pantalla, alto_pantalla)
        ),
        "izquierda": (
            (-ancho_enemigo, -ancho_enemigo),
            (0, alto_pantalla - alto_enemigo)
        ),
        "derecha": (
            (ancho_pantalla, ancho_pantalla),
            (0, alto_pantalla - alto_enemigo)
        )
    }
    rango_x, rango_y = random.choice(list(bordes.values()))
    enemigos.append(tipo_enemigo(
        random.randint(*rango_x),
        random.randint(*rango_y)
    ))


def agregar_corazon_vida():
    ancho_corazon = CorazonVida.imagen.get_width()
    alto_corazon = CorazonVida.imagen.get_height()
    corazones_vida.append(CorazonVida(
        random.randint(0, ancho_pantalla - ancho_corazon),
        random.randint(0, alto_pantalla - alto_corazon),
    ))


def agregar_pizza_extra():
    ancho_pizza_extra = PizzaExtra.imagen.get_width()
    alto_pizza_extra = PizzaExtra.imagen.get_height()
    pizzas_extra_suelo.append(PizzaExtra(
        random.randint(0, ancho_pantalla - ancho_pizza_extra),
        random.randint(0, alto_pantalla - alto_pizza_extra),
    ))


def registrar_enemigo_derrotado():
    global puntos, tiempo_mensaje_mejora, mensaje_mejora

    puntos += 1
    mejoras_maximas = int(
        REDUCCION_LANZAMIENTO_MAXIMA / REDUCCION_LANZAMIENTO_POR_MEJORA
    )
    if (
        puntos % ENEMIGOS_POR_MEJORA == 0
        and puntos // ENEMIGOS_POR_MEJORA <= mejoras_maximas
    ):
        tiempo_mensaje_mejora = DURACION_MENSAJE_MEJORA
        if puntos // ENEMIGOS_POR_MEJORA == mejoras_maximas:
            mensaje_mejora = "¡Mejora máxima!"
        else:
            mensaje_mejora = "¡Lanzador mejorado!"


def colisiones():
    global pizzas, enemigos, puntos, tiempo_mensaje_mejora
    global mensaje_mejora, corazones_vida, pizzas_extra_suelo
    global tiempo_disparo_extra

    pizzas_sobrevivientes = []
    enemigos_sobrevivientes = list(enemigos)
    for pizza_actual in pizzas:
        pizza_choco = False

        for enemigo_actual in enemigos_sobrevivientes[:]:
            if pizza_actual.rectangulo.colliderect(enemigo_actual.rectangulo):
                enemigos_sobrevivientes.remove(enemigo_actual)
                pizza_choco = True
                registrar_enemigo_derrotado()
                # Sonar cada vez que una pizza acierta a un enemigo.
                sonido_golpe.play()
                break
        if not pizza_choco:
            pizzas_sobrevivientes.append(pizza_actual)

    pizzas = pizzas_sobrevivientes

    # La estrella derrota a los enemigos por contacto; sin ella, recibir daño
    # sigue sujeto al periodo de invulnerabilidad del repartidor.
    if repartidor.estrella_activa:
        for enemigo_actual in enemigos_sobrevivientes[:]:
            if repartidor.rectangulo.colliderect(enemigo_actual.rectangulo):
                enemigos_sobrevivientes.remove(enemigo_actual)
                registrar_enemigo_derrotado()
                sonido_golpe.play()
    elif repartidor.tiempo_invulnerable <= 0:
        for enemigo_actual in enemigos_sobrevivientes[:]:
            if repartidor.rectangulo.colliderect(enemigo_actual.rectangulo):
                enemigos_sobrevivientes.remove(enemigo_actual)
                repartidor.recibir_golpe()
                break
    enemigos = enemigos_sobrevivientes

    # El corazón cura si falta vida o activa la estrella si ya está al máximo.
    if repartidor.vidas > 0:
        for corazon_actual in corazones_vida[:]:
            if repartidor.rectangulo.colliderect(corazon_actual.rectangulo):
                if repartidor.recuperar_vida():
                    corazones_vida.remove(corazon_actual)
                else:
                    repartidor.activar_estrella()
                    corazones_vida.remove(corazon_actual)
                break

    # Recoger la pizza activa el disparo extra y elimina el objeto del suelo.
    for pizza_extra_actual in pizzas_extra_suelo[:]:
        if repartidor.rectangulo.colliderect(pizza_extra_actual.rectangulo):
            pizzas_extra_suelo.remove(pizza_extra_actual)
            tiempo_disparo_extra = DURACION_DISPARO_EXTRA
            break


def actualizar_juego(delta_time):
    # Solo los temporizadores del loop necesitan reasignarse aquí.
    global tiempo_ultimo_lanzamiento, tiempo_ultimo_enemigo
    global tiempo_ultimo_corazon
    global tiempo_ultima_pizza_extra, tiempo_disparo_extra
    global tiempo_mensaje_mejora
    global estado, tiempo_final

    tiempo_mensaje_mejora = max(0, tiempo_mensaje_mejora - delta_time)
    tiempo_disparo_extra = max(0, tiempo_disparo_extra - delta_time)

    # Delegar al objeto su movimiento, límites e invulnerabilidad.
    repartidor.actualizar(delta_time, ancho_pantalla, alto_pantalla)

    # Calcular la etapa actual de aparición según el tiempo transcurrido.
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
    if tiempo_transcurrido < DURACION_ETAPA_APARICION * 1000:
        intervalo_enemigos = INTERVALO_INICIAL_ENEMIGOS
    elif tiempo_transcurrido < DURACION_ETAPA_APARICION * 2 * 1000:
        intervalo_enemigos = INTERVALO_SEGUNDA_ETAPA_ENEMIGOS
    else:
        intervalo_enemigos = INTERVALO_MINIMO_ENEMIGOS

    # Cada etapa genera enemigos más seguido, hasta el intervalo mínimo.
    tiempo_ultimo_enemigo += delta_time
    if tiempo_ultimo_enemigo >= intervalo_enemigos:
        agregar_enemigo()
        tiempo_ultimo_enemigo = 0

    # Crear un corazón coleccionable cada 20 segundos.
    tiempo_ultimo_corazon += delta_time
    if tiempo_ultimo_corazon >= 20:
        agregar_corazon_vida()
        tiempo_ultimo_corazon = 0

    # Actualizar la vida de los corazones y quitar los que ya expiraron.
    for i in range(len(corazones_vida) - 1, -1, -1):
        if not corazones_vida[i].actualizar(delta_time):
            corazones_vida.pop(i)

    # Aparece una pizza coleccionable cada 30 segundos y expira a los 5.
    tiempo_ultima_pizza_extra += delta_time
    if tiempo_ultima_pizza_extra >= INTERVALO_APARICION_PIZZA_EXTRA:
        agregar_pizza_extra()
        tiempo_ultima_pizza_extra = 0

    for i in range(len(pizzas_extra_suelo) - 1, -1, -1):
        if not pizzas_extra_suelo[i].actualizar(delta_time):
            pizzas_extra_suelo.pop(i)

    # Cada enemigo se mueve con la velocidad fija definida en su clase.
    for enemigo_actual in enemigos:
        enemigo_actual.mover_hacia(
            repartidor.x,
            repartidor.y,
            delta_time,
        )

    # Reducir el tiempo entre lanzamientos cada diez enemigos, hasta 1.25 s.
    mejoras_lanzador = min(
        puntos // ENEMIGOS_POR_MEJORA,
        int(REDUCCION_LANZAMIENTO_MAXIMA / REDUCCION_LANZAMIENTO_POR_MEJORA),
    )
    intervalo_lanzamiento = (
        INTERVALO_LANZAMIENTO_INICIAL
        - mejoras_lanzador * REDUCCION_LANZAMIENTO_POR_MEJORA
    )
    tiempo_ultimo_lanzamiento += delta_time
    if tiempo_ultimo_lanzamiento >= intervalo_lanzamiento:
        lanzar_pizza()
        tiempo_ultimo_lanzamiento = 0

    # Mover pizzas y quitar de la lista las que salen de la pantalla.
    for i in range(len(pizzas) - 1, -1, -1):
        pizzas[i].mover(delta_time)
        if pizzas[i].fuera_de_pantalla(ancho_pantalla, alto_pantalla):
            pizzas.pop(i)

    # Resolver colisiones antes de dibujar el fotograma.
    colisiones()

    # Guardar el tiempo y detener la música al perder la última vida.
    if repartidor.vidas <= 0:
        estado = "Terminado"
        tiempo_final = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        pygame.mixer.music.stop()


def dibujar_juego():
    # Dibujar el fondo y los elementos que permanecen visibles al terminar.
    pantalla.blit(fondo, (0, 0))

    repartidor.dibujar(pantalla)

    interfaz.dibujar_vidas(pantalla, repartidor.vidas)
    interfaz.dibujar_puntaje(pantalla, puntos)

    for enemigo_actual in enemigos:
        enemigo_actual.dibujar(pantalla)
    for corazon_actual in corazones_vida:
        corazon_actual.dibujar(pantalla)
    for pizza_extra_actual in pizzas_extra_suelo:
        pizza_extra_actual.dibujar(pantalla)
    for pizza_actual in pizzas:
        pizza_actual.dibujar(pantalla)

    interfaz.dibujar_cronometro(
        pantalla, estado, tiempo_inicio, tiempo_final
    )
    if tiempo_mensaje_mejora > 0:
        interfaz.dibujar_mensaje_mejora(pantalla, mensaje_mejora)

    # La interfaz encapsula la pantalla de fin de juego.
    if estado == "Terminado":
        interfaz.dibujar_pantalla_fin(pantalla, puntos, tiempo_final)



#Loop del juego
se_ejecuta = True

reloj = pygame.time.Clock()
tiempo_ultimo_lanzamiento = 0
tiempo_ultimo_enemigo = 0
tiempo_ultimo_corazon = 0
tiempo_ultima_pizza_extra = 0
tiempo_mensaje_mejora = 0
mensaje_mejora = ""
# Iniciar la música en bucle al comenzar el juego, con volumen reducido.
pygame.mixer.music.play(-1)
while se_ejecuta:

    delta_time = reloj.tick(60)/1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        elif (
            estado == "Jugando"
            and evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_ESCAPE
        ):
            duracion_pausa = pausa.alternar()
            if pausa.pausado:
                pygame.mixer.music.pause()
            else:
                # Excluir la pausa del cronómetro y del escalado de dificultad.
                tiempo_inicio += duracion_pausa
                pygame.mixer.music.unpause()

        # Solo enviar controles al repartidor durante el juego activo.
        elif estado == "Jugando" and not pausa.pausado:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                # Ignorar repeticiones si la tecla permanece presionada.
                if (
                    not getattr(evento, "repeat", False)
                    and tiempo_disparo_extra > 0
                ):
                    lanzar_pizza()
            else:
                repartidor.manejar_evento(evento)

    # Actualizar movimiento, generación y colisiones únicamente durante la partida.
    if estado == "Jugando" and not pausa.pausado:
        actualizar_juego(delta_time)

    # El dibujo continúa en ambos estados; en el final solo se renderiza la escena.
    dibujar_juego()
    pausa.dibujar(pantalla)
    pygame.display.update()


pygame.quit()
