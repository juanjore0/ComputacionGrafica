import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Posiciones iniciales
player_pos = pygame.Vector2((screen.get_width() / 2) - 600, screen.get_height() / 2)
player_pos2 = pygame.Vector2((screen.get_width() / 2) + 600, screen.get_height() / 2)

# Límites del tablero
x1, y1 = 20, 20
x2, y2 = screen.get_width() - 20, screen.get_height() - 20

# Pelota
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_radius = 10
ball_speed = pygame.Vector2(250, 200)  # velocidad inicial (px/segundo)

# Marcador
score_left = 0
score_right = 0
font = pygame.font.Font(None, 74)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Jugadores (rectángulos)
    player_rect = pygame.Rect(player_pos.x, player_pos.y, 10, 80)
    player_rect2 = pygame.Rect(player_pos2.x, player_pos2.y, 10, 80)

    pygame.draw.rect(screen, "white", player_rect)
    pygame.draw.rect(screen, "purple", player_rect2)

    # Pelota
    pygame.draw.circle(screen, "red", ball_pos, ball_radius)
    ball_pos += ball_speed * dt
    # Rebote pelota con los bordes superior e inferior
    if ball_pos.y - ball_radius <= y1 or ball_pos.y + ball_radius >= y2:
        ball_speed.y *= -1

    # Rebote pelota con los jugadores
    if player_rect.collidepoint(ball_pos) or player_rect2.collidepoint(ball_pos):
        ball_speed.x *= -1
    
    # Anotar puntos
    if ball_pos.x - ball_radius <= x1:  # salió por la izquierda → punto jugador derecho
        score_right += 1
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # reset posición
        ball_speed.x *= -1  # cambiar dirección

    if ball_pos.x + ball_radius >= x2:  # salió por la derecha → punto jugador izquierdo
        score_left += 1
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_speed.x *= -1

    

    # Bordes del tablero
    pygame.draw.line(screen, "white", (x1, y1), (x2, y1), 4)  # superior
    pygame.draw.line(screen, "white", (x1, y2), (x2, y2), 4)  # inferior
    pygame.draw.line(screen, "white", (x1, y1), (x1, y2), 4)  # izquierda
    pygame.draw.line(screen, "white", (x2, y1), (x2, y2), 4)  # derecha
    # Línea central
    pygame.draw.line(screen, "white", (screen.get_width() / 2, y1), (screen.get_width() / 2, y2), 4)

    # Movimiento jugadores
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    if keys[pygame.K_UP]:
        player_pos2.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos2.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos2.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos2.x += 300 * dt

    # Rect de colisión para la línea central
    middle_line = pygame.Rect(screen.get_width() / 2 - 2, y1, 4, y2 - y1)

    # Colisión jugador 1 con línea central
    if player_rect.colliderect(middle_line):
        player_pos.x -= 10  # lo regresamos
    # Colisión jugador 2 con línea central
    if player_rect2.colliderect(middle_line):
        player_pos2.x += 10

    # Límites para que no salgan del tablero
    player_pos.x = max(x1, min(player_pos.x, x2 - player_rect.width))
    player_pos.y = max(y1, min(player_pos.y, y2 - player_rect.height))

    player_pos2.x = max(x1, min(player_pos2.x, x2 - player_rect2.width))
    player_pos2.y = max(y1, min(player_pos2.y, y2 - player_rect2.height))

    # Mostrar marcador
    text_left = font.render(str(score_left), True, "white")
    text_right = font.render(str(score_right), True, "white")
    screen.blit(text_left, (screen.get_width() // 2 - 100, 40))
    screen.blit(text_right, (screen.get_width() // 2 + 60, 40))
    
      
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
