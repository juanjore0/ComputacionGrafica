import pygame
import os
from constantes import ANCHO, ALTO

class Cinematica:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        # Fuentes para el texto
        self.font_dialogo = pygame.font.Font(None, 36)
        self.font_nombre = pygame.font.Font(None, 40)
        self.font_instruccion = pygame.font.Font(None, 24)
        
        # Cargar imagen de fondo (La fogata)
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        ruta_fondo = os.path.join(base, 'assets', 'images', 'backgrounds', 'fogata6.png')
        
        try:
            self.fondo = pygame.image.load(ruta_fondo).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except:
            # Fallback: Fondo oscuro (marrón noche) si no hay imagen aún
            self.fondo = pygame.Surface((ANCHO, ALTO))
            self.fondo.fill((20, 10, 5)) 
        
        # --- DIÁLOGOS DE LA HISTORIA ---
        self.dialogos = [
            ("Abuelo", "Acércate a la fogata, nieto mío... La noche es fría."),
            ("Nieto", "¡Ya voy, abuelo!"),
            ("Nieto", "¿Qué historia nos contarás hoy?"),
            ("Abuelo", "Je, je... Hoy te contaré sobre aquellos días lejanos..."),
            ("Abuelo", "Cuando ir a la escuela no era tan fácil como tomar un autobús."),
            ("Abuelo", "Era una verdadera odisea. Una aventura diaria."),
            ("Abuelo", "Había rocas, ríos salvajes, bosques densos..."),
            ("Abuelo", "Y yo solo era un niño, decidido a aprender."),
            ("Abuelo", "¿Crees que podrías haberlo logrado tú?"),
            ("Abuelo", "Vamos a averiguarlo..."),
        ]
        
        # Variables de control
        self.indice_dialogo = 0
        self.texto_actual = ""
        self.letra_indice = 0
        self.velocidad_texto = 2  # Velocidad de escritura (más bajo es más rápido)
        self.contador_ticks = 0
        self.terminado_escribir = False
        
        self.activo = True

    def reiniciar(self):
        """Reinicia la cinemática para verla desde el principio"""
        self.indice_dialogo = 0
        self.texto_actual = ""
        self.letra_indice = 0
        self.terminado_escribir = False
        self.activo = True

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'salir'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'saltar' # Opción para saltar la intro
                
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not self.terminado_escribir:
                        # Si no terminó de escribir, completar la frase de golpe
                        personaje, frase = self.dialogos[self.indice_dialogo]
                        self.texto_actual = frase
                        self.terminado_escribir = True
                    else:
                        # Si ya terminó, pasar al siguiente diálogo
                        self.indice_dialogo += 1
                        self.letra_indice = 0
                        self.texto_actual = ""
                        self.terminado_escribir = False
                        
                        # Si no hay más diálogos, terminar
                        if self.indice_dialogo >= len(self.dialogos):
                            return 'terminar'
        return None

    def actualizar(self):
        # Lógica de máquina de escribir
        if self.indice_dialogo < len(self.dialogos):
            personaje, frase = self.dialogos[self.indice_dialogo]
            
            if not self.terminado_escribir:
                self.contador_ticks += 1
                if self.contador_ticks >= self.velocidad_texto:
                    self.contador_ticks = 0
                    if self.letra_indice < len(frase):
                        self.texto_actual += frase[self.letra_indice]
                        self.letra_indice += 1
                    else:
                        self.terminado_escribir = True

    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        
        # Panel de texto (fondo negro semitransparente abajo)
        superficie_panel = pygame.Surface((ANCHO, 200))
        superficie_panel.set_alpha(200)
        superficie_panel.fill((0, 0, 0))
        rect_panel = superficie_panel.get_rect(bottom=ALTO)
        self.pantalla.blit(superficie_panel, rect_panel)
        
        if self.indice_dialogo < len(self.dialogos):
            personaje, frase = self.dialogos[self.indice_dialogo]
            
            # Color del nombre según personaje
            # Abuelo: Naranja cálido, Nieto: Azul claro
            color_nombre = (255, 200, 100) if personaje == "Abuelo" else (100, 200, 255)
            
            # Dibujar Nombre
            texto_nombre = self.font_nombre.render(personaje, True, color_nombre)
            self.pantalla.blit(texto_nombre, (50, ALTO - 180))
            
            # Dibujar Texto
            texto_dialogo = self.font_dialogo.render(self.texto_actual, True, (255, 255, 255))
            self.pantalla.blit(texto_dialogo, (50, ALTO - 140))
            
            # Indicador de "Siguiente" (Parpadeante)
            if self.terminado_escribir:
                if (pygame.time.get_ticks() // 500) % 2 == 0: 
                    flecha = self.font_instruccion.render("Presiona ESPACIO para continuar ▼", True, (150, 150, 150))
                    self.pantalla.blit(flecha, (ANCHO - 350, ALTO - 40))

    def mostrar(self, clock, fps):
        """Bucle principal de la cinemática"""
        while self.activo:
            accion = self.manejar_eventos()
            
            if accion == 'salir':
                return 'salir'
            elif accion == 'saltar' or accion == 'terminar':
                return 'menu' # Ir al menú principal al terminar
            
            self.actualizar()
            self.dibujar()
            
            pygame.display.flip()
            clock.tick(fps)
        
        return 'menu'