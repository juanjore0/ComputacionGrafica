import pygame
import funciones as fn

# Inicializar pygame
pygame.init()

# Clase Boton (mantengo la tuya prácticamente igual)
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, color_texto=(255, 255, 255), fuente=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto 
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 36)
        self.hover = False

    def dibujar(self, pantalla):
        color_actual = self.color_hover if self.hover else self.color_normal
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def actualizar(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.hover:
                    return True
        return False


# ---------------------------
# Programa principal
# ---------------------------
if __name__ == "__main__":
    pantalla = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Dibujar Figuras con Botones")
    reloj = pygame.time.Clock()

    # Botones (mantengo tus posiciones y tamaños)
    boton_linea = Boton(50, 50, 200, 60, "LINEA", (0, 120, 250), (0, 180, 255))
    boton_circulo = Boton(260, 50, 200, 60, "CIRCULO", (200, 50, 50), (255, 80, 80))
    boton_rectangulo = Boton(470, 50, 200, 60, "RECTANGULO", (50, 200, 50), (80, 255, 80))
    boton_elipse = Boton(680, 50, 200, 60, "ELIPSE", (150, 0, 150), (200, 0, 200))
    boton_poligono = Boton(900, 50, 200, 60, "POLIGONO", (100, 100, 100), (150, 150, 150))

    # Variables de dibujo
    figuras = []           # Guardará todas las figuras dibujadas
    modo = None            # Puede ser "linea", "circulo", etc.
    punto_inicio = None    # Punto inicial de la figura
    area_botones = pygame.Rect(0, 0, 1200, 120)  # Zona de botones (evita que clic en botón cuente)

    ejecutando = True
    while ejecutando:
        eventos = pygame.event.get()

        # Manejo básico de salir
        for evento in eventos:
            if evento.type == pygame.QUIT:
                ejecutando = False

        if boton_linea.actualizar(eventos):
            modo = "linea"
            punto_inicio = None
        if boton_circulo.actualizar(eventos):
            modo = "circulo"
            punto_inicio = None
        if boton_rectangulo.actualizar(eventos):
            modo = "rectangulo"
            punto_inicio = None
        if boton_elipse.actualizar(eventos):
            modo = "elipse"
            punto_inicio = None
        if boton_poligono.actualizar(eventos):
            modo = "poligono"
            punto_inicio = None

        # --- Procesar clicks en el lienzo ---
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Ignorar si el click fue sobre la zona de botones
                if area_botones.collidepoint(evento.pos):
                    continue

                if modo == "linea":
                    if punto_inicio is None:
                        # primer click -> inicio
                        punto_inicio = evento.pos
                    else:
                        # segundo click -> fin => agregar línea y resetear inicio
                        punto_fin = evento.pos
                        figuras.append(("linea", (0, 0, 255), punto_inicio, punto_fin, 5))
                        punto_inicio = None
                
                if modo == "circulo":
                    if punto_inicio is None:
                        punto_inicio = evento.pos
                    else:
                        punto_fin = evento.pos
                        radio = int(((punto_fin[0] - punto_inicio[0]) ** 2 + (punto_fin[1] - punto_inicio[1]) ** 2) ** 0.5)
                        figuras.append(("circulo", (255, 0, 0), punto_inicio, radio, 0))
                        punto_inicio = None

                
                

        # --- Dibujado ---
        pantalla.fill((30, 30, 30))

        # Dibujar botones
        boton_linea.dibujar(pantalla)
        boton_circulo.dibujar(pantalla)
        boton_rectangulo.dibujar(pantalla)
        boton_elipse.dibujar(pantalla)
        boton_poligono.dibujar(pantalla)

        # Redibujar todas las figuras almacenadas
        for fig in figuras:
            if fig[0] == "linea":
                _, color, inicio, fin, grosor = fig
                fn.dibujar_linea(pantalla, color, inicio, fin, grosor)
            
            elif fig[0] == "circulo":
                _, color, centro, radio, ancho = fig
                fn.dibujar_circulo(pantalla, color, centro, radio, ancho)

        # Opcional: si quieres mostrar visualmente el punto_inicio mientras esperas el fin,
        # podrías dibujar un pequeño círculo en punto_inicio. Lo dejo comentado:
        # if punto_inicio is not None:
        #     pygame.draw.circle(pantalla, (255,255,0), punto_inicio, 4)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
