import pygame
import os
from constantes import ANCHO, ALTO

class Introduccion:
    """Clase para manejar la introducción animada del juego"""
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.activo = True
        
        # Cargar los frames de la animación de la fogata
        base = os.path.dirname(os.path.abspath(__file__))
        # Como src está al mismo nivel que assets, subimos un nivel y entramos a assets
        ruta_backgrounds = os.path.join(base, '..', 'assets', 'images', 'backgrounds')
        
        # Normalizar la ruta (esto elimina los '..')
        ruta_backgrounds = os.path.normpath(ruta_backgrounds)
        
        # Imprimir la ruta para debug
        print(f"[DEBUG] Ruta base (src): {base}")
        print(f"[DEBUG] Buscando imágenes en: {ruta_backgrounds}")
        print(f"[DEBUG] ¿Existe la carpeta? {os.path.exists(ruta_backgrounds)}")
        
        # Listar archivos en la carpeta (si existe)
        if os.path.exists(ruta_backgrounds):
            archivos = os.listdir(ruta_backgrounds)
            print(f"[DEBUG] Archivos encontrados: {archivos}")
        
        self.frames = []
        frames_cargados = 0
        
        # Cargar las imágenes en orden (fogata1.jpg hasta fogata6.jpg)
        for i in range(1, 7):
            ruta_frame = os.path.join(ruta_backgrounds, f'fogata{i}.png')
            
            try:
                if os.path.exists(ruta_frame):
                    imagen = pygame.image.load(ruta_frame).convert()
                    imagen = pygame.transform.scale(imagen, (ANCHO, ALTO))
                    self.frames.append(imagen)
                    frames_cargados += 1
                    print(f"✓ fogata{i}.jpg cargada correctamente")
                else:
                    print(f"✗ No existe: {ruta_frame}")
            except Exception as e:
                print(f"✗ Error cargando fogata{i}.jpg: {e}")
        
        # Si no se cargó ningún frame, crear uno de respaldo
        if len(self.frames) == 0:
            print("⚠ ADVERTENCIA: No se cargaron imágenes. Usando frame de respaldo")
            frame_respaldo = pygame.Surface((ANCHO, ALTO))
            frame_respaldo.fill((30, 30, 50))
            
            # Dibujar mensaje de error
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render("Error: No se encontraron las imágenes", True, (255, 0, 0))
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            frame_respaldo.blit(texto, rect_texto)
            
            texto2 = fuente.render(f"Buscadas en: backgrounds/", True, (255, 255, 255))
            rect_texto2 = texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
            frame_respaldo.blit(texto2, rect_texto2)
            
            self.frames = [frame_respaldo]
        else:
            print(f"✓ Introducción cargada exitosamente: {frames_cargados} frames")
        
        # Control de animación
        self.frame_actual = 0
        self.velocidad_animacion = 10  # Cambiar frame cada 8 ticks
        self.contador_frames = 0
        
        # Control de tiempo
        self.duracion_total = 4  # 4 segundos
        self.tiempo_transcurrido = 0
        
        # Texto
        self.fuente = pygame.font.Font(None, 48)
        self.texto_skip = pygame.font.Font(None, 24)
        self.mostrar_titulo = True
        self.fade_in = 0
        
    def actualizar(self, dt):
        """Actualiza la animación"""
        self.contador_frames += 1
        if self.contador_frames >= self.velocidad_animacion:
            self.contador_frames = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
        
        self.tiempo_transcurrido += dt
        
        if self.fade_in < 255:
            self.fade_in += 5
        
    def manejar_eventos(self, eventos):
        """Maneja eventos de la introducción"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return 'salir'
            
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return 'finalizar'
        
        if self.tiempo_transcurrido >= self.duracion_total:
            return 'finalizar'
        
        return None
    
    def dibujar(self):
        """Dibuja el frame actual de la introducción"""
        # Dibujar el frame de la fogata
        self.pantalla.blit(self.frames[self.frame_actual], (0, 0))
        
        # Título (opcional - puedes eliminarlo si no lo quieres)
        if self.mostrar_titulo and self.fade_in > 0:
            texto = self.fuente.render("Can You Go?", True, (255, 255, 255))
            texto.set_alpha(min(self.fade_in, 200))
            rect_texto = texto.get_rect(center=(ANCHO // 2, 100))
            self.pantalla.blit(texto, rect_texto)
        
        # Instrucción para saltar
        texto_skip = self.texto_skip.render("Presiona cualquier tecla para continuar...", True, (200, 200, 200))
        texto_skip.set_alpha(min(self.fade_in, 180))
        rect_skip = texto_skip.get_rect(center=(ANCHO // 2, ALTO - 50))
        self.pantalla.blit(texto_skip, rect_skip)
    
    def mostrar(self, clock, fps):
        """Bucle principal de la introducción"""
        while self.activo:
            dt = clock.get_time() / 1000.0
            eventos = pygame.event.get()
            
            resultado = self.manejar_eventos(eventos)
            
            if resultado == 'finalizar':
                self.activo = False
                return 'jugar'
            elif resultado == 'salir':
                self.activo = False
                return 'salir'
            
            self.actualizar(dt)
            self.dibujar()
            
            pygame.display.flip()
            clock.tick(fps)
        
        return 'jugar'
