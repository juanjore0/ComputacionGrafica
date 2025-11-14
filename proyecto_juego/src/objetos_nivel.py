import pygame
import os

class Coleccionable(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='libro'):
        super().__init__()
        
        self.tipo = tipo
        
        if self.tipo == 'libro':
            # --- Cargar imagen del libro ---
            try:
                base = os.path.dirname(os.path.abspath(__file__))
                ruta_imagen = os.path.join(base, '..', 'assets', 'images', 'decorations', 'libro.png') 
                self.image = pygame.image.load(ruta_imagen).convert_alpha()
                self.image = pygame.transform.scale(self.image, (40, 40))
            except Exception as e:
                print(f"Error cargando imagen de libro: {e}")
                self.image = pygame.Surface((32, 32))
                self.image.fill((255, 0, 255)) # Color magenta brillante para debug
            
            self.valor = 100 # Puntos que da el libro
        
        self.rect = self.image.get_rect(topleft=(x, y))

#--- Clase para Trampas ---
class Trampa(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='espinas'):
        super().__init__()
        
        self.tipo = tipo
    
        if self.tipo == 'espinas': 
            try:
                base = os.path.dirname(os.path.abspath(__file__))
                ruta_imagen = os.path.join(base, '..', 'assets', 'images', 'decorations', 'fuego.png') 
                self.image = pygame.image.load(ruta_imagen).convert_alpha()
                self.image = pygame.transform.scale(self.image, (95, 47)) 
            except Exception as e:
                print(f"Error cargando imagen de trampa: {e}")
                self.image = pygame.Surface((95, 47))
                self.image.fill((255, 0, 0)) 
            
            self.daño = 1
        
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Clase para el Final del Nivel ---
class PuntoFinal(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.set_alpha(0) # Completamente transparente
        self.rect = self.image.get_rect(topleft=(x, y))