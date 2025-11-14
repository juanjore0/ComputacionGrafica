import pygame
from objetos_nivel import Coleccionable, Trampa, PuntoFinal
class Nivel:
    def __init__(self, mapa, tile_suelo):
        self.mapa = mapa
        # Recortar el tile para eliminar bordes transparentes
        self.tile_suelo = self.recortar_tile(tile_suelo)
        self.plataformas = self.crear_plataformas()


        # Grupo para guardar los sprites de los libros
        self.grupo_coleccionables = pygame.sprite.Group()
        
        # --- Ejemplo: Añadir un libro manualmente ---
        libro1 = Coleccionable(400, 100, 'libro') 
        self.grupo_coleccionables.add(libro1)
        
        libro2 = Coleccionable(600, 50, 'libro')
        self.grupo_coleccionables.add(libro2)

                # --- AÑADIDO: Grupo de Trampas ---
        self.grupo_trampas = pygame.sprite.Group()
        
        # -- Añadir unas espinas manualmente ---
        espinas1 = Trampa(250,100, 'espinas') 
        self.grupo_trampas.add(espinas1)
    
    # --- FUNCIÓN 'recortar_tile' CORREGIDA ---
    def recortar_tile(self, tile):
        """Recorta los bordes transparentes de un tile de forma robusta"""
        
        # 1. Obtener el rectángulo de la imagen original (siempre es (0, 0, ancho, alto))
        tile_rect = tile.get_rect()
        
        # 2. Obtener el rectángulo que contiene los píxeles no transparentes
        rect_recortado = tile.get_bounding_rect()
        
        # 3. Comprobar si el tile está completamente transparente (evitar crash)
        if rect_recortado.width == 0 or rect_recortado.height == 0:
            print("Advertencia: El tile de suelo es completamente transparente.")
            return tile # Devolver el original para evitar un error
            
        # 4. LA CLAVE: Comprobar si el rect recortado es *diferente* al rect original.
        #    Esto detecta no solo cambios de tamaño, sino también de *posición* (offsets).
        if rect_recortado != tile_rect:
            print(f"Tile recortado: {tile_rect.size} -> {rect_recortado.size} (offset: {rect_recortado.topleft})")
            # Devolver solo la sub-superficie que contiene los píxeles
            return tile.subsurface(rect_recortado)
        else:
            print("Tile no necesita recorte")
            return tile
    # --- FIN DE LA FUNCIÓN RECORTAR_TILE ---
        
    def crear_plataformas(self):
        plataformas = []
        # Estas dimensiones ahora son las del tile YA recortado
        tile_ancho = self.tile_suelo.get_width()
        tile_alto = self.tile_suelo.get_height()
        
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                if celda == 1:
                    # La posición se calcula con las nuevas dimensiones
                    x = col_idx * tile_ancho
                    y = fila_idx * tile_alto
                    
                    # Usar el tile recortado para colisiones
                    plataforma = pygame.Rect(x, y, tile_ancho, tile_alto)
                    plataformas.append(plataforma)
        
        print(f"Creadas {len(plataformas)} plataformas")
        print(f"Tamaño tile recortado usado: {tile_ancho}x{tile_alto}")
        return plataformas
    
    def dibujar(self, pantalla):
        # Estas dimensiones son las del tile YA recortado
        tile_ancho = self.tile_suelo.get_width()
        tile_alto = self.tile_suelo.get_height()
        
        for fila_idx, fila in enumerate(self.mapa):
            for col_idx, celda in enumerate(fila):
                if celda == 1:
                    # La posición se calcula con las nuevas dimensiones
                    x = col_idx * tile_ancho
                    y = fila_idx * tile_alto
                    pantalla.blit(self.tile_suelo, (x, y))