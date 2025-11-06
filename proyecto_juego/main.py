import pygame
pygame.init()

# --- CONFIGURACIÓN GENERAL ---
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Demo tipo Mario Bros - Pygame")
clock = pygame.time.Clock()

# --- COLORES ---
AZUL_CIELO = (135, 206, 235)
VERDE = (0, 200, 0)
ROJO = (255, 50, 50)
GRIS = (100, 100, 100)

# --- JUGADOR ---
player = pygame.Rect(100, 300, 40, 50)
vel_x = 0
vel_y = 0
en_suelo = False

# --- MAPA (1 = bloque sólido, 0 = vacío) ---
nivel = [
    "000000000000000000000000000000000000000000000000000000000000",
    "000000000000000000000000000000000000000000000000000000000000",
    "000000000000000000000000000000000000000000000000000000000000",
    "000000000000000000000000000000000000000000000000000000000000",
    "000000000000000000000000000000000000000000000000000000000000",
    "000000000000000000000000000000000000000000000000000000000000",
    "111111111111111111111111111111111111111111111111111111111111",
]
tile_size = 50
map_width = len(nivel[0]) * tile_size
map_height = len(nivel) * tile_size

# Crear lista de tiles (bloques sólidos)
tiles = []
for fila, linea in enumerate(nivel):
    for col, val in enumerate(linea):
        if val == "1":
            tiles.append(pygame.Rect(col * tile_size, fila * tile_size, tile_size, tile_size))


# --- BUCLE PRINCIPAL ---
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time (segundos)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # --- ENTRADAS ---
    keys = pygame.key.get_pressed()
    vel_x = 0
    if keys[pygame.K_LEFT]:
        vel_x = -200
    if keys[pygame.K_RIGHT]:
        vel_x = 200
    if keys[pygame.K_SPACE] and en_suelo:
        vel_y = -500  # salto

    # --- FÍSICAS ---
    vel_y += 1000 * dt  # gravedad
    player.x += vel_x * dt
    player.y += vel_y * dt
    en_suelo = False

    # --- COLISIONES CON EL MAPA ---
    for tile in tiles:
        if player.colliderect(tile):
            # Colisión vertical
            if vel_y > 0:  # cayendo
                player.bottom = tile.top
                vel_y = 0
                en_suelo = True
            elif vel_y < 0:  # saltando
                player.top = tile.bottom
                vel_y = 0

            # Colisión horizontal
            if vel_x > 0:
                player.right = tile.left
            elif vel_x < 0:
                player.left = tile.right

    # --- CÁMARA (centrar jugador) ---
    camera_x = player.centerx - ANCHO // 2
    camera_x = max(0, min(camera_x, map_width - ANCHO))

    # --- DIBUJAR ---
    pantalla.fill(AZUL_CIELO)

    # Dibujar tiles visibles
    for tile in tiles:
        if -tile_size < tile.x - camera_x < ANCHO:
            pygame.draw.rect(pantalla, VERDE, (tile.x - camera_x, tile.y, tile_size, tile_size))

    # Dibujar jugador
    pygame.draw.rect(pantalla, ROJO, (player.x - camera_x, player.y, player.width, player.height))

    pygame.display.flip()

pygame.quit()
