import pygame
import random
import math
from enemigo import Enemigo


class Perro(Enemigo):
    imagen = pygame.image.load("perro.png")
    imagen = pygame.transform.scale(imagen, (64, 90))
    velocidad = 1.35