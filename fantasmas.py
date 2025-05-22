import pygame
import random
from enum import Enum
from laberintos import Pantallas
from tiles import TileType

# ====================================================================================
#   fantasmas.py (modulo logica de los fantasmas/enemigos)
#   class --> Fantasma, Direccion
#
# ------------------------------------------------------------------------------------
class Direccion(Enum):
    RIGHT = "ri"
    LEFT = "le"
    UP = "up"
    DOWN = "do"

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, game, x, y, id_fantasma, dir_defecto, azul=False, ojos=False):
        super().__init__()
        self.game = game
        self.id_fantasma = id_fantasma
        self.direccion = dir_defecto
        self.azul = azul
        self.ojos = ojos
        self.velocidad = 2

        # Diccionario de direcciones
        self.dic_direccion = self.generar_direcciones()

        # Puntos clave
        self.ptos_clave = self.procesar_puntos_clave([
            (75, 425), (225, 225), (225, 425), (225, 675), (225, 575),
            (325, 575), (225, 75), (425, 425), (325, 225),
            (875, 425), (725, 225), (725, 425), (725, 675), (725, 575),
            (625, 575), (725, 75), (525, 425), (625, 225)
        ])

        # Animaciones
        self.lista_imagenes = self.cargar_imagenes()
        self.indice_animacion = 0
        self.image = self.lista_imagenes[0 + self.id_fantasma * 2]
        self.rect = self.image.get_rect()
        self.rect.x = x * self.game.CO.TX
        self.rect.y = y * self.game.CO.TY

        # Radius (reducir el radio, para hacer mas permisiva la colision)...
        # ... y mas jugable... radius= 25 (default) --> reducido a 15
        self.radius = 20

        # Estados
        self.vel_xy = self.dic_direccion[self.direccion][:2]
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 100  # Velocidad de animación
    
    def update(self):
        self.actualizar_animacion()
        self.manejar_colisiones()
        self.verificar_colision_pacman()
    
    def generar_direcciones(self):
        """Generar las direcciones y configuraciones."""

        anim_base = [0, 2, 4, 6] if self.azul or self.ojos else [0, 8, 16, 24]

        return {
            Direccion.RIGHT.value: [1, 0, anim_base[0] + self.id_fantasma * 2, "updole"],
            Direccion.LEFT.value: [-1, 0, anim_base[1] + self.id_fantasma * 2, "updori"],
            Direccion.UP.value: [0, -1, anim_base[2] + self.id_fantasma * 2, "riledo"],
            Direccion.DOWN.value: [0, 1, anim_base[3] + self.id_fantasma * 2, "rileup"]
        }

    def procesar_puntos_clave(self, puntos_crudos):
        """Convertir puntos clave a coordenadas del tablero."""
        return [(int((pcx - 25) // 50), int((pcy - 25) // 50)) for pcx, pcy in puntos_crudos]

    def cargar_imagenes(self):
        """Cargar imágenes según el estado del fantasma."""

        if self.ojos:
            return [self.game.obtenerGrafico(f"fantasma{i + 51}.png", 1)[0] for i in range(8)]
        elif self.azul:
            return [self.game.obtenerGrafico(f"fantasmaAzul{i + 1}.png", 1)[0] for i in range(8)]
        else:
            return [
                self.game.obtener_grafico(f"fantasma{i + 1}.png", 1)[0]
                for i in range(38) if i not in [8, 9, 18, 19, 28, 29]
            ]
    
    def manejar_colisiones(self):
        """Verificar y manejar colisiones del fantasma."""

        if self.rect.x % self.game.CO.TX == 0 and self.rect.y % self.game.CO.TY == 0:
            x, y = self.rect.x // self.game.CO.TX, self.rect.y // self.game.CO.TY

            if (x, y) in self.ptos_clave:
                self.perseguir_pacman()
            
            if not self.colision_laberinto(x, y):
                self.vel_xy = self.dic_direccion[self.direccion][:2]
            else:
                self.elegir_direccion_alternativa()
                return

        self.rect.x += self.vel_xy[0] * self.velocidad
        self.rect.y += self.vel_xy[1] * self.velocidad

    def elegir_direccion_alternativa(self):
        """Elegir otra dirección al encontrar un obstáculo."""

        opciones = self.dic_direccion[self.direccion][3]
        aleatorio = random.randrange(0, 3) * 2
        nueva_direccion = opciones[aleatorio: aleatorio + 2]
        self.direccion = nueva_direccion
        self.vel_xy = self.dic_direccion[self.direccion][:2]
    
    def colision_laberinto(self, x, y):
        """Determinar si hay colisión con el laberinto."""

        """ if self.es_teletransporte(x, y, self.vel_xy[0]):
            return False """
        
        indice = self.game.obtener_indice(x + self.vel_xy[0], y + self.vel_xy[1])
        
        if indice is None:
            return False
        
        return Pantallas.get_laberinto(self.game.nivel)[indice] == TileType.WALL.value
    
    """ def es_teletransporte(self, x, y, vel_x):
        if y == 11:  # Línea especial para teletransporte
            if x + vel_x > self.game.CO.COLUMNAS:
                self.rect.x = -self.game.CO.TX
                return True
            elif x + vel_x < -1:
                self.rect.x = self.game.CO.COLUMNAS * self.game.CO.TX
                return True
        return False """
    
    def perseguir_pacman(self):
        """Actualizar dirección para perseguir a PacMan."""

        if random.randrange(100) > self.game.nivel * 30:
            return
        if random.randrange(10) < 5:  # Decisión horizontal/vertical
            self.direccion = Direccion.UP.value if self.game.pacman.rect.y < self.rect.y else Direccion.DOWN.value
        else:
            self.direccion = Direccion.LEFT.value if self.game.pacman.rect.x < self.rect.x else Direccion.RIGHT.value
        
        self.vel_xy = self.dic_direccion[self.direccion][:2]

    def actualizar_animacion(self):
        """Actualizar el fotograma actual del fantasma."""

        if pygame.time.get_ticks() - self.ultimo_update > self.fotograma_vel:
            self.ultimo_update = pygame.time.get_ticks()
            self.indice_animacion = 1 - self.indice_animacion  # Alterna entre 0 y 1
            base = self.dic_direccion[self.direccion][2]
            self.image = self.lista_imagenes[base + self.indice_animacion]

            if self.azul:
                self.image.set_alpha(100 if self.game.obtenerDuracionAzules() > 0 else 255)

    def verificar_colision_pacman(self):
        """Verificar colisiones con PacMan."""

        if self.ojos or self.game.CO.INVULNERABLE:
            return
        
        colision = pygame.sprite.spritecollide(
            self, self.game.listas_sprites["pacman"], not self.azul, pygame.sprite.collide_circle
        )

        for impacto in colision:
            if self.azul:
                self.manejar_colision_comido()
            else:
                self.manejar_colision_atrapa_pacman(impacto)

    def manejar_colision_comido(self):
        """Manejar cuando PacMan come al fantasma azul."""

        self.game.sonidos.reproducir("eating_ghost")
        self.kill()

        coor_x = self.rect.x // self.game.CO.TX
        coor_y = self.rect.y // self.game.CO.TY
        self.game.sumaPtosComeFantasmas *= 2
        self.game.puntos += self.game.sumaPtosComeFantasmas
        self.game.instanciaPtosComeFantasmas(self.game.sumaPtosComeFantasmas, coor_x, coor_y)
        self.game.instanciar_fantasma(coor_x, coor_y, self.id_fantasma, self.direccion, False, True)

    def manejar_colision_atrapa_pacman(self, impacto):
        """Manejar cuando el fantasma atrapa a PacMan."""
        self.game.sonidos.reproducir("pacman_dies")
        self.game.instanciar_pacman_dies(impacto.rect.x, impacto.rect.y)
