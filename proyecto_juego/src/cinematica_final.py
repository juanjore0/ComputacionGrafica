import pygame
import os
from constantes import ANCHO, ALTO

class CinematicaFinal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        self.font_dialogo = pygame.font.Font(None, 36)
        self.font_nombre = pygame.font.Font(None, 40)
        self.font_instruccion = pygame.font.Font(None, 24)
        
        # --- CARGA DE IMÁGENES ---
        self.fondos = {}
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imgs = os.path.join(base, 'assets', 'images', 'backgrounds')
        

        lista_imagenes = {
            'escuela': 'historia_final.png', # Reusamos la del final del nivel o una nueva 'final_escuela.png'
            'fogata': 'fogata1.png'
        }
        
        print("--- CARGANDO CINEMÁTICA FINAL ---")
        for clave, nombre_archivo in lista_imagenes.items():
            ruta = os.path.join(ruta_imgs, nombre_archivo)
            try:
                img = pygame.image.load(ruta).convert()
                img = pygame.transform.scale(img, (ANCHO, ALTO))
                self.fondos[clave] = img
                print(f"✓ Cargado: {nombre_archivo}")
            except Exception as e:
                print(f"⚠ Error cargando {nombre_archivo}: {e}")
                surf = pygame.Surface((ANCHO, ALTO))
                surf.fill((10, 20, 40)) # Azul oscuro final
                self.fondos[clave] = surf

        self.fondo_actual = self.fondos['escuela']
        
        # --- DIÁLOGOS FINALES (Cortos y Emotivos) ---
        self.dialogos = [
            # ESCENA 1: LLEGADA A LA ESCUELA (El Pasado)
            ("Abuelo", "Y así, con las piernas temblando y el corazón a mil..."), 
            ("Abuelo", "Finalmente vi las puertas de la escuela frente a mí."), 
            ("Abuelo", "Estaba sucio y exhausto, pero tenía mis libros a salvo."),
            
            # ESCENA 2: VUELTA A LA FOGATA (El Presente)
            ("Nieto", "¡Guau! ¿Hacías todo eso solo para poder estudiar?"), 
            ("Abuelo", "Cada día. Porque el conocimiento es la aventura más valiosa."),
            ("Abuelo", "El camino nunca es fácil, pero la recompensa siempre vale la pena."),
            ("Abuelo", "Y ahora, nieto mío... es tu turno de escribir tu propia historia."),
            ("Sistema", "GRACIAS POR JUGAR")
        ]
        
        # --- CAMBIOS DE FONDO ---
        self.cambios_fondo = {
            0: 'escuela',  # Empieza viendo la escuela
            3: 'fogata'    # Vuelve a la fogata cuando habla el Nieto
        }
        
        self.indice_dialogo = 0
        self.texto_actual = ""
        self.letra_indice = 0
        self.velocidad_texto = 2 
        self.contador_ticks = 0
        self.terminado_escribir = False
        
        self.activo = True

    def reiniciar(self):
        self.indice_dialogo = 0
        self.texto_actual = ""
        self.letra_indice = 0
        self.terminado_escribir = False
        self.activo = True
        self.fondo_actual = self.fondos['escuela'] 

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'salir'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'terminar' 
                
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not self.terminado_escribir:
                        if self.indice_dialogo < len(self.dialogos):
                            personaje, frase = self.dialogos[self.indice_dialogo]
                            self.texto_actual = frase
                            self.terminado_escribir = True
                    else:
                        self.indice_dialogo += 1
                        self.letra_indice = 0
                        self.texto_actual = ""
                        self.terminado_escribir = False
                        
                        if self.indice_dialogo >= len(self.dialogos):
                            return 'terminar'
                        
                        # Cambio de fondo
                        if self.indice_dialogo in self.cambios_fondo:
                            clave_nueva = self.cambios_fondo[self.indice_dialogo]
                            self.fondo_actual = self.fondos[clave_nueva]
                            
        return None

    def actualizar(self):
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

    def dibujar_texto_multilinea(self, texto, x, y, max_ancho, color):
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            prueba_linea = linea_actual + palabra + " "
            ancho_linea, _ = self.font_dialogo.size(prueba_linea)
            
            if ancho_linea < max_ancho:
                linea_actual = prueba_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)
        
        altura_linea = self.font_dialogo.get_linesize()
        for i, linea in enumerate(lineas):
            texto_surface = self.font_dialogo.render(linea, True, color)
            self.pantalla.blit(texto_surface, (x, y + (i * altura_linea)))

    def dibujar(self):
        self.pantalla.blit(self.fondo_actual, (0, 0))
        
        superficie_panel = pygame.Surface((ANCHO, 220))
        superficie_panel.set_alpha(210)
        superficie_panel.fill((0, 0, 0))
        rect_panel = superficie_panel.get_rect(bottom=ALTO)
        self.pantalla.blit(superficie_panel, rect_panel)
        
        if self.indice_dialogo < len(self.dialogos):
            personaje, frase = self.dialogos[self.indice_dialogo]
            
            # Color especial para el mensaje de SISTEMA
            if personaje == "Sistema":
                color_nombre = (255, 50, 50) # Rojo
                color_texto = (255, 255, 0)  # Amarillo
            else:
                color_nombre = (255, 200, 100) if personaje == "Abuelo" else (100, 200, 255)
                color_texto = (255, 255, 255)
            
            texto_nombre = self.font_nombre.render(personaje, True, color_nombre)
            self.pantalla.blit(texto_nombre, (50, ALTO - 190))
            
            margen_x = 50
            ancho_maximo = ANCHO - (margen_x * 2)
            self.dibujar_texto_multilinea(
                self.texto_actual, 
                margen_x, 
                ALTO - 150, 
                ancho_maximo, 
                color_texto
            )
            
            if self.terminado_escribir:
                if (pygame.time.get_ticks() // 500) % 2 == 0: 
                    flecha = self.font_instruccion.render("Presiona ESPACIO ▼", True, (150, 150, 150))
                    self.pantalla.blit(flecha, (ANCHO - 250, ALTO - 40))

    def mostrar(self, clock, fps):
        while self.activo:
            accion = self.manejar_eventos()
            
            if accion == 'salir': return 'salir'
            elif accion == 'terminar': return 'terminar'
            
            self.actualizar()
            self.dibujar()
            
            pygame.display.flip()
            clock.tick(fps)
        
        return 'terminar'