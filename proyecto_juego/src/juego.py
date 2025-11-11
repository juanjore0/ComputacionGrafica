import pygame
import os
from constantes import ANCHO, ALTO, FPS
from nivel import Nivel
from personaje import Personaje
from cargador_sprites import CargadorSprites
from menu import Menu


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Can You Go?')
        self.clock = pygame.time.Clock()
        self.estado = 'MENU'  # Estados: MENU, JUGANDO, PAUSA, GAME_OVER

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
            
            if elementos and 'sprite0' in elementos:
                self.tile_suelo = elementos['sprite0'][0]
                print("✓ Suelo cargado correctamente (sprite0)")
            else:
                raise Exception("No se encontró 'sprite0' en los elementos sólidos")

        except Exception as e:
            print(f"Error cargando suelo: {e}")
            self.tile_suelo = pygame.Surface((95, 47))
            self.tile_suelo.fill((150, 110, 40))
        
        # Cargar spritesheet del personaje
        try:
            self.animaciones = CargadorSprites.cargar_animaciones_jugador(
                ruta_personaje, 
                escala=(112, 112)
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
        
        # Inicializar nivel y personaje
        self.inicializar_nivel()
        
        # Crear menú
        self.menu = Menu(self.pantalla)

    def inicializar_nivel(self):
        """Inicializa o reinicia el nivel del juego"""
        # Mapa simplificado
        self.mapa = [
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,1,0,0,0,1,1,1,0,0,0,0],
        ]
        self.nivel = Nivel(self.mapa, self.tile_suelo)
        
        # Calcular posición inicial
        tile_alto = self.tile_suelo.get_height()
        posicion_y_segura = 3 * tile_alto - 70
        
        self.personaje = Personaje(100, posicion_y_segura, self.pj_imagen, self.animaciones)
        self.todas = pygame.sprite.Group(self.personaje)
        
        print(f"Nivel inicializado - Personaje en: ({self.personaje.rect.x}, {self.personaje.rect.y})")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        resultado = self.menu.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'JUGANDO'
            self.inicializar_nivel()  # Reiniciar nivel al empezar
            return True
        elif resultado == 'salir':
            return False
        
        return True
    
    def bucle_juego(self):
        """Bucle principal del juego"""
        corriendo = True
        
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                
                # Pausa con ESC
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.estado = 'MENU'
                        self.menu.activo = True
                        resultado = self.mostrar_menu()
                        if not resultado:
                            corriendo = False
            
            # Actualizar
            self.personaje.update(self.nivel.plataformas)
            
            # Dibujar fondo
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Dibujar nivel
            self.nivel.dibujar(self.pantalla)
            
            # Debug: Dibujar hitboxes (comentar para versión final)
            # pygame.draw.rect(self.pantalla, (255, 0, 0), self.personaje.rect, 2)
            # pygame.draw.rect(self.pantalla, (0, 255, 0), self.personaje.hitbox, 2)
            
            # Dibujar jugador
            self.todas.draw(self.pantalla)
            
            # Mostrar FPS (opcional)
            fuente = pygame.font.Font(None, 30)
            fps_texto = fuente.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.pantalla.blit(fps_texto, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return False
    
    def ejecutar(self):
        """Método principal que controla el flujo del juego"""
        corriendo = True
        
        while corriendo:
            if self.estado == 'MENU':
                corriendo = self.mostrar_menu()
            
            elif self.estado == 'JUGANDO':
                corriendo = self.bucle_juego()
        
        pygame.quit()