import pygame
class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen=None):
        super().__init__()
        if imagen is not None:
            self.image = imagen
        else:
            self.image = pygame.Surface((48, 48))
            self.image.fill((100, 170, 250))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.en_suelo = False
    def update(self, plataformas):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -15
        self.vel_y += 1
        self.rect.y += self.vel_y
        self.en_suelo = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self.vel_y >= 0:
                self.rect.bottom = plataforma.rect.top
                self.vel_y = 0
                self.en_suelo = True
