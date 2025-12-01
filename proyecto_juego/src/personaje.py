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
        self.fuerza_salto = -14
        self.velocidad = 4  # 
        self.en_suelo = False
        

        # Inventario y puntos
        self.puntos = 0 

        # ---Vidas, Puntos e Invencibilidad ---
        self.vidas = 3
        self.invencible = False
        self.tiempo_invencible = 0
        self.duracion_invencibilidad = 1200 # 1.2 segundos en milisegundos

        # Control de estados
        self.atacando = False
        self.agachado = False
        self.usando_escudo = False
        
        # Forzar actualización inicial de la animación
        if self.animaciones:
            self.actualizar_animacion()

     # ---Método para Recibir Daño ---       
    def recibir_daño(self, cantidad):
        # Solo recibe daño si NO está invencible y no está muerto
        if not self.invencible and self.vidas > 0:
            self.vidas -= cantidad
            self.invencible = True
            self.tiempo_invencible = pygame.time.get_ticks() # Momento actual
            print(f"¡AUCH! Vidas restantes: {self.vidas}")
            
            # Activar animación de "herido" (si la tienes)
            if 'hurt' in self.animaciones:
                self.animacion_actual = 'hurt'
                self.animacion_bloqueada = True
                self.frame_actual = 0
            
            if self.vidas <= 0:
                print("¡HAS PERDIDO!")
                # Activar animación de "muerte" (si la tienes)
                if 'death' in self.animaciones:
                    self.animacion_actual = 'death'
                    self.animacion_bloqueada = True
                    self.frame_actual = 0
                else:
                    self.animacion_bloqueada = False # Si no hay anim, que no se bloquee


    def update(self, plataformas):
        # Controles
        if self.animacion_actual == 'death':
            self.actualizar_animacion()
            return # No permitir más acciones

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
        
        #  SOLO HORIZONTALES (no resetear Y)
        if self.rect.left < 0:
            self.rect.left = 0
            self.actualizar_hitbox()
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.actualizar_hitbox()
    
        
        # Actualizar animación
        self.actualizar_animacion()

        #Lógica de Invencibilidad y Parpadeo (al final de update) ---
        if self.invencible:
            ahora = pygame.time.get_ticks()
            
            # Efecto de parpadeo (solo si está vivo)
            if self.vidas > 0:
                if (ahora // 100) % 2 == 0:
                    self.image.set_alpha(100) # Semitransparente
                else:
                    self.image.set_alpha(255) # Visible
                
            # Comprobar si se acabó el tiempo de invencibilidad
            if ahora - self.tiempo_invencible > self.duracion_invencibilidad:
                self.invencible = False
                self.image.set_alpha(255) # Asegurarse de que sea visible
        else:
            # Asegurarse de que es visible si no está invencible
            self.image.set_alpha(255) 

    
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
        if self.animaciones is None: return
        
        if self.animacion_actual not in self.animaciones:
            self.animacion_actual = 'idle'
        
        frames_disponibles = len(self.animaciones[self.animacion_actual])
        if self.frame_actual >= frames_disponibles:
            self.frame_actual = 0
        
        
        # 1. Definir qué animaciones se quedan en el último frame
        # ¡HEMOS QUITADO 'death' DE ESTA LISTA!
        animaciones_estaticas = ['crouch', 'shield'] 
        
        # 2. Avanzar el frame
        self.contador_frames += 1
        if self.contador_frames >= self.velocidad_animacion:
            self.contador_frames = 0
            
            # Comprobar si es una animación está tica Y está en el último frame
            if self.animacion_actual in animaciones_estaticas and self.frame_actual == frames_disponibles - 1:
                pass # No hacer nada, quedarse en el último frame
            else:
                self.frame_actual += 1 # Avanzar al siguiente frame
        
        # 3. Comprobar si la animación ha terminado
        if self.frame_actual >= frames_disponibles:
            
            if self.animacion_actual == 'attack':
                self.atacando = False
                self.animacion_bloqueada = False
                self.animacion_actual = 'idle'
                self.frame_actual = 0
                
            elif self.animacion_actual == 'hurt':
                self.animacion_bloqueada = False
                self.animacion_actual = 'idle'
                self.frame_actual = 0
                
            # --- ESTA ES LA NUEVA LÓGICA ---
            elif self.animacion_actual == 'death':
                self.frame_actual = frames_disponibles - 1 # Quedarse en el último frame...
                self.animacion_bloqueada = False # ...PERO AVISAR QUE LA ANIMACIÓN TERMINÓ
                
            elif self.animacion_actual in animaciones_estaticas:
                self.frame_actual = frames_disponibles - 1 # Quedarse en el último frame
                
            else: # Para animaciones en bucle (idle, run)
                self.frame_actual = 0
        
        # (El resto de la función se queda igual)
        sprite = self.animaciones[self.animacion_actual][self.frame_actual]
        
        if not self.mirando_derecha:
            sprite = pygame.transform.flip(sprite, True, False)
        
        pos_anterior = self.rect.center
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.center = pos_anterior
        self.actualizar_hitbox()