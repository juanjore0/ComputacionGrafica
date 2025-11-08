import pygame
import os
from constantes import ANCHO, ALTO, FPS
from nivel import Nivel
from personaje import Personaje
from cargador_sprites import CargadorSprites


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Demo Suelo Dedicado')
        self.clock = pygame.time.Clock()

        # Rutas
        base = os.path.dirname(os.path.abspath(__file__))
        ruta_fondo = os.path.join(base, '..', 'assets', 'images', 'backgrounds', 'Background_0.png')
        ruta_suelo = os.path.join(base, '..', 'assets', 'images', 'tiles', 'tiles.png')
        ruta_personaje = os.path.join(base, '..', 'assets', 'images', 'player', 'player.png')
        
        # Fondo
        try:
            self.fondo = pygame.image.load(ruta_fondo).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except Exception:
            self.fondo = pygame.Surface((ANCHO, ALTO))
            self.fondo.fill((40, 70, 120))
        
        # Cargar suelo
        try:
            elementos = CargadorSprites.cargar_elementos_solidos(ruta_suelo, escala=(95, 47))
            
            # Usamos el suelo con césped (sprite0) como tile principal
            if elementos and 'sprite0' in elementos:
                self.tile_suelo = elementos['sprite0'][0]  # Tomar el primer frame
                print("✓ Suelo cargado correctamente (sprite0)")
            else:
                raise Exception("No se encontró 'sprite0' en los elementos sólidos")

        except Exception as e:
            print(f"Error cargando suelo: {e}")
            self.tile_suelo = pygame.Surface((95, 47))
            self.tile_suelo.fill((150, 110, 40))
        
        # Cargar spritesheet del personaje con todas las animaciones
        try:
            self.animaciones = CargadorSprites.cargar_animaciones_jugador(
                ruta_personaje, 
                escala=(112, 112)  # Doble del tamaño original (56x56 -> 112x112)
            )
            
            if self.animaciones:
                self.pj_imagen = self.animaciones['idle'][0]
                print("✓ Animaciones cargadas correctamente")
                print(f"  Animaciones disponibles: {list(self.animaciones.keys())}")
            else:
                raise Exception("No se pudieron cargar las animaciones")
                
        except Exception as e:
            print(f"Error cargando sprite: {e}")
            self.pj_imagen = pygame.Surface((112, 112))
            self.pj_imagen.fill((0, 255, 0))
            self.animaciones = None
        
        # Mapa simplificado
        self.mapa = [
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,1,0,0,0,1,1,1,0,0,0,0],
        ]
        self.nivel = Nivel(self.mapa, self.tile_suelo)
        
        # Calcular posición inicial sobre una plataforma
        tile_alto = self.tile_suelo.get_height()
        posicion_y_segura = 3 * tile_alto - 70  # Fila 3 del mapa, ajustado para estar encima
        
        self.personaje = Personaje(100, posicion_y_segura, self.pj_imagen, self.animaciones)
        self.todas = pygame.sprite.Group(self.personaje)
        
        # Debug
        print(f"Personaje creado en posición: ({self.personaje.rect.x}, {self.personaje.rect.y})")
        print(f"Tamaño del personaje: {self.personaje.rect.width}x{self.personaje.rect.height}")
        print(f"Imagen del personaje cargada: {self.pj_imagen is not None}")
        print(f"Animaciones cargadas: {self.animaciones is not None}")
        print(f"Altura de tile: {tile_alto}")
        print(f"Número de plataformas: {len(self.nivel.plataformas)}")

    
    def bucle(self):
        corriendo = True
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
            
            self.personaje.update(self.nivel.plataformas)
            
            # Dibujar fondo
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Dibujar nivel
            self.nivel.dibujar(self.pantalla)
            
            # Debug: Dibujar hitboxes
            pygame.draw.rect(self.pantalla, (255, 0, 0), self.personaje.rect, 2)
            pygame.draw.rect(self.pantalla, (0, 255, 0), self.personaje.hitbox, 2)
            
            # Dibujar jugador
            self.todas.draw(self.pantalla)
            
            # Mostrar posición cada cierto tiempo
            if pygame.time.get_ticks() % 1000 < 16:
                print(f"Pos: ({self.personaje.rect.x}, {self.personaje.rect.y}), Suelo: {self.personaje.en_suelo}")
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
