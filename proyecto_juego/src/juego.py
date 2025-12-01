import pygame
import os
from constantes import ANCHO, ALTO, FPS
from nivel import Nivel
from personaje import Personaje
from cargador_sprites import CargadorSprites
from menu import Menu
from introduccion import Introduccion
from gestor_niveles import GestorNiveles

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Can You Go?')
        self.clock = pygame.time.Clock()
        self.estado = 'MENU'
        
        # Variable para activar/desactivar debug
        self.debug_mode = False  # Empieza desactivado

        #  VIDAS GLOBALES (se mantienen entre niveles)
        self.vidas_globales = 3

        # Gestor de niveles
        self.gestor_niveles = GestorNiveles()
      
        # Rutas
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_fondo = os.path.join(base, 'assets', 'images', 'backgrounds', 'Background.png')
        ruta_tiles = os.path.join(base, 'assets', 'images', 'tiles', 'tiles.png')
        ruta_personaje = os.path.join(base, 'assets', 'images', 'player', 'player.png')
        
        # Fondo
        try:
            self.fondo = pygame.image.load(ruta_fondo).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except Exception:
            self.fondo = pygame.Surface((ANCHO, ALTO))
            self.fondo.fill((40, 70, 120))
        
        # Cargar TODOS los tiles
        print("\n╔══ CARGANDO TILES ══╗")
        try:
            self.tiles_dict = CargadorSprites.cargar_elementos_solidos(
                ruta_tiles, 
                escala=(95, 47)
            )
            
            if self.tiles_dict:
                print(f"✓ {len(self.tiles_dict)} tiles cargados correctamente")
            else:
                raise Exception("No se pudieron cargar los tiles")


        except Exception as e:
            print(f"✗ Error cargando tiles: {e}")
            tile_default = pygame.Surface((95, 47))
            tile_default.fill((150, 110, 40))
            self.tiles_dict = {'sprite0': [tile_default]}
        
        print("\n╔══ CARGANDO OBJETOS ══╗")
        try:
            self.objetos_dict = CargadorSprites.cargar_objetos_juego(base)
            
            if self.objetos_dict:
                print(f"✓ {len(self.objetos_dict)} objetos cargados correctamente")
            else:
                raise Exception("No se pudieron cargar los objetos")
        
        except Exception as e:
            print(f"✗ Error cargando objetos: {e}")
            # Crear objetos por defecto
            libro_default = pygame.Surface((40, 40))
            libro_default.fill((255, 0, 255))
            espinas_default = pygame.Surface((95, 47))
            espinas_default.fill((255, 0, 0))
            self.objetos_dict = {
                'libro': libro_default,
                'espinas': espinas_default
            }

        # Cargar sprites de vidas
        print("\n╔══ CARGANDO UI ══╗")
        try:
            self.sprites_vidas = CargadorSprites.cargar_sprites_vidas(
                base, 
                escala=(140, 40) 
            )
            print(f"✓ Sprites de vidas cargados")
        except Exception as e:
            print(f"✗ Error cargando sprites de vidas: {e}")
            self.sprites_vidas = None

        # Cargar cartel indicador
        print("\n╔══ CARGANDO CARTEL INDICADOR ══╗")
        try:
            self.sprites_cartel = CargadorSprites.cargar_cartel_nivel(
                base,
                escala=(60, 56)  # Escalado para que se vea bien
            )
            print(f"✓ Cartel indicador cargado")
        except Exception as e:
            print(f"✗ Error cargando cartel: {e}")
            self.sprites_cartel = None

    
        # Cargar spritesheet del personaje
        print("\n╔══ CARGANDO PERSONAJE ══╗")
        try:
            self.animaciones = CargadorSprites.cargar_animaciones_jugador(
                ruta_personaje, 
                escala=(112, 112)
            )
            
            if self.animaciones:
                self.pj_imagen = self.animaciones['idle'][0]
                print("✓ Animaciones cargadas correctamente")
            else:
                raise Exception("No se pudieron cargar las animaciones")
                
        except Exception as e:
            print(f"✗ Error cargando sprite: {e}")
            self.pj_imagen = pygame.Surface((112, 112))
            self.pj_imagen.fill((0, 255, 0))
            self.animaciones = None
        
        # Inicializar nivel y personaje
        self.inicializar_nivel()
        
        # Crear menú
        self.menu = Menu(self.pantalla)
        self.introduccion = Introduccion(self.pantalla)


    def inicializar_nivel(self, restaurar_vidas=False):
        """Inicializa o reinicia el nivel actual"""
        datos_nivel = self.gestor_niveles.obtener_nivel()
        
        if datos_nivel is None:
            print("ERROR: No hay más niveles disponibles")
            return
        
        self.nivel = Nivel(
            datos_nivel['mapa'],      # Primer argumento: mapa
            self.tiles_dict,          # Segundo argumento: tiles_dict
            self.objetos_dict,         # Tercer argumento: objetos_dict
            self.sprites_cartel     # Cuarto argumento: sprites_cartel
        )
        
        # Usar la posición de spawn del nivel
        spawn_x = datos_nivel.get('spawn_x', 100)
        spawn_y = datos_nivel.get('spawn_y', 300)
        
        # Guardar posición de spawn para respawn
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        
        self.personaje = Personaje(spawn_x, spawn_y, self.pj_imagen, self.animaciones)
        
        # Asignar vidas globales al personaje
        if restaurar_vidas:
            self.vidas_globales = 3  # Restaurar vidas al inicio del juego
        self.personaje.vidas = self.vidas_globales
        
        self.todas = pygame.sprite.Group(self.personaje)
        self.todas.add(self.nivel.grupo_coleccionables)
        self.todas.add(self.nivel.grupo_trampas)
        self.todas.add(self.nivel.grupo_punto_final)
        
        print(f"\n╔═══════════════════════════════════════════════╗")
        print(f"║  NIVEL {self.gestor_niveles.nivel_actual + 1}/{self.gestor_niveles.total_niveles()}: {datos_nivel['nombre']:30s} ║")
        print(f"║  Spawn: ({spawn_x}, {spawn_y})                     ║")
        print(f"║  Vidas: {self.vidas_globales}/3                              ║")
        print(f"╚═══════════════════════════════════════════════╝\n")
    
    def respawn_personaje(self):
        """Reaparece el personaje en el punto de inicio del nivel"""
        print(f"💀 ¡Respawneando! Vidas restantes: {self.vidas_globales}")
        
        # Restaurar posición
        self.personaje.rect.x = self.spawn_x
        self.personaje.rect.y = self.spawn_y
        self.personaje.actualizar_hitbox()
        
        # Resetear física
        self.personaje.vel_x = 0
        self.personaje.vel_y = 0
        self.personaje.en_suelo = False
        
        # Resetear animación
        self.personaje.animacion_actual = 'idle'
        self.personaje.frame_actual = 0
        self.personaje.animacion_bloqueada = False
        
        # Dar invencibilidad temporal
        self.personaje.invencible = True
        self.personaje.tiempo_invencible = pygame.time.get_ticks()
    
    def cargar_siguiente_nivel(self):
        """Carga el siguiente nivel si existe"""
        if self.gestor_niveles.siguiente_nivel():
            print("\n🎉 ¡NIVEL COMPLETADO! Cargando siguiente nivel...")
            # Mantener vidas al pasar de nivel
            self.vidas_globales = self.personaje.vidas
            self.inicializar_nivel()
            return True
        else:
            print("\n🏆 ¡FELICIDADES! ¡Has completado todos los niveles!")
            self.estado = 'MENU'
            self.gestor_niveles.reiniciar_nivel()
            self.vidas_globales = 3  # Restaurar vidas para la próxima partida
            return False
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        resultado = self.menu.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'INTRODUCCION'
            self.gestor_niveles.reiniciar_nivel()
            self.vidas_globales = 3  # Reiniciar vidas al empezar nueva partida
            return True
        elif resultado == 'salir':
            return False
        
        return True


    def mostrar_introduccion(self):
        """Muestra la introducción animada"""
        self.introduccion.activo = True
        self.introduccion.tiempo_transcurrido = 0
        self.introduccion.fade_in = 0
        
        resultado = self.introduccion.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'JUGANDO'
            self.inicializar_nivel(restaurar_vidas=True)  # Restaurar vidas al empezar
            return True
        elif resultado == 'salir':
            return False
        return True

    def bucle_juego(self):
        """Bucle principal del juego"""
        corriendo = True
        
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.estado = 'MENU'
                        self.menu.activo = True
                        resultado = self.mostrar_menu()
                        if not resultado:
                            corriendo = False
                    
                    # Presionar P para activar/desactivar debug
                    if event.key == pygame.K_p:
                        self.debug_mode = not self.debug_mode
                        print(f"🔍 Debug mode: {'ON ' if self.debug_mode else 'OFF ✗'}")

            # SOLO UNA LLAMADA A UPDATE
            self.personaje.update(self.nivel.plataformas)
            
            # Detectar caída al vacío DESPUÉS de update
            if self.personaje.rect.top > ALTO:
                self.vidas_globales -= 1
                self.personaje.vidas = self.vidas_globales
                
                print(f"💀 ¡Caída al vacío! Vidas restantes: {self.vidas_globales}")
                
                if self.vidas_globales > 0:
                    self.respawn_personaje()
                else:
                    print("💀 GAME OVER - Sin vidas")
                    self.estado = 'MENU'
                    self.menu.activo = True
                    self.gestor_niveles.reiniciar_nivel()
                    self.vidas_globales = 3
                    corriendo = False
                    continue

            # Lógica de GAME OVER por animación de muerte
            if self.personaje.vidas <= 0 and not self.personaje.animacion_bloqueada:
                print("Volviendo al menú por Game Over")
                self.estado = 'MENU'
                self.menu.activo = True
                self.gestor_niveles.reiniciar_nivel()
                self.vidas_globales = 3
                corriendo = False
                continue
            
            # Lógica de colección de libros
            libros_recogidos = []
            for libro in self.nivel.grupo_coleccionables:
                if self.personaje.hitbox.colliderect(libro.rect):
                    self.personaje.puntos += libro.valor
                    libros_recogidos.append(libro)
                    print(f"¡Libro recogido! Puntos: {self.personaje.puntos}")
            
            if libros_recogidos:
                self.nivel.grupo_coleccionables.remove(libros_recogidos)
                self.todas.remove(libros_recogidos)
                
                # Verificar si se recogieron todos los libros
                if len(self.nivel.grupo_coleccionables) == 0:
                    if not self.nivel.cartel_encendido:  # Solo mostrar mensaje la primera vez
                        self.nivel.cartel_encendido = True
                        print("🎉 ¡Todos los libros recogidos! El cartel se ha encendido.")

            #  Lógica de daño - ACTUALIZADA para usar hitbox
            if not self.personaje.invencible:
                colisiones_trampas = []
                for trampa in self.nivel.grupo_trampas:
                    # Usar hitbox si existe, sino usar rect
                    if hasattr(trampa, 'hitbox'):
                        if self.personaje.hitbox.colliderect(trampa.hitbox):
                            colisiones_trampas.append(trampa)
                    else:
                        if self.personaje.hitbox.colliderect(trampa.rect):
                            colisiones_trampas.append(trampa)
                
                if colisiones_trampas:
                    self.personaje.recibir_daño(1)
                    #  Actualizar vidas globales cuando recibe daño
                    self.vidas_globales = self.personaje.vidas
            
            #  Verificar si llegó al punto final Y tiene todos los libros
            for punto_final in self.nivel.grupo_punto_final:
                if self.personaje.hitbox.colliderect(punto_final.rect):
                    if self.nivel.cartel_encendido:  # Solo pasar si recogió todos los libros
                        if not self.cargar_siguiente_nivel():
                            corriendo = False
                            continue
                    else:
                        # Mostrar mensaje de que faltan libros (solo una vez por contacto)
                        if not hasattr(self, '_mostro_mensaje_libros'):
                            self._mostro_mensaje_libros = True
                            libros_faltantes = len(self.nivel.grupo_coleccionables)
                            print(f"⚠️ ¡Recoge todos los libros antes de pasar! Faltan: {libros_faltantes}")
            
            # Resetear flag de mensaje cuando no está tocando el punto final
            if not any(self.personaje.hitbox.colliderect(pf.rect) for pf in self.nivel.grupo_punto_final):
                if hasattr(self, '_mostro_mensaje_libros'):
                    delattr(self, '_mostro_mensaje_libros')

            # Dibujar todo
            self.pantalla.blit(self.fondo, (0, 0))
            self.nivel.dibujar(self.pantalla, debug=self.debug_mode)
            self.todas.draw(self.pantalla)
            
            #  Dibujar hitbox del personaje en modo debug
            if self.debug_mode and hasattr(self.personaje, 'hitbox'):
                pygame.draw.rect(self.pantalla, (0, 255, 255), self.personaje.hitbox, 2)  # Cian
                # Rect completo del personaje (amarillo)
                pygame.draw.rect(self.pantalla, (255, 255, 0), self.personaje.rect, 2)
            
            # HUD
            fuente = pygame.font.Font(None, 30)
            fps_texto = fuente.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.pantalla.blit(fps_texto, (10, 10))
            
            #  Mostrar libros restantes en lugar de puntos totales
            libros_recogidos_total = self.nivel.total_libros - len(self.nivel.grupo_coleccionables)
            texto_libros = fuente.render(f"Libros: {libros_recogidos_total}/{self.nivel.total_libros}", True, (255, 255, 255))
            self.pantalla.blit(texto_libros, (10, 40))
            
            #  Mostrar sprite de vidas GLOBALES
            if self.sprites_vidas:
                vidas_actual = max(0, min(3, self.vidas_globales))
                sprite_vida = self.sprites_vidas[vidas_actual]
                self.pantalla.blit(sprite_vida, (ANCHO - 140, 10))
            else:
                texto_vidas = fuente.render(f"Vidas: {self.vidas_globales}", True, (255, 255, 255))
                self.pantalla.blit(texto_vidas, (ANCHO - 150, 10))
            
            # Mostrar nivel actual
            texto_nivel = fuente.render(
                f"Nivel {self.gestor_niveles.nivel_actual + 1}/{self.gestor_niveles.total_niveles()}", 
                True, (255, 255, 255)
            )
            pos_x_nivel = ANCHO - 160 - texto_nivel.get_width() - 10
            self.pantalla.blit(texto_nivel, (pos_x_nivel, 10))
            
            # Mostrar debug mode activado
            if self.debug_mode:
                debug_texto = fuente.render("DEBUG MODE [P para desactivar]", True, (255, 255, 0))
                self.pantalla.blit(debug_texto, (10, 70))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return False


    def ejecutar(self):
        """Método principal que controla el flujo del juego"""
        corriendo = True
        
        while corriendo:
            if self.estado == 'MENU':
                corriendo = self.mostrar_menu()
            elif self.estado == 'INTRODUCCION':
                corriendo = self.mostrar_introduccion()
            elif self.estado == 'JUGANDO':
                corriendo = self.bucle_juego()
        
        pygame.quit()