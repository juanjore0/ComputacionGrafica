import pygame
import os
from constantes import ANCHO, ALTO

class Cinematica:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        self.font_dialogo = pygame.font.Font(None, 36)
        self.font_nombre = pygame.font.Font(None, 40)
        self.font_instruccion = pygame.font.Font(None, 24)
        
        # --- CARGA DE IMÁGENES ---
        self.fondos = {}
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imgs = os.path.join(base, 'assets', 'images', 'backgrounds')
        
        # Lista de claves y nombres de archivo
        lista_imagenes = {
            'fogata': 'intro_fogata.png',
            'camino': 'historia_camino.png', 
            'rio': 'historia_rio.png',       
            'final': 'historia_final.png'    
        }
        
        print("--- CARGANDO CINEMÁTICA ---")
        for clave, nombre_archivo in lista_imagenes.items():
            ruta = os.path.join(ruta_imgs, nombre_archivo)
            try:
                img = pygame.image.load(ruta).convert()
                img = pygame.transform.scale(img, (ANCHO, ALTO))
                self.fondos[clave] = img
                print(f"✓ Cargado: {nombre_archivo}")
            except Exception as e:
                print(f"⚠ Error cargando {nombre_archivo}: {e}")
                # Fallback: Color sólido si falta la imagen
                surf = pygame.Surface((ANCHO, ALTO))
                surf.fill((20, 10, 30))
                self.fondos[clave] = surf

        self.fondo_actual = self.fondos['fogata']
        
        # --- DIÁLOGOS ---
        self.dialogos = [
            # FOGATA (Índices 0, 1, 2)
            ("Abuelo", "La fogata crepita con fuerza esta noche, ¿verdad, hijo?"), # 0
            ("Abuelo", "Su calor... me recuerda a aquellos amaneceres helados de mi juventud."), # 1
            ("Nieto", "¿Amaneceres, abuelo?"), # 2
            
            # CAMBIO A CAMINO (Índices 3, 4, 5)
            ("Abuelo", "Sí... Cuando tenía tu edad, el mundo era muy distinto al que conoces."), # 3
            ("Abuelo", "No había autobuses escolares, ni caminos pavimentados que facilitaran el viaje."), # 4
            ("Abuelo", "Ir a la escuela era una auténtica batalla diaria contra la propia naturaleza."), # 5
            
            # CAMBIO A RÍO (Índices 6, 7)
            ("Abuelo", "Recuerdo bosques que parecían no tener fin y ríos caudalosos que rugían con furia."), # 6
            ("Abuelo", "Cada día era una prueba de valor y resistencia, solo por el deseo de aprender."), # 7
            
            # CAMBIO A FINAL (Índices 8, 9)
            ("Abuelo", "Cierra los ojos e imagina que eres yo en aquel entonces, enfrentando lo desconocido."), # 8
            ("Abuelo", "Dime... ¿Crees que tienes lo necesario para llegar?"), # 9
        ]
        
        # --- MAPA DE CAMBIOS DE FONDO ---
        self.cambios_fondo = {
            0: 'fogata',
            3: 'camino',
            6: 'rio',
            8: 'final'
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
        self.fondo_actual = self.fondos['fogata'] 

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'salir'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'saltar' 
                
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not self.terminado_escribir:
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
                        
                        # --- VERIFICAR CAMBIO DE FONDO ---
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
        """Dibuja texto dividiéndolo en varias líneas si excede el ancho"""
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
        
        # Dibujar cada línea
        altura_linea = self.font_dialogo.get_linesize()
        for i, linea in enumerate(lineas):
            texto_surface = self.font_dialogo.render(linea, True, color)
            self.pantalla.blit(texto_surface, (x, y + (i * altura_linea)))

    def dibujar(self):
        # Dibujar el fondo actual
        self.pantalla.blit(self.fondo_actual, (0, 0))
        
        # Panel de texto más alto para acomodar varias líneas
        altura_panel = 220
        superficie_panel = pygame.Surface((ANCHO, altura_panel))
        superficie_panel.set_alpha(210)
        superficie_panel.fill((0, 0, 0))
        rect_panel = superficie_panel.get_rect(bottom=ALTO)
        self.pantalla.blit(superficie_panel, rect_panel)
        
        if self.indice_dialogo < len(self.dialogos):
            personaje, frase = self.dialogos[self.indice_dialogo]
            
            color_nombre = (255, 200, 100) if personaje == "Abuelo" else (100, 200, 255)
            
            # Nombre
            texto_nombre = self.font_nombre.render(personaje, True, color_nombre)
            # Subimos un poco el nombre para dar espacio al texto
            self.pantalla.blit(texto_nombre, (50, ALTO - 190))
            
            # --- USAR EL NUEVO DIBUJADO MULTILÍNEA ---
            margen_x = 50
            ancho_maximo = ANCHO - (margen_x * 2) # Margen de 50px a cada lado
            self.dibujar_texto_multilinea(
                self.texto_actual, 
                margen_x, 
                ALTO - 150, 
                ancho_maximo, 
                (255, 255, 255)
            )
            
            if self.terminado_escribir:
                if (pygame.time.get_ticks() // 500) % 2 == 0: 
                    flecha = self.font_instruccion.render("Presiona ESPACIO ->", True, (150, 150, 150))
                    self.pantalla.blit(flecha, (ANCHO - 250, ALTO - 40))

    def mostrar(self, clock, fps):
        while self.activo:
            accion = self.manejar_eventos()
            
            if accion == 'salir': return 'salir'
            elif accion == 'saltar' or accion == 'terminar': return 'menu' 
            
            self.actualizar()
            self.dibujar()
            
            pygame.display.flip()
            clock.tick(fps)
        
        return 'menu'