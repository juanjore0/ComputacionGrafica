import pygame
from constantes import ANCHO, ALTO

class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, animaciones=None):
        super().__init__()
        
        # Animaciones
        self.animaciones = animaciones
        self.animacion_actual = 'idle'
        self.frame_actual = 0
        self.contador_frames = 0
        self.velocidad_animacion = 8
        self.mirando_derecha = True
        self.animacion_bloqueada = False
        
        # Configurar imagen inicial
        if animaciones and 'idle' in animaciones:
            self.image = animaciones['idle'][0].copy()
        else:
            self.image = imagen if imagen else pygame.Surface((112, 112))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # HITBOX CORREGIDA
        hitbox_ancho = 50
        hitbox_alto = 65
        
        self.hitbox_offset_x = (self.rect.width - hitbox_ancho) // 2
        self.hitbox_offset_y = self.rect.height - hitbox_alto
        
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            hitbox_ancho,
            hitbox_alto
        )
        
        # Física
        self.vel_x = 0
        self.vel_y = 0
        self.gravedad = 0.8
        self.fuerza_salto = -15
        self.velocidad = 5
        self.en_suelo = False
        

        # Inventario y puntos
        self.puntos = 0 
        
        # Control de estados
        self.atacando = False
        self.agachado = False
        self.usando_escudo = False
        
        # Forzar actualización inicial de la animación
        if self.animaciones:
            self.actualizar_animacion()
        
    def update(self, plataformas):
        # Controles
        teclas = pygame.key.get_pressed()
        self.vel_x = 0
        
        # Guardar animación anterior
        animacion_anterior = self.animacion_actual
        
        # No permitir movimiento si está en animación bloqueada
        if not self.animacion_bloqueada:
            # Agacharse (tecla S o Flecha Abajo)
            if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                self.animacion_actual = 'crouch'
                self.agachado = True
            # Escudo (tecla x)
            elif teclas[pygame.K_x]:
                self.animacion_actual = 'shield'
                self.usando_escudo = True
            # Atacar (tecla Z)
            elif teclas[pygame.K_z]:
                if not self.atacando:
                    self.animacion_actual = 'attack'
                    self.atacando = True
                    self.animacion_bloqueada = True
            # Movimiento horizontal
            elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.vel_x = -self.velocidad
                if self.en_suelo:
                    self.animacion_actual = 'run'
                self.mirando_derecha = False
                self.agachado = False
                self.usando_escudo = False
            elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.vel_x = self.velocidad
                if self.en_suelo:
                    self.animacion_actual = 'run'
                self.mirando_derecha = True
                self.agachado = False
                self.usando_escudo = False
            else:
                if self.en_suelo:
                    self.animacion_actual = 'idle'
                self.agachado = False
                self.usando_escudo = False
            
            # Saltar (Espacio, W o Flecha Arriba)
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo:
                self.vel_y = self.fuerza_salto
                self.en_suelo = False
                self.agachado = False
                self.usando_escudo = False
        
        # Animaciones de salto/caída (tienen prioridad sobre otras)
        if not self.en_suelo and not self.animacion_bloqueada:
            if self.vel_y < 0:  # Subiendo
                self.animacion_actual = 'jump_up'
            else:  # Cayendo
                self.animacion_actual = 'jump_down'
        
        # Si cambió la animación, reiniciar el frame
        if animacion_anterior != self.animacion_actual:
            self.frame_actual = 0
            self.contador_frames = 0
        
        # Aplicar gravedad
        self.vel_y += self.gravedad
        if self.vel_y > 20:
            self.vel_y = 20
        
        # ===== MOVIMIENTO MEJORADO CON COLISIONES SUAVIZADAS =====
        
        # Mover horizontalmente y verificar colisiones
        self.rect.x += self.vel_x
        self.actualizar_hitbox()
        self.colision_horizontal(plataformas)
        
        # Mover verticalmente y verificar colisiones
        self.rect.y += self.vel_y
        self.actualizar_hitbox()
        self.en_suelo = False
        self.colision_vertical(plataformas)
        
        # Límites de pantalla
        if self.rect.left < 0:
            self.rect.left = 0
            self.actualizar_hitbox()
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.actualizar_hitbox()
        if self.rect.top > ALTO:
            self.rect.y = 0
            self.vel_y = 0
            self.actualizar_hitbox()
        
        # Actualizar animación
        self.actualizar_animacion()
    
    def actualizar_hitbox(self):
        """Actualiza la posición de la hitbox para que siga al sprite"""
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y
    
    def colision_horizontal(self, plataformas):
        """Maneja colisiones horizontales de forma suavizada"""
        for plataforma in plataformas:
            if self.hitbox.colliderect(plataforma):
                if self.vel_x > 0:  # Moviendo a la derecha
                    # Ajustar para que la hitbox quede justo al lado de la plataforma
                    self.hitbox.right = plataforma.left
                    # Actualizar rect basándose en la nueva posición de hitbox
                    self.rect.x = self.hitbox.x - self.hitbox_offset_x
                    self.vel_x = 0  # Detener movimiento horizontal
                    
                elif self.vel_x < 0:  # Moviendo a la izquierda
                    # Ajustar para que la hitbox quede justo al lado de la plataforma
                    self.hitbox.left = plataforma.right
                    # Actualizar rect basándose en la nueva posición de hitbox
                    self.rect.x = self.hitbox.x - self.hitbox_offset_x
                    self.vel_x = 0  # Detener movimiento horizontal
    
    def colision_vertical(self, plataformas):
        """Maneja colisiones verticales"""
        for plataforma in plataformas:
            if self.hitbox.colliderect(plataforma):
                if self.vel_y > 0:  # Cayendo
                    # Ajustar para que la hitbox quede justo encima de la plataforma
                    self.hitbox.bottom = plataforma.top
                    # Actualizar rect basándose en la nueva posición de hitbox
                    self.rect.y = self.hitbox.y - self.hitbox_offset_y
                    self.vel_y = 0
                    self.en_suelo = True
                    
                elif self.vel_y < 0:  # Saltando (golpea desde abajo)
                    # Ajustar para que la hitbox quede justo debajo de la plataforma
                    self.hitbox.top = plataforma.bottom
                    # Actualizar rect basándose en la nueva posición de hitbox
                    self.rect.y = self.hitbox.y - self.hitbox_offset_y
                    self.vel_y = 0
    
    def actualizar_animacion(self):
        if self.animaciones is None:
            return
        
        # Verificar que la animación actual existe
        if self.animacion_actual not in self.animaciones:
            self.animacion_actual = 'idle'
        
        # Verificar que el frame actual es válido
        frames_disponibles = len(self.animaciones[self.animacion_actual])
        if self.frame_actual >= frames_disponibles:
            self.frame_actual = 0
        
        # Para animaciones que deben quedarse en el último frame
        animaciones_estaticas = ['crouch', 'shield', 'death']
        
        # Si es una animación estática y ya llegó al último frame, no avanzar
        if self.animacion_actual in animaciones_estaticas and self.frame_actual == frames_disponibles - 1:
            pass
        else:
            # Incrementar contador de frames
            self.contador_frames += 1
            
            # Cambiar al siguiente frame si es tiempo
            if self.contador_frames >= self.velocidad_animacion:
                self.contador_frames = 0
                self.frame_actual += 1
                
                # Verificar si llegamos al final de la animación
                if self.frame_actual >= frames_disponibles:
                    
                    # Desbloquear animaciones que solo se ejecutan una vez
                    if self.animacion_actual == 'attack':
                        self.atacando = False
                        self.animacion_bloqueada = False
                        self.animacion_actual = 'idle'
                        self.frame_actual = 0
                    elif self.animacion_actual in animaciones_estaticas:
                        self.frame_actual = frames_disponibles - 1
                    elif self.animacion_actual == 'hurt':
                        self.animacion_bloqueada = False
                        self.animacion_actual = 'idle'
                        self.frame_actual = 0
                    else:
                        self.frame_actual = 0
        
        # Obtener el sprite actual
        sprite = self.animaciones[self.animacion_actual][self.frame_actual]
        
        # Voltear el sprite si mira a la izquierda
        if not self.mirando_derecha:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Actualizar imagen manteniendo la posición
        pos_anterior = self.rect.center
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.center = pos_anterior
        self.actualizar_hitbox()