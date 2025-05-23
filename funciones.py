import pygame
import sys
from jugador import PacMan, PacmanShowVidas
from fantasmas import Fantasma
from varios import *
from laberintos import Pantallas
from tiles import TileType

def crear_escenario(self):
    """Crear el laberinto y los tiles correspondientes."""
    contador = -1
    for i in range(self.CO.FILAS):
        for ii in range(self.CO.COLUMNAS):
            contador += 1
            valor_tile = Pantallas.get_laberinto(self.nivel)[contador]

            # Usar enumeración para los tipos de tiles
            if valor_tile == TileType.WALL.value:
                tile = LaberintoTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tile)
                self.listas_sprites["laberinto"].add(tile)
            elif valor_tile == TileType.DOT.value:
                dot = Puntitos(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(dot)
                self.listas_sprites["puntitos"].add(dot)
            elif valor_tile == TileType.POWER_DOT.value:
                power_dot = PuntosGordos(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(power_dot)
                self.listas_sprites["puntos_gordos"].add(power_dot)

def instanciar_pacman(self):
    self.pacman = PacMan(self, self.CO.PACMAN_INI_POS[0], self.CO.PACMAN_INI_POS[1])
    self.listas_sprites["all_sprites"].add(self.pacman)
    self.listas_sprites["pacman"].add(self.pacman)

def instanciar_showvidas(self):
    for i in range(self.vidas):
        self.pacman_vidas = PacmanShowVidas(self, self.CO.VIDAS_COOR_X, self.CO.VIDAS_COOR_Y + i)
        self.listas_sprites["vidas"].add(self.pacman_vidas)

def instanciar_fantasmas(self):
    for i in range(self.CO.N_FANTASMAS):
        datos = self.CO.LISTA_ARGS_FANTASMAS[i]
        coorX = datos[0]
        coorY = datos[1]
        instanciar_fantasma(self, coorX, coorY, i, datos[3], False, False)

def instanciar_fantasma(self, coorX, coorY, i, direc, azul, ojos):
    fantasma = Fantasma(self, coorX, coorY, i, direc, azul, ojos)
    self.listas_sprites["fantasmas"].add(fantasma)

def instanciar_fruta(self):
    if len(self.listas_sprites["items"]) != 0 or not self.estado_juego["en_juego"]:
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update["item-fruta"] > self.CO.INTERVALO_FRUTA:
        self.ultimo_update["item-fruta"] = calculo
        print("Instanciada-Fruta")
        newFruta = ItemFrutas(self)
        self.listas_sprites["all_sprites"].add(newFruta)
        self.listas_sprites["items"].add(newFruta)

def check_showbonus_kill(self):
    if len(self.listas_sprites["items"]) != 0 or not self.estado_juego["en_juego"]:
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update["show-bonus-fruta"] > self.CO.DURACION_SHOW_BONUS_FRUTA:
        self.ultimo_update["show-bonus-fruta"] = calculo
        #print("3sg")
        eliminar_elemento_de_lista(self, "textos", "show-bonus-fruta")

def instanciar_textos(self):
    MARGEN = 9

    self.instanciar_texto(self.CO.TXT_PREPARADO, 90, (self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES) // 2,
        300, self.COL.VERDE_FONDO, fondo=self.COL.BG_GRIS_OSCURO, negrita=True, tipo="txt-preparado")
    
    self.instanciar_texto("Puntos", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY, self.COL.AMARILLENTO, negrita=True, centrado=False)
    self.instanciar_texto("Nivel", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 4, self.COL.AMARILLENTO, negrita=True, centrado=False)
    self.instanciar_texto("0", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 2, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-puntos")
    self.instanciar_texto(str(self.nivel), 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 5, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-nivel")

def updates_segun_estado(self):
    """Updates condicionales (presentacion/preparado/en_juego...)"""

    check_temporizador_azules(self)
    checkNivelSuperado(self)
    self.instanciar_fruta_periodicamente()

    if self.estado_juego["menu_presentacion"]:
        self.listas_sprites["textos"].update()
    
    elif self.estado_juego["preparado"]:
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimo_update["preparado"] > self.CO.DURACION_PREPARADO:
            self.ultimo_update["preparado"] = calculo
            self.resetear_estados_juego()
            self.estado_juego["preparado"] = False
            self.estado_juego["en_juego"] = True
            eliminar_elemento_de_lista(self, "textos", "txt-preparado")
    
    else:
        self.listas_sprites["all_sprites"].update()
        self.listas_sprites["fantasmas"].update()
        self.listas_sprites["vidas"].update()
        self.listas_sprites["textos"].update()
    
    #self.checkTransicion_gameOverRejugar()

def check_temporizador_azules(self):
    calculo = pygame.time.get_ticks()
    if self.temporizadorAzules and calculo - self.ultimo_update["azules"] > self.CO.DURACION_AZULES[self.nivel]:
        self.ultimo_update["azules"] = calculo
        print("tiempo-azules-agotado")
        self.temporizadorAzules = False

        for fantasma in self.listas_sprites["fantasmas"]:
            fantasma.kill()
            x, y = int(fantasma.rect.x / self.CO.TX), int(fantasma.rect.y / self.CO.TY)
            self.instanciar_fantasma(x, y, fantasma.id_fantasma, fantasma.direccion, azul=False, ojos=False)

def checkNivelSuperado(self):
    if len(self.listas_sprites["puntitos"]) <= 0:
        print("nivel superado")

def draw_listas_sprites(self):
    """Renderizar las listas-sprites"""
    self.listas_sprites["all_sprites"].draw(self.pantalla)
    self.listas_sprites["fantasmas"].draw(self.pantalla)
    self.listas_sprites["vidas"].draw(self.pantalla)

    # dibujar rectangulo "transparente" escapatoria
    pygame.draw.rect(self.pantalla, self.COL.GRIS_FONDO, 
        (self.CO.COLUMNAS * self.CO.TX, 11 * self.CO.TY, self.CO.TX, self.CO.TY))
    
    self.listas_sprites["textos"].draw(self.pantalla)

def eventos_comenzar_quit_etc(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.program_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.program_running = False
                pygame.quit()
                sys.exit()
            
            if event.key == pygame.K_RETURN and self.estado_juego["menu_presentacion"]:
                pygame.mixer.music.stop()
                self.resetear_estados_juego()
                self.estado_juego["preparado"] = True
                self.estado_juego["en_juego"] = True
                self.ultimo_update["preparado"] = pygame.time.get_ticks()
                self.sonidos.reproducir("inicio_nivel")
                # ************** Comenzar partida (Pulsando ENTER) ***********************
                self.new_game()
            
            if event.key == pygame.K_TAB:
                for clave in self.estado_juego:
                    print(clave, self.estado_juego[clave])

def eliminar_elemento_de_lista(self, lista, elemento):
    for sprite in self.listas_sprites[lista]:
        if isinstance(sprite, Textos) and sprite.tipo == elemento:
            self.listas_sprites["textos"].remove(sprite)
            break

