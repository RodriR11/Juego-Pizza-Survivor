import pygame


class PizzaExtra:
    duracion = 5
    duracion_titileo = 1
    intervalo_titileo_ms = 100
    imagen = pygame.transform.scale(
        pygame.image.load("pizza.png"),
        (40, 40)
    )

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiempo_restante = self.duracion

    @property
    def rectangulo(self):
        return self.imagen.get_rect(topleft=(self.x, self.y))

    def actualizar(self, delta_time):
        self.tiempo_restante -= delta_time
        return self.tiempo_restante > 0

    def dibujar(self, superficie):
        debe_titilar = self.tiempo_restante <= self.duracion_titileo
        visible = (
            not debe_titilar
            or pygame.time.get_ticks() // self.intervalo_titileo_ms % 2 == 0
        )
        if visible:
            superficie.blit(self.imagen, (self.x, self.y))
