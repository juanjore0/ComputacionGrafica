import pygame
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
