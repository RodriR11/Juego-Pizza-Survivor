import pygame
import math
import random

class Enemigo:
    imagen = None
    velocidad = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def rectangulo(self):
        # El rectángulo de colisión utiliza las dimensiones de la imagen.
        return pygame.Rect(
            self.x,
            self.y,
            self.imagen.get_width(),
            self.imagen.get_height()
        )

    def mover_hacia(self, objetivo_x, objetivo_y, delta_time):
        # Cada enemigo se mueve hacia el objetivo a su propia velocidad.
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            self.x += dx / distancia * self.velocidad * 60 * delta_time
            self.y += dy / distancia * self.velocidad * 60 * delta_time

    def dibujar(self, superficie):
        # Dibujar la imagen definida por la clase concreta del enemigo.
        superficie.blit(self.imagen, (self.x, self.y))