import pygame


class Pausa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.pausado = False
        self.inicio_pausa = None
        self.fuente = pygame.font.Font(None, 72)
        self.fuente_instruccion = pygame.font.Font(None, 32)

    def alternar(self):
        ahora = pygame.time.get_ticks()

        if not self.pausado:
            self.pausado = True
            self.inicio_pausa = ahora
            return 0

        duracion_pausa = ahora - self.inicio_pausa
        self.pausado = False
        self.inicio_pausa = None
        return duracion_pausa

    def dibujar(self, superficie):
        if not self.pausado:
            return

        capa = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 180))
        superficie.blit(capa, (0, 0))

        titulo = self.fuente.render("PAUSA", True, (255, 255, 255))
        superficie.blit(
            titulo,
            titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 20)),
        )

        instruccion = self.fuente_instruccion.render(
            "Presiona ESC para continuar", True, (255, 255, 255)
        )
        superficie.blit(
            instruccion,
            instruccion.get_rect(
                center=(self.ancho // 2, self.alto // 2 + 35)
            ),
        )
