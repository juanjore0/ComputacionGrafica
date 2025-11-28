import pygame
import os
from constantes import ANCHO, ALTO, FPS, BLANCO
from cargador_sprites import CargadorSprites
from menu import Menu
from introduccion import Introduccion
from gestor_niveles import GestorNiveles


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Can You Go?')
        self.clock = pygame.time.Clock()
        self.estado = 'MENU'  # Estados: MENU, INTRODUCCION, JUGANDO, NIVEL_COMPLETADO, VICTORIA
        
        # Rutas
        base = os.path.dirname(os.path.abspath(__file__))
        ruta_fondo = os.path.join(base, '..', 'assets', 'images', 'backgrounds', 'Background.png')
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
            else:
                raise Exception("No se pudieron cargar las animaciones")
        except Exception as e:
            print(f"Error cargando sprite: {e}")
            self.pj_imagen = pygame.Surface((112, 112))
            self.pj_imagen.fill((0, 255, 0))
            self.animaciones = None
        
        # Inicializar gestor de niveles (se crea después)
        self.gestor_niveles = None
        
        # Crear menú e introducción
        self.menu = Menu(self.pantalla)
        self.introduccion = Introduccion(self.pantalla)
        
        # Fuente para textos
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_grande = pygame.font.Font(None, 72)
    
    def inicializar_juego(self):
        """Inicializa el gestor de niveles y empieza desde el nivel 1"""
        self.gestor_niveles = GestorNiveles(
            tile_suelo=self.tile_suelo,
            imagen_pj=self.pj_imagen,
            animaciones_pj=self.animaciones
        )
        print("🎮 Juego inicializado correctamente")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        resultado = self.menu.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'INTRODUCCION'
            return True
        elif resultado == 'salir':
            return False
        
        return True
    
    def mostrar_introduccion(self):
        """Muestra la introducción animada"""
        self.introduccion.activo = True
        self.introduccion.tiempo_transcurrido = 0
        self.introduccion.fade_in = 0
        
        resultado = self.introduccion.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'JUGANDO'
            self.inicializar_juego()
            return True
        elif resultado == 'salir':
            return False
        return True
    
    def mostrar_pantalla_nivel_completado(self):
        """Muestra una pantalla de transición entre niveles"""
        esperando = True
        tiempo_inicio = pygame.time.get_ticks()
        tiempo_minimo = 2000  # 2 segundos mínimo
        
        while esperando:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'salir'
                
                # Permitir saltar después del tiempo mínimo
                if tiempo_transcurrido > tiempo_minimo:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        esperando = False
            
            # Auto-avanzar después de 5 segundos
            if tiempo_transcurrido > 5000:
                esperando = False
            
            # Dibujar pantalla
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Título
            texto_titulo = self.fuente_grande.render("¡NIVEL COMPLETADO!", True, BLANCO)
            rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            self.pantalla.blit(texto_titulo, rect_titulo)
            
            # Estadísticas
            texto_puntos = self.fuente.render(
                f"Libros recogidos: {self.gestor_niveles.personaje.puntos // 100}", 
                True, BLANCO
            )
            rect_puntos = texto_puntos.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            self.pantalla.blit(texto_puntos, rect_puntos)
            
            texto_vidas = self.fuente.render(
                f"Vidas restantes: {self.gestor_niveles.personaje.vidas}", 
                True, BLANCO
            )
            rect_vidas = texto_vidas.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            self.pantalla.blit(texto_vidas, rect_vidas)
            
            # Instrucción
            if tiempo_transcurrido > tiempo_minimo:
                texto_continuar = self.fuente.render(
                    "Presiona cualquier tecla para continuar...", 
                    True, BLANCO
                )
                texto_continuar.set_alpha(int(abs(pygame.math.Vector2(1, 0).rotate(tiempo_transcurrido * 0.2).x) * 255))
                rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO - 100))
                self.pantalla.blit(texto_continuar, rect_continuar)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return 'continuar'
    
    def mostrar_pantalla_victoria(self):
        """Muestra la pantalla de victoria final"""
        esperando = True
        
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'salir'
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
            
            # Dibujar pantalla
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Título
            texto_titulo = self.fuente_grande.render("¡VICTORIA!", True, (255, 215, 0))
            rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 80))
            self.pantalla.blit(texto_titulo, rect_titulo)
            
            # Mensaje
            texto_mensaje = self.fuente.render(
                "¡Has completado todos los niveles!", 
                True, BLANCO
            )
            rect_mensaje = texto_mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 10))
            self.pantalla.blit(texto_mensaje, rect_mensaje)
            
            # Puntos finales
            texto_puntos = self.fuente.render(
                f"Puntos totales: {self.gestor_niveles.personaje.puntos}", 
                True, BLANCO
            )
            rect_puntos = texto_puntos.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
            self.pantalla.blit(texto_puntos, rect_puntos)
            
            # Instrucción
            texto_continuar = self.fuente.render(
                "Presiona cualquier tecla para volver al menú", 
                True, BLANCO
            )
            rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO - 80))
            self.pantalla.blit(texto_continuar, rect_continuar)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return 'menu'
    
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
            
            # Obtener estado del juego
            estado_juego = self.gestor_niveles.obtener_estado_juego()
            
            # Manejar según el estado
            if estado_juego == 'game_over':
                print("🔄 Volviendo al menú por Game Over")
                self.estado = 'MENU'
                self.menu.activo = True
                corriendo = False
                continue
            
            elif estado_juego == 'nivel_completado':
                # Mostrar pantalla de nivel completado
                resultado = self.mostrar_pantalla_nivel_completado()
                
                if resultado == 'salir':
                    corriendo = False
                    continue
                
                # Intentar cargar el siguiente nivel
                if not self.gestor_niveles.siguiente_nivel():
                    # No hay más niveles, mostrar victoria
                    self.estado = 'VICTORIA'
                    resultado = self.mostrar_pantalla_victoria()
                    
                    if resultado == 'menu':
                        self.estado = 'MENU'
                        self.menu.activo = True
                        corriendo = False
                    else:
                        corriendo = False
                    continue
            
            elif estado_juego == 'jugando':
                # Actualizar
                self.gestor_niveles.actualizar()
                
                # Dibujar fondo
                self.pantalla.blit(self.fondo, (0, 0))
                
                # Dibujar nivel
                self.gestor_niveles.dibujar(self.pantalla)
                
                # HUD
                fuente = pygame.font.Font(None, 30)
                
                # FPS
                fps_texto = fuente.render(f"FPS: {int(self.clock.get_fps())}", True, BLANCO)
                self.pantalla.blit(fps_texto, (10, 10))
                
                # Nivel actual
                nivel_texto = fuente.render(
                    f"Nivel: {self.gestor_niveles.nivel_actual_numero}/3", 
                    True, BLANCO
                )
                self.pantalla.blit(nivel_texto, (10, 40))
                
                # Puntos
                texto_puntos = fuente.render(
                    f"Libros: {self.gestor_niveles.personaje.puntos // 100}", 
                    True, BLANCO
                )
                self.pantalla.blit(texto_puntos, (10, 70))
                
                # Vidas
                texto_vidas = fuente.render(
                    f"Vidas: {self.gestor_niveles.personaje.vidas}", 
                    True, BLANCO
                )
                self.pantalla.blit(texto_vidas, (ANCHO - 150, 10))
                
                pygame.display.flip()
                self.clock.tick(FPS)
        
        return False
    
    def ejecutar(self):
        """Método principal que controla el flujo del juego"""
        corriendo = True
        
        while corriendo:
            if self.estado == 'MENU':
                corriendo = self.mostrar_menu()
            elif self.estado == 'INTRODUCCION':
                corriendo = self.mostrar_introduccion()
            elif self.estado == 'JUGANDO':
                corriendo = self.bucle_juego()
        
        pygame.quit()