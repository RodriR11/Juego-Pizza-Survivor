import pygame


class Interfaz:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.corazon = pygame.image.load("corazon.png")
        self.corazon = pygame.transform.scale(self.corazon, (32, 32))
        self.fuente_puntaje = pygame.font.Font(None, 36)
        self.fuente_cronometro = pygame.font.Font(None, 36)
        self.fuente_game_over = pygame.font.Font(None, 96)
        self.fuente_resultado = pygame.font.Font(None, 48)
        self.fuente_mejora = pygame.font.Font(None, 42)

    @staticmethod
    def formatear_tiempo(segundos):
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        return f"{minutos}:{segundos_restantes:02d}"

    def dibujar_vidas(self, superficie, vidas):
        for indice in range(vidas):
            superficie.blit(self.corazon, (10 + indice * 36, 10))

    def dibujar_puntaje(self, superficie, puntos):
        texto = self.fuente_puntaje.render(
            f"Puntos: {puntos}", True, (255, 255, 255)
        )
        superficie.blit(texto, (self.ancho - 150, 10))

    def dibujar_cronometro(
        self, superficie, estado, tiempo_inicio, tiempo_final
    ):
        if estado == "Jugando":
            segundos = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        else:
            segundos = tiempo_final

        texto = self.fuente_cronometro.render(
            f"Tiempo: {self.formatear_tiempo(segundos)}",
            True,
            (255, 255, 255),
        )
        superficie.blit(texto, texto.get_rect(midtop=(self.ancho // 2, 10)))

    def dibujar_pantalla_fin(self, superficie, puntos, tiempo_final):
        capa = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 180))
        superficie.blit(capa, (0, 0))

        titulo = self.fuente_game_over.render(
            "GAME OVER", True, (255, 70, 70)
        )
        superficie.blit(
            titulo,
            titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 80)),
        )

        resultado = self.fuente_resultado.render(
            f"Puntaje final: {puntos}", True, (255, 255, 255)
        )
        superficie.blit(
            resultado,
            resultado.get_rect(center=(self.ancho // 2, self.alto // 2 + 10)),
        )

        tiempo = self.fuente_resultado.render(
            f"Tiempo sobrevivido: {self.formatear_tiempo(tiempo_final)}",
            True,
            (255, 255, 255),
        )
        superficie.blit(
            tiempo,
            tiempo.get_rect(center=(self.ancho // 2, self.alto // 2 + 70)),
        )

    def dibujar_mensaje_mejora(self, superficie, mensaje):
        texto = self.fuente_mejora.render(
            mensaje, True, (255, 230, 80)
        )
        superficie.blit(
            texto,
            texto.get_rect(center=(self.ancho // 2, 60)),
        )
