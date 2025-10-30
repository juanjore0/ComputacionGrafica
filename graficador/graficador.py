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
ANCHO_PANEL = 280
FPS = 60
COLOR_BG = (28, 28, 32)
COLOR_PANEL = (20, 20, 24)
COLOR_TEXTO = (240, 240, 240)
COLOR_BORDE = (70, 70, 80)
COLOR_CANVAS = (255, 255, 255)
COLOR_GRID = (230, 230, 235)
COLOR_AXES = (120, 120, 120)

# Paleta de colores disponibles
PALETA_COLORES = [
    ("Rojo", (255, 0, 0)),
    ("Azul", (0, 0, 255)),
    ("Verde", (0, 200, 0)),
    ("Amarillo", (255, 255, 0)),
    ("Naranja", (255, 140, 0)),
    ("Púrpura", (160, 32, 240)),
    ("Rosa", (255, 105, 180)),
    ("Turquesa", (64, 224, 208)),
    ("Negro", (0, 0, 0)),
    ("Gris", (128, 128, 128))
]

# Colores por tipo de figura (por defecto)
COLORES_FIGURAS = {
    "Linea_DDA": (255, 69, 0),
    "Linea_Bresenham": (30, 144, 255),
    "Circulo": (34, 139, 34),
    "Elipse": (147, 112, 219),
    "Triangulo": (255, 215, 0),
    "Rectangulo": (220, 20, 60),
    "Poligono": (64, 224, 208),
    "Bezier": (255, 105, 180),
    "Lapiz": (0, 0, 0)
}

# -----------------------------
# Clase Boton (POO)
# -----------------------------
class Boton:
    def __init__(self, x, y, w, h, texto, on_click=None,
                 color=(70, 130, 180), color_hover=(100, 160, 210),
                 color_texto=(255, 255, 255), fuente=None):
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
        pygame.draw.rect(surface, col, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=10)
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
# Clase BotonColor (selector circular)
# -----------------------------
class BotonColor:
    def __init__(self, x, y, radio, color, on_click=None):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.on_click = on_click
        self.hover = False
        self.activo = False

    def draw(self, surface):
        # Círculo de color
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radio)
        
        # Borde
        borde_color = (255, 255, 255) if self.activo else (200, 200, 200)
        borde_width = 4 if self.activo else 2
        pygame.draw.circle(surface, borde_color, (self.x, self.y), self.radio, borde_width)
        
        # Efecto hover
        if self.hover and not self.activo:
            pygame.draw.circle(surface, (255, 255, 100), (self.x, self.y), self.radio + 3, 2)

    def handle(self, events):
        mouse_pos = pygame.mouse.get_pos()
        dist = math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        self.hover = dist <= self.radio
        
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
    puntos_x = linea_bresenham(0, cy, w-1, cy)
    dibujar_puntos(surface, puntos_x, color)
    puntos_y = linea_bresenham(cx, 0, cx, h-1)
    dibujar_puntos(surface, puntos_y, color)


# -----------------------------
# App Graficador
# -----------------------------
class GraficadorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("🎨 Graficador 2D")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 36)
        self.font_subtitle = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 22)

        # Canvas donde se dibuja
        canvas_w = ANCHO - ANCHO_PANEL - 30
        canvas_h = ALTO - 40
        self.canvas = pygame.Surface((canvas_w, canvas_h))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.topleft = (15, 20)

        # Estado
        self.herramienta = "Linea_Bresenham"
        self.color_actual = (0, 0, 0)  # Color seleccionado
        self.mostrando_grid = True
        self.mostrando_ejes = True
        self.dibujando = False
        self.puntos_temp = []
        self.figuras = []

        # Estado para lápiz (dibujo a mano alzada)
        self.modo_lapiz = False
        self.puntos_lapiz = []

        # Estado para polígonos y Bézier
        self.modo_poligono = False
        self.vertices_poligono = []
        self.modo_bezier = False
        self.puntos_bezier = []

        self.limpiar_canvas()
        self.botones = []
        self.botones_color = []
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
        x = ANCHO - ANCHO_PANEL + 15
        y = 80
        w = ANCHO_PANEL - 30
        h = 40
        sep = 8

        def set_tool(nombre):
            def _cb():
                self.herramienta = nombre
                self.cancelar_modos_especiales()
                for b in self.botones:
                    if hasattr(b, 'es_herramienta') and b.es_herramienta:
                        b.activo = (b.texto == nombre.replace('_', ' '))
            return _cb

        # Herramientas con colores personalizados
        herramientas = [
            ("Lápiz", "Lapiz", (50, 50, 50), (80, 80, 80)),
            ("Linea DDA", "Linea_DDA", (255, 99, 71), (255, 129, 101)),
            ("Linea Bresenham", "Linea_Bresenham", (30, 144, 255), (60, 174, 255)),
            ("Circulo", "Circulo", (50, 205, 50), (80, 235, 80)),
            ("Elipse", "Elipse", (147, 112, 219), (177, 142, 249)),
            ("Triangulo", "Triangulo", (255, 215, 0), (255, 245, 30)),
            ("Rectangulo", "Rectangulo", (220, 20, 60), (250, 50, 90)),
            ("Poligono", "Poligono", (64, 224, 208), (94, 254, 238)),
            ("Bezier", "Bezier", (255, 105, 180), (255, 135, 210))
        ]

        for i, (texto, nombre, color, color_hover) in enumerate(herramientas):
            btn = Boton(x, y + i*(h+sep), w, h, texto, 
                    on_click=set_tool(nombre),
                    color=color,
                    color_hover=color_hover)
            btn.es_herramienta = True
            if nombre == self.herramienta:
                btn.activo = True
            self.botones.append(btn)

        # --- BOTONES DE COLOR (ANTES DE LAS ACCIONES) ---
        y_colores = y + len(herramientas)*(h+sep) + 20
        
        # Título de sección
        self.y_titulo_colores = y_colores
        
        # Crear botones circulares de color
        radio = 16
        margen = 10
        cols = 5
        x_inicio = x + 15
        
        def set_color(color):
            def _cb():
                self.color_actual = color
                for bc in self.botones_color:
                    bc.activo = (bc.color == color)
            return _cb
        
        for i, (nombre, color) in enumerate(PALETA_COLORES):
            fila = i // cols
            col = i % cols
            bx = x_inicio + col * (radio * 2 + margen)
            by = y_colores + 30 + fila * (radio * 2 + margen)
            
            btn_color = BotonColor(bx, by, radio, color, on_click=set_color(color))
            if color == self.color_actual:
                btn_color.activo = True
            self.botones_color.append(btn_color)

        # Botones de acción (DESPUÉS DE LOS COLORES)
        y_acc = y_colores + 130
        
        b_deshacer = Boton(x, y_acc, w, h, "Deshacer", 
                        on_click=self.deshacer,
                        color=(138, 43, 226),
                        color_hover=(168, 73, 255))
        
        b_limpiar = Boton(x, y_acc + (h+sep), w, h, "Limpiar", 
                        on_click=self.vaciar_figuras,
                        color=(220, 20, 60),
                        color_hover=(250, 50, 90))

        y_toggle = y_acc + 2*(h+sep) + 10
        
        b_grid = Boton(x, y_toggle, w, h, "Cuadrícula", 
                    on_click=self.toggle_grid,
                    color=(70, 130, 180),
                    color_hover=(100, 160, 210))
        
        b_axes = Boton(x, y_toggle + (h+sep), w, h, "Ejes", 
                    on_click=self.toggle_axes,
                    color=(70, 130, 180),
                    color_hover=(100, 160, 210))

        self.botones.extend([b_deshacer, b_limpiar, b_grid, b_axes])

    def cancelar_modos_especiales(self):
        """Cancela modos de polígono, Bézier y lápiz"""
        self.modo_poligono = False
        self.vertices_poligono = []
        self.modo_bezier = False
        self.puntos_bezier = []
        self.modo_lapiz = False
        self.puntos_lapiz = []
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

            # Manejo de teclado
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

                    # Modo LÁPIZ (dibujo a mano alzada)
                    if self.herramienta == "Lapiz":
                        self.modo_lapiz = True
                        self.puntos_lapiz = [(mx, my)]

                    # Modo polígono
                    elif self.herramienta == "Poligono":
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
                # Modo lápiz: capturar movimiento mientras se mantiene presionado
                if self.modo_lapiz and self.canvas_rect.collidepoint(e.pos):
                    mx = e.pos[0] - self.canvas_rect.x
                    my = e.pos[1] - self.canvas_rect.y
                    mx = max(0, min(self.canvas.get_width()-1, mx))
                    my = max(0, min(self.canvas.get_height()-1, my))
                    self.puntos_lapiz.append((mx, my))

                # Preview para figuras normales
                elif self.dibujando and len(self.puntos_temp) > 0:
                    mx = e.pos[0] - self.canvas_rect.x
                    my = e.pos[1] - self.canvas_rect.y
                    mx = max(0, min(self.canvas.get_width()-1, mx))
                    my = max(0, min(self.canvas.get_height()-1, my))
                    if len(self.puntos_temp) == 1:
                        self.puntos_temp.append((mx, my))
                    else:
                        self.puntos_temp[1] = (mx, my)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                # Finalizar dibujo con lápiz
                if self.modo_lapiz:
                    self._finalizar_lapiz()
                    self.modo_lapiz = False

                # Finalizar figura normal
                if self.dibujando:
                    self.dibujando = False
                    if len(self.puntos_temp) == 2:
                        self._guardar_figura_normal()
                    self.puntos_temp = []

        # Manejo de botones de herramientas
        for b in self.botones:
            b.handle(eventos)

        # Manejo de botones de color
        for bc in self.botones_color:
            bc.handle(eventos)

        return True

    def _guardar_figura_normal(self):
        """Guarda figuras que requieren 2 puntos"""
        p0, p1 = self.puntos_temp
        figura = {
            "tipo": self.herramienta,
            "puntos": [p0, p1],
            "color": self.color_actual
        }
        self.figuras.append(figura)
        self._dibujar_figura(self.canvas, figura)

    def _finalizar_poligono(self):
        """Finaliza y guarda un polígono"""
        if len(self.vertices_poligono) >= 3:
            figura = {
                "tipo": "Poligono",
                "puntos": self.vertices_poligono.copy(),
                "color": self.color_actual
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
                "color": self.color_actual
            }
            self.figuras.append(figura)
            self._dibujar_figura(self.canvas, figura)
        self.modo_bezier = False
        self.puntos_bezier = []

    def _finalizar_lapiz(self):
        """Finaliza y guarda un trazo a mano alzada"""
        if len(self.puntos_lapiz) >= 2:
            figura = {
                "tipo": "Lapiz",
                "puntos": self.puntos_lapiz.copy(),
                "color": self.color_actual
            }
            self.figuras.append(figura)
            self._dibujar_figura(self.canvas, figura)
        self.puntos_lapiz = []

    def _dibujar_figura(self, surface, f):
        """Dibuja una figura usando algoritmos manuales"""
        tipo = f["tipo"]
        puntos_coords = f["puntos"]
        color = f["color"]

        if tipo == "Lapiz" and len(puntos_coords) >= 2:
            # Dibujar líneas conectando todos los puntos del trazo
            for i in range(len(puntos_coords) - 1):
                p0 = puntos_coords[i]
                p1 = puntos_coords[i + 1]
                pts = linea_bresenham(p0[0], p0[1], p1[0], p1[1])
                dibujar_puntos(surface, pts, color)

        elif tipo == "Linea_DDA" and len(puntos_coords) == 2:
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
        # Preview de trazo a mano alzada
        if self.modo_lapiz and len(self.puntos_lapiz) >= 2:
            for i in range(len(self.puntos_lapiz) - 1):
                p0 = self.puntos_lapiz[i]
                p1 = self.puntos_lapiz[i + 1]
                pts = linea_bresenham(p0[0], p0[1], p1[0], p1[1])
                dibujar_puntos(surface, pts, self.color_actual)

        # Preview de figuras normales
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

            # Fondo
            self.screen.fill(COLOR_BG)

            # Panel derecho
            panel_rect = pygame.Rect(ANCHO - ANCHO_PANEL, 0, ANCHO_PANEL, ALTO)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)
            
            # Título bonito en el panel
            titulo = self.font_title.render("Herramientas", True, (100, 200, 255))
            self.screen.blit(titulo, (ANCHO - ANCHO_PANEL + 15, 20))
            
            # Línea decorativa
            pygame.draw.line(self.screen, (100, 200, 255), 
                           (ANCHO - ANCHO_PANEL + 15, 60), 
                           (ANCHO - 15, 60), 3)

            # Botones de herramientas
            for b in self.botones:
                b.draw(self.screen)

            # Sección de colores
            titulo_colores = self.font_subtitle.render("Colores", True, (100, 200, 255))
            self.screen.blit(titulo_colores, (ANCHO - ANCHO_PANEL + 15, self.y_titulo_colores))
            
            # Botones de color
            for bc in self.botones_color:
                bc.draw(self.screen)

            # Canvas con preview
            preview_surface = self.canvas.copy()
            self._dibujar_preview(preview_surface)
            self.screen.blit(preview_surface, self.canvas_rect)

            # Borde del canvas
            pygame.draw.rect(self.screen, (100, 200, 255), self.canvas_rect, width=3, border_radius=5)

            # Instrucciones
            info_y = ALTO - 60
            if self.modo_lapiz:
                txt1 = self.font_small.render("Lápiz: Mantén presionado y dibuja", True, (200, 200, 210))
                self.screen.blit(txt1, (20, info_y))
            elif self.modo_poligono:
                txt1 = self.font_small.render("Polígono: Clic para agregar vértices", True, (200, 200, 210))
                txt2 = self.font_small.render("ENTER/ESPACIO para finalizar, ESC para cancelar", True, (200, 200, 210))
                self.screen.blit(txt1, (20, info_y))
                self.screen.blit(txt2, (20, info_y + 20))
            elif self.modo_bezier:
                txt1 = self.font_small.render(f"Bézier: {len(self.puntos_bezier)}/4 puntos de control", True, (200, 200, 210))
                txt2 = self.font_small.render("Clic para colocar puntos (se dibuja al 4to punto)", True, (200, 200, 210))
                self.screen.blit(txt1, (20, info_y))
                self.screen.blit(txt2, (20, info_y + 20))
            else:
                txt = self.font_small.render(f"Herramienta: {self.herramienta.replace('_', ' ')}", True, (200, 200, 210))
                self.screen.blit(txt, (20, info_y))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


# -----------------------------
# Ejecutar
# -----------------------------
if __name__ == "__main__":
    app = GraficadorApp()
    app.run()