import pygame


class Pizza:
    imagen = pygame.transform.scale(
        pygame.image.load("pizza.png"),
        (32, 32)
    )
    velocidad = 500

    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    @property
    def rectangulo(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.imagen.get_width(),
            self.imagen.get_height()
        )

    def mover(self, delta_time):
        self.x += self.velocidad_x * delta_time
        self.y += self.velocidad_y * delta_time

    def fuera_de_pantalla(self, ancho, alto):
        rectangulo = self.rectangulo
        return (
            rectangulo.right < 0
            or rectangulo.left > ancho
            or rectangulo.bottom < 0
            or rectangulo.top > alto
        )

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, self.y))
