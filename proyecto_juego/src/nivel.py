import pygame
from objetos_nivel import Coleccionable, Trampa, PuntoFinal

class Nivel:
    def __init__(self, mapa, tile_suelo, libros_cfg=None, trampas_cfg=None, punto_final_cfg=None):
        """
        Inicializa un nivel del juego.
        
        Args:
            mapa: Matriz 2D con la estructura del nivel (0=vacío, 1=plataforma)
            tile_suelo: Surface del tile de suelo
            libros_cfg: Lista de tuplas (x, y, tipo) con posiciones de libros
            trampas_cfg: Lista de tuplas (x, y, tipo) con posiciones de trampas
            punto_final_cfg: Tupla (x, y, ancho, alto) con la posición del punto final
        """
        self.mapa = mapa
        self.tile_suelo = self.recortar_tile(tile_suelo)
        self.plataformas = []
        self.crear_plataformas()
        
        # Grupos de sprites
        self.grupo_coleccionables = pygame.sprite.Group()
        self.grupo_trampas = pygame.sprite.Group()
        self.punto_final = None
        
        # Crear libros desde config
        if libros_cfg:
            for x, y, tipo in libros_cfg:
                libro = Coleccionable(x, y, tipo)
                self.grupo_coleccionables.add(libro)
            print(f"✓ {len(libros_cfg)} libros añadidos al nivel")
        
        # Crear trampas desde config
        if trampas_cfg:
            for x, y, tipo in trampas_cfg:
                trampa = Trampa(x, y, tipo)
                self.grupo_trampas.add(trampa)
            print(f"✓ {len(trampas_cfg)} trampas añadidas al nivel")
        
        # Crear punto final desde config
        if punto_final_cfg:
            x, y, ancho, alto = punto_final_cfg
            self.punto_final = PuntoFinal(x, y, ancho, alto)
            print(f"✓ Punto final creado en ({x}, {y})")
    
    def recortar_tile(self, tile):
        """Recorta los bordes transparentes de un tile de forma robusta"""
        
        # 1. Obtener el rectángulo de la imagen original
        tile_rect = tile.get_rect()
        
        # 2. Obtener el rectángulo que contiene los píxeles no transparentes
        rect_recortado = tile.get_bounding_rect()
        
        # 3. Comprobar si el tile está completamente transparente
        if rect_recortado.width == 0 or rect_recortado.height == 0:
            print("⚠ Advertencia: El tile de suelo es completamente transparente.")
            return tile
        
        # 4. Comprobar si hay diferencias para recortar
        if rect_recortado != tile_rect:
            print(f"✂ Tile recortado: {tile_rect.size} -> {rect_recortado.size} (offset: {rect_recortado.topleft})")
            return tile.subsurface(rect_recortado)
        else:
            return tile
    
    def crear_plataformas(self):
        """Crea las plataformas colisionables basándose en el mapa"""
        self.plataformas = []
        tile_ancho = self.tile_suelo.get_width()
        tile_alto = self.tile_suelo.get_height()
        
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                if celda == 1:
                    x = col_idx * tile_ancho
                    y = fila_idx * tile_alto
                    plataforma = pygame.Rect(x, y, tile_ancho, tile_alto)
                    self.plataformas.append(plataforma)
        
        print(f"✓ {len(self.plataformas)} plataformas creadas")
        print(f"  Tamaño tile: {tile_ancho}x{tile_alto}")
    
    def dibujar(self, pantalla):
        """Dibuja el nivel en la pantalla"""
        tile_ancho = self.tile_suelo.get_width()
        tile_alto = self.tile_suelo.get_height()
        
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                if celda == 1:
                    x = col_idx * tile_ancho
                    y = fila_idx * tile_alto
                    pantalla.blit(self.tile_suelo, (x, y))