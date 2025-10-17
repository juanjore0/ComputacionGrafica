import pygame 

#funcion para dibujar un circulo en la pantalla
def dibujar_circulo(pantalla, color, centro, radio, ancho=0):
    pygame.draw.circle(pantalla, color, centro, radio, ancho)

#funcion para dibujar un rectangulo en la pantalla
def dibujar_rectangulo(pantalla, color, rect, ancho=0):
    pygame.draw.rect(pantalla, color, rect, ancho)

#funcion para dibujar una elipse en la pantalla
def dibujar_elipse(pantalla, color, rect, ancho=0):
    pygame.draw.ellipse(pantalla, color, rect, ancho)

#funcion para dibujar una linea en la pantalla
def dibujar_linea(pantalla, color, start_pos, end_pos, ancho=1):
    pygame.draw.line(pantalla, color, start_pos, end_pos, ancho)

#funcion para dibujar un poligono en la pantalla
def dibujar_poligono(pantalla, color, puntos, ancho=0):
    pygame.draw.polygon(pantalla, color, puntos, ancho)