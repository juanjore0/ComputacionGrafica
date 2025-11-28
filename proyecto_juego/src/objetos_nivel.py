import pygame

class Coleccionable(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, tipo='libro'):
        """
        Args:
            x, y: Posición del coleccionable
            imagen: Surface de pygame con la imagen ya cargada
            tipo: Tipo de coleccionable (para futuras expansiones)
        """
        super().__init__()
        
        self.tipo = tipo
        self.image = imagen
        
        # Configurar valores según el tipo
        if self.tipo == 'libro':
            self.valor = 100
        else:
            self.valor = 50  # Valor por defecto
        
        self.rect = self.image.get_rect(topleft=(x, y))


class Trampa(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, tipo='espinas'):
        """
        Args:
            x, y: Posición de la trampa
            imagen: Surface de pygame con la imagen ya cargada
            tipo: Tipo de trampa (para futuras expansiones)
        """
        super().__init__()
        self.tipo = tipo
        self.image = imagen
        
        # Configurar daño según el tipo
        if self.tipo == 'espinas':
            self.daño = 1
        else:
            self.daño = 1
        
        # Rect para dibujar (posición visual completa)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # ✅ Crear un hitbox más pequeño para colisiones
        if self.tipo == 'espinas':
            # Ajusta estos valores para cambiar el tamaño del hitbox
            ancho_hitbox = int(self.image.get_width() * 0.8)  # 80% del ancho
            alto_hitbox = int(self.image.get_height() * 0.5)  # 50% del alto
            
            # Centrar el hitbox en la parte inferior de la imagen
            offset_x = (self.image.get_width() - ancho_hitbox) // 2
            offset_y = self.image.get_height() - alto_hitbox
            
            self.hitbox = pygame.Rect(
                x + offset_x,
                y + offset_y,
                ancho_hitbox,
                alto_hitbox
            )
        else:
            self.hitbox = self.rect.copy()
    
    def dibujar_hitbox(self, pantalla, color=(255, 0, 0)):
        """Dibuja el hitbox para debug"""
        pygame.draw.rect(pantalla, color, self.hitbox, 2)  # Borde de 2 píxeles
        # También dibujar un rectángulo semi-transparente
        superficie = pygame.Surface((self.hitbox.width, self.hitbox.height))
        superficie.set_alpha(100)  # Semi-transparente
        superficie.fill(color)
        pantalla.blit(superficie, (self.hitbox.x, self.hitbox.y))


class PuntoFinal(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        """
        Zona invisible que marca el final del nivel
        """
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.set_alpha(0)  # Completamente transparente
        self.rect = self.image.get_rect(topleft=(x, y))