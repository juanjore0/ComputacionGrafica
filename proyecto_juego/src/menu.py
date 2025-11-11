import pygame
import os
from constantes import ANCHO, ALTO

class Boton:
    """Clase para manejar botones clickeables en el menú"""
    def __init__(self, x, y, ancho, alto, accion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.accion = accion
        self.hover = False
    
    def verificar_hover(self, pos_mouse):
        """Verifica si el mouse está sobre el botón"""
        self.hover = self.rect.collidepoint(pos_mouse)
        return self.hover
    
    def verificar_click(self, pos_mouse):
        """Verifica si se hizo click en el botón"""
        if self.rect.collidepoint(pos_mouse):
            return True
        return False
    
    def dibujar_debug(self, pantalla):
        """Dibuja el área del botón para debug (opcional)"""
        color = (255, 255, 0, 100) if self.hover else (255, 0, 0, 100)
        s = pygame.Surface((self.rect.width, self.rect.height))
        s.set_alpha(100)
        s.fill(color[:3])
        pantalla.blit(s, (self.rect.x, self.rect.y))


class Menu:
    """Clase para manejar el menú principal del juego"""
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.activo = True
        self.debug_mode = False  # Cambiar a True para ver las áreas de los botones
        
        # Cargar imágenes del menú (normal, hover play, hover quit)
        base = os.path.dirname(os.path.abspath(__file__))
        ruta_menu_normal = os.path.join(base, '..', 'assets', 'images', 'menus', 'inicio.png')
        ruta_menu_play = os.path.join(base, '..', 'assets', 'images', 'menus', 'inicio_play.png')
        ruta_menu_quit = os.path.join(base, '..', 'assets', 'images', 'menus', 'inicio_quit.png')
        
        try:
            self.imagen_normal = pygame.image.load(ruta_menu_normal).convert()
            self.imagen_normal = pygame.transform.scale(self.imagen_normal, (ANCHO, ALTO))
            
            self.imagen_play_hover = pygame.image.load(ruta_menu_play).convert()
            self.imagen_play_hover = pygame.transform.scale(self.imagen_play_hover, (ANCHO, ALTO))
            
            self.imagen_quit_hover = pygame.image.load(ruta_menu_quit).convert()
            self.imagen_quit_hover = pygame.transform.scale(self.imagen_quit_hover, (ANCHO, ALTO))
            
            self.imagen_actual = self.imagen_normal
            print("✓ Menú cargado correctamente (3 estados)")
        except Exception as e:
            print(f"Error cargando menú: {e}")
            # Crear un menú simple si falla la carga
            self.imagen_normal = pygame.Surface((ANCHO, ALTO))
            self.imagen_normal.fill((40, 70, 120))
            self.imagen_play_hover = self.imagen_normal
            self.imagen_quit_hover = self.imagen_normal
            self.imagen_actual = self.imagen_normal
        
        # Crear botones basados en las posiciones en tu imagen
        # Botón PLAY (coordenadas ajustadas basadas en la imagen)
        self.boton_play = Boton(
            x=145,           # Posición X del botón
            y=430,           # Posición Y del botón
            ancho=165,       # Ancho del área clickeable
            alto=90,         # Alto del área clickeable
            accion='jugar'
        )
        
        # Botón QUIT (coordenadas ajustadas basadas en la imagen)
        self.boton_quit = Boton(
            x=485,           # Posición X del botón
            y=430,           # Posición Y del botón
            ancho=165,       # Ancho del área clickeable
            alto=90,         # Alto del área clickeable
            accion='salir'
        )
        
        self.botones = [self.boton_play, self.boton_quit]
        
        # Cursor personalizado (opcional)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    def manejar_eventos(self, eventos):
        """Maneja los eventos del menú"""
        pos_mouse = pygame.mouse.get_pos()
        
        # Actualizar hover de los botones y cambiar imagen según hover
        play_hover = self.boton_play.verificar_hover(pos_mouse)
        quit_hover = self.boton_quit.verificar_hover(pos_mouse)
        
        # Cambiar la imagen según qué botón tiene hover
        if play_hover:
            self.imagen_actual = self.imagen_play_hover
        elif quit_hover:
            self.imagen_actual = self.imagen_quit_hover
        else:
            self.imagen_actual = self.imagen_normal
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return 'salir'
            
            # Detectar clicks
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Click izquierdo
                    # Verificar qué botón fue clickeado
                    if self.boton_play.verificar_click(pos_mouse):
                        print("¡Botón PLAY presionado!")
                        return 'jugar'
                    
                    if self.boton_quit.verificar_click(pos_mouse):
                        print("¡Botón QUIT presionado!")
                        return 'salir'
            
            # Atajo de teclado (opcional)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    return 'jugar'
                if evento.key == pygame.K_ESCAPE:
                    return 'salir'
                # Debug mode toggle
                if evento.key == pygame.K_F1:
                    self.debug_mode = not self.debug_mode
                    print(f"Debug mode: {self.debug_mode}")
        
        return None
    
    def dibujar(self):
        """Dibuja el menú en la pantalla"""
        # Dibujar la imagen del menú (cambia según el hover)
        self.pantalla.blit(self.imagen_actual, (0, 0))
        
        # Dibujar áreas de botones en modo debug
        if self.debug_mode:
            for boton in self.botones:
                boton.dibujar_debug(self.pantalla)
            
            # Mostrar instrucciones de debug
            fuente = pygame.font.Font(None, 24)
            texto = fuente.render("F1: Toggle Debug | Mouse: Hover/Click", True, (255, 255, 255))
            self.pantalla.blit(texto, (10, 10))
    
    def mostrar(self, clock, fps):
        """Bucle principal del menú"""
        while self.activo:
            # Obtener eventos
            eventos = pygame.event.get()
            
            # Manejar eventos y obtener acción
            accion = self.manejar_eventos(eventos)
            
            # Ejecutar acción si hay alguna
            if accion == 'jugar':
                self.activo = False
                return 'jugar'
            elif accion == 'salir':
                self.activo = False
                return 'salir'
            
            # Dibujar
            self.dibujar()
            
            # Actualizar pantalla
            pygame.display.flip()
            clock.tick(fps)
        
        return 'salir'