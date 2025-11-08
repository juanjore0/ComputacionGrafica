import pygame

class CargadorSprites:
    """Clase auxiliar para cargar sprites desde un spritesheet"""
    
    @staticmethod
    def cargar_frames(spritesheet, coordenadas, frame_size=(56, 56), escala=None):
        """
        Carga múltiples frames desde un spritesheet.
        
        Args:
            spritesheet: La imagen del spritesheet cargada
            coordenadas: Lista de tuplas (x, y) con las posiciones de cada frame
            frame_size: Tupla (ancho, alto) del tamaño de cada frame
            escala: Tupla (ancho, alto) opcional para redimensionar
        
        Returns:
            Lista de surfaces con los frames extraídos
        """
        frames = []
        ancho, alto = frame_size
        
        for x, y in coordenadas:
            # Extraer el frame
            frame = spritesheet.subsurface(pygame.Rect(x, y, ancho, alto))
            
            # Escalar si se especificó
            if escala:
                frame = pygame.transform.scale(frame, escala)
            
            frames.append(frame)
        
        return frames
    
    @staticmethod
    def cargar_elementos_solidos(ruta_spritesheet, escala=None):
        """
        Carga los elementos sólidos del mapa (suelo, arbustos, árboles, etc.)
        desde el spritesheet principal.
        """
        try:
            spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
        except Exception as e:
            print(f"Error cargando spritesheet: {e}")
            return None
        
        # Definir las coordenadas y tamaños de cada elemento
        elementos_info = {
            'sprite0': {'rect': (180, 215, 112, 66)},       # suelo cesped
            'sprite1': {'rect': (1, 1, 78, 70)},          # suelo con césped
            'sprite2': {'rect': (86, 2, 64, 36)},         # subida suelo V inversa            'sprite4': {'rect': (176, 51, 124, 43)},      # arbusto amarillo claro
            'sprite5': {'rect': (88, 60, 74, 226)},       # árbol con plataforma
            'sprite6': {'rect': (1, 74, 78, 69)},         # suelo sin césped
            'sprite7': {'rect': (176, 99, 124, 43)},      # arbusto verde
            'sprite8': {'rect': (176, 147, 124, 43)},     # arbusto verde oscuro
            'sprite9': {'rect': (2, 161, 75, 16)},        # plataforma madera
            'sprite10': {'rect': (1, 195, 76, 101)},      # árbol decorativo
            'sprite11': {'rect': (176, 195, 124, 43)},    # arbusto verde muy oscuro
        }

        elementos_cargados = {}
        for nombre, info in elementos_info.items():
            x, y, ancho, alto = info['rect']
            
            # Extraer el sprite del spritesheet
            sprite = spritesheet.subsurface(pygame.Rect(x, y, ancho, alto))
            
            # Escalar si se especificó
            if escala:
                sprite = pygame.transform.scale(sprite, escala)
            
            # Guardar en una lista (para mantener consistencia con la interfaz)
            elementos_cargados[nombre] = [sprite]
            
            print(f"✓ Cargado {nombre}: {ancho}x{alto} -> {sprite.get_width()}x{sprite.get_height()}")
        
        return elementos_cargados

    @staticmethod
    def cargar_animaciones_jugador(ruta_spritesheet, escala=(56, 56)):
        """
        Carga todas las animaciones del jugador desde el spritesheet.
        Basado en las coordenadas proporcionadas.
        """
        try:
            spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
        except Exception as e:
            print(f"Error cargando spritesheet: {e}")
            return None
        
        # Define las coordenadas de cada animación según el archivo
        animaciones = {
            # 1. Personaje quieto (idle)
            'idle': [
                (0, 0),
            ],
            
            # 2. Personaje atacando
            'attack': [
                (0, 56), (56, 56), (112, 56), (168, 56), (224, 56), (280, 56), (336, 56), (392, 56),
            ],
            
            # 3. Personaje corriendo
            'run': [
                (0, 112), (56, 112), (112, 112), (168, 112), (224, 112), (280, 112), (336, 112), (392, 112),
            ],
            
            # 4. Personaje saltando (inicio del salto)
            'jump_up': [
                (0, 168), (56, 168), (112, 168), (168, 168), (224, 168), (280, 168), (336, 168), (392, 168),
            ],
            
            # 5. Personaje cayendo
            'jump_down': [
                (0, 224), (56, 224), (112, 224), (168, 224), (224, 224), (280, 224), (336, 224), (392, 224),
            ],
            
            # 6. Personaje recibiendo daño
            'hurt': [
                (0, 280), (56, 280), (112, 280), (168, 280),
            ],
            
            # 7 y 8. Personaje muriendo
            'death': [
                (0, 336), (56, 336), (112, 336), (168, 336), (224, 336), (280, 336), (336, 336), (392, 336),
                (0, 392), (56, 392), (112, 392), (168, 392),
            ],
            
            # 9. Agachándose
            'crouch': [
                (0, 504), (56, 504), (112, 504),
            ],
            
            # 10. Usando escudo
            'shield': [
                (0, 560), (56, 560), (112, 560),
            ],
        }
        
        # Cargar todos los frames
        animaciones_cargadas = {}
        for nombre, coords in animaciones.items():
            animaciones_cargadas[nombre] = CargadorSprites.cargar_frames(
                spritesheet, 
                coords, 
                frame_size=(56, 56),
                escala=escala
            )
        
        return animaciones_cargadas