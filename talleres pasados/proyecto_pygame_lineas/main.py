import pygame
import sys

# Configuración
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dibujar línea con click")
clock = pygame.time.Clock()

drawing = False
start_pos = None
end_pos = None

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # botón izquierdo
                drawing = True
                start_pos = event.pos
                end_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                end_pos = event.pos
                # Aquí podrías guardar la línea o hacer algo con start_pos/end_pos

    # Dibujar fondo
    screen.fill(BG_COLOR)

    # Dibujar línea si existe
    if start_pos and end_pos:
        pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
