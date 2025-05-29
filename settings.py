import pygame

# ====================================================================================
#	settings.py (modulo de configuraciones)
# 
# ------------------------------------------------------------------------------------
class Colores:
    AMARILLO = (220, 190, 0)
    AMARILLENTO = (250, 245, 130)
    NARANJA = (250, 142, 12)
    NARANJA_ROJIZO = (255, 100, 12)
    NARANJA_ROJIZO_2 = (255, 45, 12)
    BLANCO = (240, 240, 240)
    GRIS_FONDO = (59, 59, 59)
    BG_GRIS_OSCURO = (49, 49, 50)
    ROJO = (230, 30, 20)
    VERDE_FONDO = (20, 240, 30)
    AZUL_C = (144, 205, 205)

class Constantes:
    TX, TY = 50, 50 # Tamano de los Tiles
    FILAS, COLUMNAS = 15, 19 # Filas x Columnas
    PACMAN_INI_POS = (9, 4)
    VIDAS_COOR_X = COLUMNAS # CoorX showvidas
    VIDAS_COOR_Y = 7 # CoorY Inicial showvidas
    INVULNERABLE = False
    N_FANTASMAS = 4
    # Duracion de los 'fantasmas-azules' en el nivel 1
    DURACION_AZULES = [8000, 8000, 7000, 6000, 5500, 5000, 4700, 4500, 4250, 4000, 3750, 3500, 3000, 2750, 2500]
    DURACION_PREPARADO = 4200
    INTERVALO_FRUTA = 12000
    DURACION_SHOW_BONUS_FRUTA = 2400
    DELAY_NEXT_LEVEL = 7200
    TXT_TITULO = " Pac Clon "
    TXT_PREPARADO = " Preparado! "
    ZONA_SCORES = 200
    RESOLUCION = (TX * COLUMNAS + ZONA_SCORES, TY * FILAS)
    FPS = 100

    LISTA_ARGS_FANTASMAS = [
        (5, 8, 0, 'le'), (8, 8, 1, 'le'),
        (10, 8, 2, 'ri'), (13, 8, 3, 'ri')
    ]

class Sonidos:
    def __init__(self):
        pygame.mixer.init()
        self.sonidos = self.cargar_sonidos()

    def cargar_sonidos(self):
        """Cargar todos los sonidos en un diccionario."""
        return {
            "wakawaka": self.cargar_sonido("sonido/pacmanwakawaka.ogg", 0.9),
            "sirena": self.cargar_sonido("sonido/pacmansirena.ogg", 0.2),
            "eating_cherry": self.cargar_sonido("sonido/pacmaneatingcherry.ogg"),
            "pacman_dies": self.cargar_sonido("sonido/pacmandies.ogg"),
            "gameover_retro": self.cargar_sonido("sonido/gameoveretro.ogg"),
            "fantasmas_azules": self.cargar_sonido("sonido/pacmanazules.ogg"),
            "eating_ghost": self.cargar_sonido("sonido/pacmaneatinghost.ogg"),
            "inicio_nivel": self.cargar_sonido("sonido/pacmaninicionivel.ogg"),
            "intermision": self.cargar_sonido("sonido/pacmanintermision.ogg")
        }

    def cargar_sonido(self, ruta, volumen=1.0):
        """Carga un sonido específico con el volumen indicado."""
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(volumen)
        return sonido

    def reproducir(self, nombre, duracion=None):
        """Reproduce un sonido si está en el diccionario."""
        if nombre in self.sonidos and nombre == "fantasmas_azules":
            self.sonidos[nombre].play(loops=-1)
        
        elif nombre in self.sonidos:
            if duracion == None:
                self.sonidos[nombre].play()
            else:
                self.sonidos[nombre].play(maxtime=duracion)

