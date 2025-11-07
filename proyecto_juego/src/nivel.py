import pygame
from plataforma import Plataforma
class Nivel:
    def __init__(self, mapa, tile_imagen):
        self.plataformas = pygame.sprite.Group()
        # Usa el tamaño del tile directamente
        tile_w = tile_imagen.get_width()
        tile_h = tile_imagen.get_height()
        for y, fila in enumerate(mapa):
            for x, valor in enumerate(fila):
                if valor == 1:
                    pl = Plataforma(x * tile_w, y * tile_h, tile_imagen)
                    self.plataformas.add(pl)
    def dibujar(self, pantalla):
        self.plataformas.draw(pantalla)
