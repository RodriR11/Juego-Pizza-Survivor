import pygame


class Repartidor:
    vidas_maximas = 3
    duracion_estrella = 5
    aumento_velocidad_estrella = 0.5

    def __init__(self, x, y, sonido_vida_perdida):
        self.imagen = pygame.image.load("repartidor.png")
        self.imagen = pygame.transform.scale(self.imagen, (64, 100))

        self.x = x
        self.y = y
        self.velocidad = 3.5
        self.cambio_x = 0
        self.cambio_y = 0
        self.vidas = self.vidas_maximas
        self.tiempo_invulnerable = 0
        self.tiempo_estrella = 0
        self.sonido_vida_perdida = sonido_vida_perdida

    @property
    def rectangulo(self):
        return self.imagen.get_rect(topleft=(self.x, self.y))

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                self.cambio_x = -1
            if evento.key == pygame.K_RIGHT:
                self.cambio_x = 1
            if evento.key == pygame.K_UP:
                self.cambio_y = -1
            if evento.key == pygame.K_DOWN:
                self.cambio_y = 1

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.cambio_x = 0
            if evento.key in (pygame.K_UP, pygame.K_DOWN):
                self.cambio_y = 0

    def actualizar(self, delta_time, ancho_pantalla, alto_pantalla):
        if self.tiempo_invulnerable > 0:
            self.tiempo_invulnerable = max(
                0, self.tiempo_invulnerable - delta_time
            )
        if self.tiempo_estrella > 0:
            self.tiempo_estrella = max(0, self.tiempo_estrella - delta_time)

        velocidad_actual = self.velocidad
        if self.estrella_activa:
            velocidad_actual += self.aumento_velocidad_estrella

        self.x += self.cambio_x * velocidad_actual
        self.y += self.cambio_y * velocidad_actual
        self.x = max(0, min(self.x, ancho_pantalla - self.rectangulo.width))
        self.y = max(0, min(self.y, alto_pantalla - self.rectangulo.height))

    @property
    def estrella_activa(self):
        return self.tiempo_estrella > 0

    def activar_estrella(self):
        self.tiempo_estrella = self.duracion_estrella

    def recibir_golpe(self):
        if self.tiempo_invulnerable > 0:
            return False

        self.vidas -= 1
        self.tiempo_invulnerable = 1
        self.sonido_vida_perdida.play()
        return True

    def recuperar_vida(self):
        if self.vidas >= self.vidas_maximas:
            return False

        self.vidas += 1
        return True

    def dibujar(self, superficie):
        # Titilar mientras está protegido de otro golpe.
        visible = (
            self.tiempo_invulnerable <= 0
            or pygame.time.get_ticks() // 100 % 2 == 0
        )
        if visible:
            imagen = self.imagen
            if self.estrella_activa:
                colores = (
                    (255, 80, 80, 255),
                    (255, 220, 60, 255),
                    (80, 255, 120, 255),
                    (80, 180, 255, 255),
                    (220, 80, 255, 255),
                )
                indice_color = pygame.time.get_ticks() // 100 % len(colores)
                imagen = self.imagen.copy()
                imagen.fill(
                    colores[indice_color],
                    special_flags=pygame.BLEND_RGBA_MULT,
                )
            superficie.blit(imagen, (self.x, self.y))
