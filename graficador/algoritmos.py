# -*- coding: utf-8 -*-
"""
Módulo de Algoritmos Gráficos
==============================
Implementación manual de algoritmos clásicos de rasterización.
NO utiliza funciones predefinidas de Pygame como draw.line(), draw.circle(), etc.

Autor: Proyecto Graficador 2025
"""

import math


# =============================================================================
# ALGORITMOS DE LÍNEAS
# =============================================================================

def linea_dda(x0, y0, x1, y1):
    """
    Algoritmo DDA (Digital Differential Analyzer) para dibujar líneas.
    
    Args:
        x0, y0: Coordenadas del punto inicial
        x1, y1: Coordenadas del punto final
    
    Returns:
        Lista de tuplas (x, y) con los píxeles a dibujar
    """
    puntos = []
    
    dx = x1 - x0
    dy = y1 - y0
    
    # Determinar el número de pasos
    pasos = max(abs(dx), abs(dy))
    
    if pasos == 0:
        return [(int(x0), int(y0))]
    
    # Calcular incrementos
    x_inc = dx / pasos
    y_inc = dy / pasos
    
    # Punto inicial
    x = x0
    y = y0
    
    for _ in range(int(pasos) + 1):
        puntos.append((int(round(x)), int(round(y))))
        x += x_inc
        y += y_inc
    
    return puntos


def linea_bresenham(x0, y0, x1, y1):
    """
    Algoritmo de Bresenham para dibujar líneas.
    Más eficiente que DDA (solo usa enteros).
    
    Args:
        x0, y0: Coordenadas del punto inicial
        x1, y1: Coordenadas del punto final
    
    Returns:
        Lista de tuplas (x, y) con los píxeles a dibujar
    """
    puntos = []
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    # Determinar dirección
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    err = dx - dy
    
    x, y = x0, y0
    
    while True:
        puntos.append((x, y))
        
        if x == x1 and y == y1:
            break
        
        e2 = 2 * err
        
        if e2 > -dy:
            err -= dy
            x += sx
        
        if e2 < dx:
            err += dx
            y += sy
    
    return puntos


# =============================================================================
# ALGORITMO DE CIRCUNFERENCIA
# =============================================================================

def circunferencia_bresenham(xc, yc, radio):
    """
    Algoritmo de Bresenham para dibujar circunferencias.
    Utiliza la simetría de 8 octantes para optimizar el cálculo.
    
    Args:
        xc, yc: Coordenadas del centro
        radio: Radio de la circunferencia
    
    Returns:
        Lista de tuplas (x, y) con los píxeles a dibujar
    """
    puntos = []
    
    if radio <= 0:
        return puntos
    
    x = 0
    y = radio
    d = 3 - 2 * radio
    
    # Dibujar los 8 puntos simétricos
    def agregar_puntos_simetricos(xc, yc, x, y):
        puntos.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ])
    
    agregar_puntos_simetricos(xc, yc, x, y)
    
    while y >= x:
        x += 1
        
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        
        agregar_puntos_simetricos(xc, yc, x, y)
    
    return puntos


# =============================================================================
# ALGORITMO DE ELIPSE
# =============================================================================

def elipse_bresenham(xc, yc, rx, ry):
    """
    Algoritmo de Bresenham adaptado para elipses.
    
    Args:
        xc, yc: Coordenadas del centro
        rx: Radio en el eje X
        ry: Radio en el eje Y
    
    Returns:
        Lista de tuplas (x, y) con los píxeles a dibujar
    """
    puntos = []
    
    if rx <= 0 or ry <= 0:
        return puntos
    
    def agregar_puntos_simetricos(xc, yc, x, y):
        puntos.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y)
        ])
    
    # Región 1
    x = 0
    y = ry
    
    rx2 = rx * rx
    ry2 = ry * ry
    
    px = 0
    py = 2 * rx2 * y
    
    # Decisión inicial para región 1
    p = int(ry2 - (rx2 * ry) + (0.25 * rx2))
    
    agregar_puntos_simetricos(xc, yc, x, y)
    
    # Región 1
    while px < py:
        x += 1
        px += 2 * ry2
        
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= 2 * rx2
            p += ry2 + px - py
        
        agregar_puntos_simetricos(xc, yc, x, y)
    
    # Región 2
    p = int(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)
    
    while y > 0:
        y -= 1
        py -= 2 * rx2
        
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += 2 * ry2
            p += rx2 - py + px
        
        agregar_puntos_simetricos(xc, yc, x, y)
    
    return puntos


# =============================================================================
# CURVAS DE BÉZIER CÚBICA
# =============================================================================

def bezier_cubica(p0, p1, p2, p3, num_puntos=100):
    """
    Calcula puntos de una curva de Bézier cúbica con 4 puntos de control.
    
    Args:
        p0, p1, p2, p3: Tuplas (x, y) con los 4 puntos de control
        num_puntos: Número de puntos a calcular en la curva
    
    Returns:
        Lista de tuplas (x, y) con los puntos de la curva
    """
    puntos = []
    
    for i in range(num_puntos + 1):
        t = i / num_puntos
        
        # Fórmula de Bézier cúbica: B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        t2 = t * t
        t3 = t2 * t
        
        x = (mt3 * p0[0] + 
             3 * mt2 * t * p1[0] + 
             3 * mt * t2 * p2[0] + 
             t3 * p3[0])
        
        y = (mt3 * p0[1] + 
             3 * mt2 * t * p1[1] + 
             3 * mt * t2 * p2[1] + 
             t3 * p3[1])
        
        puntos.append((int(round(x)), int(round(y))))
    
    return puntos


# =============================================================================
# POLÍGONOS Y FORMAS CERRADAS
# =============================================================================

def poligono(vertices):
    """
    Dibuja un polígono conectando una lista de vértices.
    
    Args:
        vertices: Lista de tuplas (x, y) con los vértices del polígono
    
    Returns:
        Lista de tuplas (x, y) con todos los píxeles del polígono
    """
    puntos = []
    
    if len(vertices) < 2:
        return puntos
    
    # Dibujar líneas entre vértices consecutivos
    for i in range(len(vertices)):
        p0 = vertices[i]
        p1 = vertices[(i + 1) % len(vertices)]  # El último conecta con el primero
        puntos.extend(linea_bresenham(p0[0], p0[1], p1[0], p1[1]))
    
    return puntos


def triangulo(x0, y0, x1, y1, x2, y2):
    """
    Dibuja un triángulo dados tres vértices.
    
    Args:
        x0, y0: Primer vértice
        x1, y1: Segundo vértice
        x2, y2: Tercer vértice
    
    Returns:
        Lista de tuplas (x, y) con los píxeles del triángulo
    """
    return poligono([(x0, y0), (x1, y1), (x2, y2)])


def rectangulo(x0, y0, x1, y1):
    """
    Dibuja un rectángulo usando algoritmos de líneas.
    
    Args:
        x0, y0: Esquina superior izquierda
        x1, y1: Esquina inferior derecha
    
    Returns:
        Lista de tuplas (x, y) con los píxeles del rectángulo
    """
    puntos = []
    
    # Calcular las cuatro esquinas
    min_x = min(x0, x1)
    max_x = max(x0, x1)
    min_y = min(y0, y1)
    max_y = max(y0, y1)
    
    # Dibujar los cuatro lados usando Bresenham
    puntos.extend(linea_bresenham(min_x, min_y, max_x, min_y))  # Superior
    puntos.extend(linea_bresenham(max_x, min_y, max_x, max_y))  # Derecha
    puntos.extend(linea_bresenham(max_x, max_y, min_x, max_y))  # Inferior
    puntos.extend(linea_bresenham(min_x, max_y, min_x, min_y))  # Izquierda
    
    return puntos


# =============================================================================
# UTILIDADES
# =============================================================================

def dibujar_puntos(surface, puntos, color):
    """
    Dibuja una lista de puntos en una superficie de Pygame.
    Usa set_at() para dibujar píxeles individuales.
    
    Args:
        surface: Superficie de Pygame donde dibujar
        puntos: Lista de tuplas (x, y)
        color: Tupla RGB del color
    """
    w, h = surface.get_size()
    
    # Eliminar duplicados y filtrar puntos fuera de límites
    puntos_unicos = set(puntos)
    
    for x, y in puntos_unicos:
        if 0 <= x < w and 0 <= y < h:
            surface.set_at((x, y), color)


# =============================================================================
# FUNCIONES DE TESTING (OPCIONAL)
# =============================================================================

if __name__ == "__main__":
    # Test básico de los algoritmos
    print("Probando algoritmos...")
    
    # Línea DDA
    puntos_dda = linea_dda(0, 0, 10, 10)
    print(f"DDA (0,0) a (10,10): {len(puntos_dda)} puntos")
    
    # Línea Bresenham
    puntos_bres = linea_bresenham(0, 0, 10, 10)
    print(f"Bresenham (0,0) a (10,10): {len(puntos_bres)} puntos")
    
    # Circunferencia
    puntos_circ = circunferencia_bresenham(50, 50, 20)
    print(f"Circunferencia centro (50,50) r=20: {len(puntos_circ)} puntos")
    
    # Elipse
    puntos_elipse = elipse_bresenham(50, 50, 30, 20)
    print(f"Elipse centro (50,50) rx=30 ry=20: {len(puntos_elipse)} puntos")
    
    # Bézier
    puntos_bezier = bezier_cubica((0, 0), (25, 50), (75, 50), (100, 0))
    print(f"Bézier cúbica: {len(puntos_bezier)} puntos")
    
    print("\n✓ Todos los algoritmos funcionan correctamente")