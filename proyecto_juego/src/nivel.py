import pygame
from objetos_nivel import Coleccionable, Trampa, PuntoFinal


class Nivel:
    """
    Sistema de códigos para el mapa:
    0 = Vacío (aire)
    1 = Plataforma césped (sprite0)
    2 = Libro (coleccionable)
    3 = Espinas (trampa)
    4 = Punto final
    5 = Plataforma madera (sprite9)
    6 = Suelo sin césped (sprite6)
    7 = Arbusto decorativo (sprite4) - NO colisiona
    """
    
    def __init__(self, mapa, tiles_dict, objetos_dict):
        self.mapa = mapa
        self.tiles_dict = tiles_dict
        self.objetos_dict = objetos_dict
        
        # Recortar todos los tiles
        self.tiles_recortados = {}
        for nombre, sprites in tiles_dict.items():
            if sprites:
                self.tiles_recortados[nombre] = self.recortar_tile(sprites[0])
        
        # Mapeo de códigos numéricos a nombres de sprites
        self.mapa_tiles = {
            1: 'sprite0',   # Suelo con césped
            5: 'sprite9',   # Plataforma madera
            6: 'sprite6',   # Suelo sin césped
            7: 'sprite4',   # Arbusto (decorativo, no colisiona)
            8: 'sprite5',   # Árbol con plataforma
            9: 'sprite1',   # Suelo con césped alternativo
            10: 'sprite7',  # Arbusto verde
            11: 'sprite10', # Árbol decorativo
        }
        
        # Definir qué tiles son sólidos (colisionan)
        self.tiles_solidos = {1, 5, 6, 8, 9}
        
        # Inicializar grupos vacíos
        self.plataformas = []
        self.grupo_coleccionables = pygame.sprite.Group()
        self.grupo_trampas = pygame.sprite.Group()
        self.grupo_punto_final = pygame.sprite.Group()
        
        # Procesar el mapa y crear todos los objetos
        self.procesar_mapa()
    
    def recortar_tile(self, tile):
        """Recorta los bordes transparentes de un tile de forma robusta"""
        tile_rect = tile.get_rect()
        rect_recortado = tile.get_bounding_rect()
        
        if rect_recortado.width == 0 or rect_recortado.height == 0:
            return tile
            
        if rect_recortado != tile_rect:
            return tile.subsurface(rect_recortado)
        else:
            return tile
    
    def obtener_tile(self, codigo):
        """Obtiene el sprite correspondiente a un código numérico"""
        nombre_sprite = self.mapa_tiles.get(codigo)
        if nombre_sprite and nombre_sprite in self.tiles_recortados:
            return self.tiles_recortados[nombre_sprite]
        return None
    
    def es_solido(self, codigo):
        """Verifica si un código representa un tile sólido"""
        return codigo in self.tiles_solidos
    
    def procesar_mapa(self):
        """Procesa el mapa y crea objetos según los códigos numéricos"""
        tile_principal = self.tiles_recortados.get('sprite0')
        if not tile_principal:
            print("ERROR: No se encontró el tile principal (sprite0)")
            return
        
        tile_ancho = tile_principal.get_width()
        tile_alto = tile_principal.get_height()
        
        plataformas = []
        
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                x = col_idx * tile_ancho
                y = fila_idx * tile_alto
                
                if self.es_solido(celda):
                    tile = self.obtener_tile(celda)
                    if tile:
                        if celda == 5:  # sprite9 - plataforma de madera
                            # Reducir la altura de colisión (ajusta este valor)
                            altura_plataforma = 12  # Muy delgada para que el personaje pase debajo
                            # Posicionar la colisión en la parte superior de la plataforma
                            
                            plataforma = pygame.Rect(
                                x, 
                                y, 
                                tile.get_width(), 
                                altura_plataforma
                            )
                        else:
                            # Plataformas normales usan el tamaño completo del tile
                            plataforma = pygame.Rect(x, y, tile.get_width(), tile.get_height())
                        
                        plataformas.append((plataforma, celda))
                
                elif celda == 2:  # Libro
                    if 'libro' in self.objetos_dict:
                        libro = Coleccionable(x, y, self.objetos_dict['libro'], 'libro')
                        self.grupo_coleccionables.add(libro)
                
                elif celda == 3:  # Espinas
                    if 'espinas' in self.objetos_dict:
                        # Ajustar la posición Y para que queden pegadas al suelo
                        y_ajustada = y + tile_alto - self.objetos_dict['espinas'].get_height()
                        espinas = Trampa(x, y_ajustada, self.objetos_dict['espinas'], 'espinas')
                        self.grupo_trampas.add(espinas)
                
                elif celda == 4:  # Punto final
                    punto_final = PuntoFinal(x, y, tile_ancho, tile_alto)
                    self.grupo_punto_final.add(punto_final)

        self.plataformas = [p[0] for p in plataformas]
        self.plataformas_con_tipo = plataformas
        
        print(f"╔══════════════════════════════════╗")
        print(f"║      NIVEL CREADO                ║")
        print(f"╠══════════════════════════════════╣")
        print(f"║ Plataformas:     {len(self.plataformas):4d}          ║")
        print(f"║ Coleccionables:  {len(self.grupo_coleccionables):4d}          ║")
        print(f"║ Trampas:         {len(self.grupo_trampas):4d}          ║")
        print(f"║ Puntos finales:  {len(self.grupo_punto_final):4d}          ║")
        print(f"╚══════════════════════════════════╝")
    
    def dibujar(self, pantalla, debug=False):
        """Dibuja todos los tiles del nivel según el mapa"""
        tile_principal = self.tiles_recortados.get('sprite0')
        if not tile_principal:
            return
        
        tile_ancho = tile_principal.get_width()
        tile_alto = tile_principal.get_height()
        
        # Dibujar todos los tiles visuales
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                if celda == 0:
                    continue
                
                x = col_idx * tile_ancho
                y = fila_idx * tile_alto
                
                tile = self.obtener_tile(celda)
                if tile:
                    pantalla.blit(tile, (x, y))
        
        # ✅ Modo DEBUG - Dibujar hitboxes
        if debug:
            # Dibujar hitboxes de plataformas
            for plataforma, tipo in self.plataformas_con_tipo:
                if tipo == 5:  # Plataformas de madera en AZUL
                    pygame.draw.rect(pantalla, (0, 150, 255), plataforma, 2)
                    # Rellenar semi-transparente para ver mejor
                    superficie = pygame.Surface((plataforma.width, plataforma.height))
                    superficie.set_alpha(80)
                    superficie.fill((0, 150, 255))
                    pantalla.blit(superficie, (plataforma.x, plataforma.y))
                else:  # Otras plataformas en BLANCO
                    pygame.draw.rect(pantalla, (255, 255, 255), plataforma, 1)
            
            # Dibujar hitboxes de trampas (ROJO)
            for trampa in self.grupo_trampas:
                if hasattr(trampa, 'dibujar_hitbox'):
                    trampa.dibujar_hitbox(pantalla, (255, 0, 0))
            
            # Dibujar hitboxes de coleccionables (VERDE)
            for coleccionable in self.grupo_coleccionables:
                pygame.draw.rect(pantalla, (0, 255, 0), coleccionable.rect, 2)
