import pygame
import os

class Coleccionable(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='libro'):
        super().__init__()
        
        self.tipo = tipo
        
        if self.tipo == 'libro':
            # --- Cargar imagen del libro ---
            # (¡Asegúrate que esta ruta sea correcta!)
            # Usa os.path.join para construir la ruta de forma segura
            try:
                base = os.path.dirname(os.path.abspath(__file__))
                ruta_imagen = os.path.join(base, '..', 'assets', 'images', 'decorations', 'libro.png') # ¡Inventé esta ruta! Ajústala.
                self.image = pygame.image.load(ruta_imagen).convert_alpha()
                # Escalar si es necesario
                self.image = pygame.transform.scale(self.image, (40, 40))
            except Exception as e:
                print(f"Error cargando imagen de libro: {e}")
                self.image = pygame.Surface((32, 32))
                self.image.fill((255, 0, 255)) # Color magenta brillante para debug
            
            self.valor = 100 # Puntos que da el libro
        
        self.rect = self.image.get_rect(topleft=(x, y))

#--- Clase para Trampas ---
class Trampa(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo_daño):
        super().__init__()
        
        if tipo_daño == 'espinas':
            # Cargar imagen de espinas (¡ajusta la ruta!)
            self.image = pygame.image.load('assets/images/decorations/fuego.png').convert_alpha()
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.daño = 1 # Vidas que quita

# --- Clase para el Final del Nivel ---
class PuntoFinal(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.set_alpha(0) # Completamente transparente
        self.rect = self.image.get_rect(topleft=(x, y))