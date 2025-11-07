import pygame
import os
from constantes import ANCHO, ALTO, FPS
from nivel import Nivel
from personaje import Personaje

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Demo Suelo Dedicado')
        self.clock = pygame.time.Clock()
        base = os.path.dirname(os.path.abspath(__file__))
        ruta_fondo = os.path.join(base, '..', 'assets', 'images', 'backgrounds', 'Background_0.png')
        ruta_suelo = os.path.join(base, '..', 'assets', 'images', 'tiles', 'suelo.png')
        ruta_personaje = os.path.join(base, '..', 'assets', 'images', 'player', 'char_blue1.png')
        # Fondo
        try:
            self.fondo = pygame.image.load(ruta_fondo).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except Exception:
            self.fondo = pygame.Surface((ANCHO, ALTO))
            self.fondo.fill((40,70,120))
        # Cargar suelo
        try:
            self.tile_suelo = pygame.image.load(ruta_suelo).convert_alpha()
        except Exception:
            self.tile_suelo = pygame.Surface((95, 47))  # Ajusta el tamaño si varía
            self.tile_suelo.fill((150, 110, 40))
        # Cargar personaje
        try:
            self.pj_imagen = pygame.image.load(ruta_personaje).convert_alpha()
            self.pj_imagen = pygame.transform.scale(self.pj_imagen, (48, 48))
        except Exception:
            self.pj_imagen = None
        # Mapa simplificado
        self.mapa = [
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,1,1,1,0,0,0,0],
        ]
        self.nivel = Nivel(self.mapa, self.tile_suelo)
        self.personaje = Personaje(100, 100, self.pj_imagen)
        self.todas = pygame.sprite.Group(self.personaje)
    def bucle(self):
        corriendo = True
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
            self.personaje.update(self.nivel.plataformas)
            self.pantalla.blit(self.fondo, (0, 0))
            self.nivel.dibujar(self.pantalla)
            self.todas.draw(self.pantalla)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
