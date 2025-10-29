

import pygame
import math
from algoritmos import (
    linea_dda, linea_bresenham, circunferencia_bresenham,
    elipse_bresenham, bezier_cubica, triangulo, rectangulo,
    poligono, dibujar_puntos
)

pygame.init()

# -----------------------------
# Configuración general
# -----------------------------
ANCHO, ALTO = 1200, 750
ANCHO_PANEL = 250
FPS = 60

COLOR_BG = (28, 28, 32)
COLOR_PANEL = (20, 20, 24)
COLOR_TEXTO = (240, 240, 240)
COLOR_BORDE = (70, 70, 80)

COLOR_CANVAS = (255, 255, 255)
COLOR_GRID = (230, 230, 235)
COLOR_AXES = (120, 120, 120)

# Colores por tipo de figura
COLORES_FIGURAS = {
    "Linea_DDA": (255, 69, 0),      # Naranja rojizo
    "Linea_Bresenham": (30, 144, 255),  # Azul
    "Circulo": (34, 139, 34),       # Verde
    "Elipse": (147, 112, 219),      # Púrpura
    "Triangulo": (255, 215, 0),     # Dorado
    "Rectangulo": (220, 20, 60),    # Carmesí
    "Poligono": (64, 224, 208),     # Turquesa
    "Bezier": (255, 105, 180)       # Rosa
}

# -----------------------------
# Clase Boton (POO)
# -----------------------------
class Boton:
    def __init__(self, x, y, w, h, texto, on_click=None,
                 color=(60, 62, 68), color_hover=(80, 82, 90),
                 color_texto=(240, 240, 240), fuente=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.on_click = on_click
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 26)
        self.hover = False
        self.activo = False

    def draw(self, surface):
        col = self.color_hover if (self.hover or self.activo) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDE, self.rect, width=1, border_radius=8)
        text_surf = self.fuente.render(self.texto, True, self.color_texto)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
                if self.on_click:
                    self.on_click()
                return True
        return False

# -----------------------------
# Utilidades de dibujo
# -----------------------------
def draw_grid(surface, spacing=20, color=COLOR_GRID):
    """Dibuja cuadrícula usando líneas Bresenham"""
    w, h = surface.get_size()
    for x in range(0, w, spacing):
        puntos = linea_bresenham(x, 0, x, h-1)
        dibujar_puntos(surface, puntos, color)
    for y in range(0, h, spacing):
        puntos = linea_bresenham(0, y, w-1, y)
        dibujar_puntos(surface, puntos, color)

def draw_axes(surface, color=COLOR_AXES):
    """Dibuja ejes usando líneas Bresenham"""
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    # Eje X
    puntos_x = linea_bresenham(0, cy, w-1, cy)
    dibujar_puntos(surface, puntos_x, color)
    # Eje Y
    puntos_y = linea_bresenham(cx, 0, cx, h-1)
    dibujar_puntos(surface, puntos_y, color)

# -----------------------------
# App Graficador
# -----------------------------
class GraficadorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Graficador 2D - Algoritmos Manuales")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 22)

        # Canvas donde se dibuja
        canvas_w = ANCHO - ANCHO_PANEL - 20
        canvas_h = ALTO - 40
        self.canvas = pygame.Surface((canvas_w, canvas_h))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.topleft = (ANCHO_PANEL + 10, 20)

        # Estado
        self.herramienta = "Linea_Bresenham"
        self.mostrando_grid = True
        self.mostrando_ejes = True
        self.dibujando = False
        self.puntos_temp = []  # Para figuras que requieren múltiples puntos
        self.figuras = []

        # Estado especial para polígonos y Bézier
        self.modo_poligono = False
        self.vertices_poligono = []
        self.modo_bezier = False
        self.puntos_bezier = []

        self.limpiar_canvas()
        self.botones = []
        self._crear_botones()

    def limpiar_canvas(self):
        """Limpia el canvas y redibuja grid, ejes y figuras existentes"""
        self.canvas.fill(COLOR_CANVAS)
        
        if self.mostrando_grid:
            draw_grid(self.canvas, spacing=20)
        if self.mostrando_ejes:
            draw_axes(self.canvas)

        # Redibujar figuras
        for f in self.figuras:
            self._dibujar_figura(self.canvas, f)

    def _crear_botones(self):
        x, y = 10, 15
        w = ANCHO_PANEL - 20
        h = 38
        sep = 6

        def set_tool(nombre):
            def _cb():
                self.herramienta = nombre
                self.cancelar_modos_especiales()
                for b in self.botones:
                    if hasattr(b, 'es_herramienta') and b.es_herramienta:
                        b.activo = (b.texto == nombre.replace('_', ' '))
            return _cb

        # Herramientas
        herramientas = [
            ("Linea DDA", "Linea_DDA"),
            ("Linea Bresenham", "Linea_Bresenham"),
            ("Circulo", "Circulo"),
            ("Elipse", "Elipse"),
            ("Triangulo", "Triangulo"),
            ("Rectangulo", "Rectangulo"),
            ("Poligono", "Poligono"),
            ("Bezier", "Bezier")
        ]

        for i, (texto, nombre) in enumerate(herramientas):
            btn = Boton(x, y + i*(h+sep), w, h, texto, on_click=set_tool(nombre))
            btn.es_herramienta = True
            if nombre == self.herramienta:
                btn.activo = True
            self.botones.append(btn)

        # Botones de acción
        y_acc = y + len(herramientas)*(h+sep) + 15
        b_deshacer = Boton(x, y_acc, w, h, "Deshacer", on_click=self.deshacer)
        b_limpiar = Boton(x, y_acc + (h+sep), w, h, "Limpiar", on_click=self.vaciar_figuras)

        y_toggle = y_acc + 2*(h+sep) + 15
        b_grid = Boton(x, y_toggle, w, h, "Toggle Cuadrícula", on_click=self.toggle_grid)
        b_axes = Boton(x, y_toggle + (h+sep), w, h, "Toggle Ejes", on_click=self.toggle_axes)

        self.botones.extend([b_deshacer, b_limpiar, b_grid, b_axes])

    def cancelar_modos_especiales(self):
        """Cancela modos de polígono y Bézier"""
        self.modo_poligono = False
        self.vertices_poligono = []
        self.modo_bezier = False
        self.puntos_bezier = []
        self.puntos_temp = []

    def deshacer(self):
        if self.figuras:
            self.figuras.pop()
            self.limpiar_canvas()

    def vaciar_figuras(self):
        self.figuras.clear()
        self.cancelar_modos_especiales()
        self.limpiar_canvas()

    def toggle_grid(self):
        self.mostrando_grid = not self.mostrando_grid
        self.limpiar_canvas()

    def toggle_axes(self):
        self.mostrando_ejes = not self.mostrando_ejes
        self.limpiar_canvas()

    def manejador_eventos(self):
        eventos = pygame.event.get()
        
        for e in eventos:
            if e.type == pygame.QUIT:
                return False

            # Manejo de teclado para finalizar polígonos
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    if self.modo_poligono and len(self.vertices_poligono) >= 3:
                        self._finalizar_poligono()
                    elif self.modo_bezier and len(self.puntos_bezier) == 4:
                        self._finalizar_bezier()
                elif e.key == pygame.K_ESCAPE:
                    self.cancelar_modos_especiales()
                    self.limpiar_canvas()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.canvas_rect.collidepoint(e.pos):
                    mx = e.pos[0] - self.canvas_rect.x
                    my = e.pos[1] - self.canvas_rect.y
                    
                    # Modo polígono
                    if self.herramienta == "Poligono":
                        self.modo_poligono = True
                        self.vertices_poligono.append((mx, my))
                    # Modo Bézier
                    elif self.herramienta == "Bezier":
                        self.modo_bezier = True
                        self.puntos_bezier.append((mx, my))
                        if len(self.puntos_bezier) == 4:
                            self._finalizar_bezier()
                    # Figuras normales (2 puntos)
                    else:
                        self.dibujando = True
                        self.puntos_temp = [(mx, my)]

            elif e.type == pygame.MOUSEMOTION:
                if self.dibujando and len(self.puntos_temp) > 0:
                    mx = e.pos[0] - self.canvas_rect.x
                    my = e.pos[1] - self.canvas_rect.y
                    mx = max(0, min(self.canvas.get_width()-1, mx))
                    my = max(0, min(self.canvas.get_height()-1, my))
                    if len(self.puntos_temp) == 1:
                        self.puntos_temp.append((mx, my))
                    else:
                        self.puntos_temp[1] = (mx, my)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if self.dibujando:
                    self.dibujando = False
                    if len(self.puntos_temp) == 2:
                        self._guardar_figura_normal()
                    self.puntos_temp = []

        # Manejo de botones
        for b in self.botones:
            b.handle(eventos)

        return True

    def _guardar_figura_normal(self):
        """Guarda figuras que requieren 2 puntos"""
        p0, p1 = self.puntos_temp
        figura = {
            "tipo": self.herramienta,
            "puntos": [p0, p1],
            "color": COLORES_FIGURAS.get(self.herramienta, (0, 0, 0))
        }
        self.figuras.append(figura)
        self._dibujar_figura(self.canvas, figura)

    def _finalizar_poligono(self):
        """Finaliza y guarda un polígono"""
        if len(self.vertices_poligono) >= 3:
            figura = {
                "tipo": "Poligono",
                "puntos": self.vertices_poligono.copy(),
                "color": COLORES_FIGURAS["Poligono"]
            }
            self.figuras.append(figura)
            self._dibujar_figura(self.canvas, figura)
        self.modo_poligono = False
        self.vertices_poligono = []

    def _finalizar_bezier(self):
        """Finaliza y guarda una curva Bézier"""
        if len(self.puntos_bezier) == 4:
            figura = {
                "tipo": "Bezier",
                "puntos": self.puntos_bezier.copy(),
                "color": COLORES_FIGURAS["Bezier"]
            }
            self.figuras.append(figura)
            self._dibujar_figura(self.canvas, figura)
        self.modo_bezier = False
        self.puntos_bezier = []

    def _dibujar_figura(self, surface, f):
        """Dibuja una figura usando algoritmos manuales"""
        tipo = f["tipo"]
        puntos_coords = f["puntos"]
        color = f["color"]

        if tipo == "Linea_DDA" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            pts = linea_dda(p0[0], p0[1], p1[0], p1[1])
            dibujar_puntos(surface, pts, color)

        elif tipo == "Linea_Bresenham" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            pts = linea_bresenham(p0[0], p0[1], p1[0], p1[1])
            dibujar_puntos(surface, pts, color)

        elif tipo == "Circulo" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            radio = int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
            if radio > 0:
                pts = circunferencia_bresenham(p0[0], p0[1], radio)
                dibujar_puntos(surface, pts, color)

        elif tipo == "Elipse" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            rx = abs(p1[0] - p0[0])
            ry = abs(p1[1] - p0[1])
            if rx > 0 and ry > 0:
                pts = elipse_bresenham(p0[0], p0[1], rx, ry)
                dibujar_puntos(surface, pts, color)

        elif tipo == "Triangulo" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            # Triángulo equilátero aproximado
            cx = (p0[0] + p1[0]) // 2
            pts = triangulo(p0[0], p0[1], p1[0], p1[1], cx, p0[1] - abs(p1[0]-p0[0]))
            dibujar_puntos(surface, pts, color)

        elif tipo == "Rectangulo" and len(puntos_coords) == 2:
            p0, p1 = puntos_coords
            pts = rectangulo(p0[0], p0[1], p1[0], p1[1])
            dibujar_puntos(surface, pts, color)

        elif tipo == "Poligono" and len(puntos_coords) >= 3:
            pts = poligono(puntos_coords)
            dibujar_puntos(surface, pts, color)

        elif tipo == "Bezier" and len(puntos_coords) == 4:
            pts = bezier_cubica(*puntos_coords, num_puntos=100)
            dibujar_puntos(surface, pts, color)

    def _dibujar_preview(self, surface):
        """Dibuja vista previa mientras se arrastra"""
        if self.dibujando and len(self.puntos_temp) == 2:
            preview = {
                "tipo": self.herramienta,
                "puntos": self.puntos_temp,
                "color": (150, 150, 150)
            }
            self._dibujar_figura(surface, preview)

        # Preview de polígono en construcción
        if self.modo_poligono and len(self.vertices_poligono) >= 2:
            pts = poligono(self.vertices_poligono)
            dibujar_puntos(surface, pts, (150, 150, 150))

        # Preview de puntos de control Bézier
        if self.modo_bezier:
            for i, pt in enumerate(self.puntos_bezier):
                pygame.draw.circle(surface, (255, 0, 0), pt, 4)

    def run(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejador_eventos()

            # Fondo y panel
            self.screen.fill(COLOR_BG)
            panel_rect = pygame.Rect(0, 0, ANCHO_PANEL, ALTO)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)

            # Título
            titulo = self.font_title.render("Herramientas", True, COLOR_TEXTO)
            self.screen.blit(titulo, (10, -2))

            # Botones
            for b in self.botones:
                b.draw(self.screen)

            # Canvas con preview
            preview_surface = self.canvas.copy()
            self._dibujar_preview(preview_surface)
            self.screen.blit(preview_surface, self.canvas_rect)

            # Instrucciones
            info_y = ALTO - 60
            if self.modo_poligono:
                txt1 = self.font_small.render("Polígono: Clic para agregar vértices", True, (200, 200, 210))
                txt2 = self.font_small.render("ENTER/ESPACIO para finalizar, ESC para cancelar", True, (200, 200, 210))
                self.screen.blit(txt1, (ANCHO_PANEL + 14, info_y))
                self.screen.blit(txt2, (ANCHO_PANEL + 14, info_y + 20))
            elif self.modo_bezier:
                txt1 = self.font_small.render(f"Bézier: {len(self.puntos_bezier)}/4 puntos de control", True, (200, 200, 210))
                txt2 = self.font_small.render("Clic para colocar puntos (se dibuja al 4to punto)", True, (200, 200, 210))
                self.screen.blit(txt1, (ANCHO_PANEL + 14, info_y))
                self.screen.blit(txt2, (ANCHO_PANEL + 14, info_y + 20))
            else:
                txt = self.font_small.render(f"Herramienta: {self.herramienta.replace('_', ' ')}", True, (200, 200, 210))
                self.screen.blit(txt, (ANCHO_PANEL + 14, info_y))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# -----------------------------
# Ejecutar
# -----------------------------
if __name__ == "__main__":
    app = GraficadorApp()
    app.run()