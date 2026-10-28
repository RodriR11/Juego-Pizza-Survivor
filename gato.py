import pygame
from enemigo import Enemigo


class Gato(Enemigo):
    imagen = pygame.image.load("gato.png")
    imagen = pygame.transform.scale(imagen, (54, 76))
    velocidad = 2
