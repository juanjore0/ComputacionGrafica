import pygame
import os
from constantes import ANCHO, ALTO, FPS, BLANCO
from cargador_sprites import CargadorSprites
from menu import Menu
from introduccion import Introduccion
<<<<<<< HEAD
from niveles import GestorNiveles

=======
from gestor_niveles import GestorNiveles
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Can You Go?')
        self.clock = pygame.time.Clock()
<<<<<<< HEAD
        self.estado = 'MENU'
        
        # ✅ Variable para activar/desactivar debug
        self.debug_mode = False  # Empieza desactivado

        # Gestor de niveles
        self.gestor_niveles = GestorNiveles()
      
=======
        self.estado = 'MENU'  # Estados: MENU, INTRODUCCION, JUGANDO, NIVEL_COMPLETADO, VICTORIA
        
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
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
        print("\n═══ CARGANDO TILES ═══")
        try:
            self.tiles_dict = CargadorSprites.cargar_elementos_solidos(
                ruta_tiles, 
                escala=(95, 47)
            )
            
            if self.tiles_dict:
                print(f"✓ {len(self.tiles_dict)} tiles cargados correctamente")
            else:
<<<<<<< HEAD
                raise Exception("No se pudieron cargar los tiles")


=======
                raise Exception("No se encontró 'sprite0' en los elementos sólidos")
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
        except Exception as e:
            print(f"❌ Error cargando tiles: {e}")
            tile_default = pygame.Surface((95, 47))
            tile_default.fill((150, 110, 40))
            self.tiles_dict = {'sprite0': [tile_default]}
        
        # ✅ IMPORTANTE: Cargar objetos del juego (libros, espinas, etc.)
        print("\n═══ CARGANDO OBJETOS ═══")
        try:
            self.objetos_dict = CargadorSprites.cargar_objetos_juego(base)
            
            if self.objetos_dict:
                print(f"✓ {len(self.objetos_dict)} objetos cargados correctamente")
            else:
                raise Exception("No se pudieron cargar los objetos")
        
        except Exception as e:
            print(f"❌ Error cargando objetos: {e}")
            # Crear objetos por defecto
            libro_default = pygame.Surface((40, 40))
            libro_default.fill((255, 0, 255))
            espinas_default = pygame.Surface((95, 47))
            espinas_default.fill((255, 0, 0))
            self.objetos_dict = {
                'libro': libro_default,
                'espinas': espinas_default
            }

        # ✅ Cargar sprites de vidas
        print("\n═══ CARGANDO UI ═══")
        try:
            self.sprites_vidas = CargadorSprites.cargar_sprites_vidas(
                base, 
                escala=(140, 40) 
            )
            print(f"✓ Sprites de vidas cargados")
        except Exception as e:
            print(f"❌ Error cargando sprites de vidas: {e}")
            self.sprites_vidas = None

        
        # Cargar spritesheet del personaje
        print("\n═══ CARGANDO PERSONAJE ═══")
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
            print(f"❌ Error cargando sprite: {e}")
            self.pj_imagen = pygame.Surface((112, 112))
            self.pj_imagen.fill((0, 255, 0))
            self.animaciones = None
        
        # Inicializar gestor de niveles (se crea después)
        self.gestor_niveles = None
        
        # Crear menú e introducción
        self.menu = Menu(self.pantalla)
        self.introduccion = Introduccion(self.pantalla)
<<<<<<< HEAD


    def inicializar_nivel(self):
        """Inicializa o reinicia el nivel actual"""
        datos_nivel = self.gestor_niveles.obtener_nivel()
        
        if datos_nivel is None:
            print("ERROR: No hay más niveles disponibles")
            return
        
        self.nivel = Nivel(
            datos_nivel['mapa'],      # Primer argumento: mapa
            self.tiles_dict,          # Segundo argumento: tiles_dict
            self.objetos_dict         # Tercer argumento: objetos_dict
        )
        
        # Usar la posición de spawn del nivel
        spawn_x = datos_nivel.get('spawn_x', 100)
        spawn_y = datos_nivel.get('spawn_y', 300)
        
        self.personaje = Personaje(spawn_x, spawn_y, self.pj_imagen, self.animaciones)
        self.todas = pygame.sprite.Group(self.personaje)
        self.todas.add(self.nivel.grupo_coleccionables)
        self.todas.add(self.nivel.grupo_trampas)
        self.todas.add(self.nivel.grupo_punto_final)
        
        print(f"\n╔══════════════════════════════════════════════╗")
        print(f"║  NIVEL {self.gestor_niveles.nivel_actual + 1}/{self.gestor_niveles.total_niveles()}: {datos_nivel['nombre']:30s} ║")
        print(f"║  Spawn: ({spawn_x}, {spawn_y})                     ║")
        print(f"╚══════════════════════════════════════════════╝\n")
    
    def cargar_siguiente_nivel(self):
        """Carga el siguiente nivel si existe"""
        if self.gestor_niveles.siguiente_nivel():
            print("\n🎉 ¡NIVEL COMPLETADO! Cargando siguiente nivel...")
            self.inicializar_nivel()
            return True
        else:
            print("\n🏆 ¡FELICIDADES! ¡Has completado todos los niveles!")
            self.estado = 'MENU'
            self.gestor_niveles.reiniciar_nivel()
            return False
=======
        
        # Fuente para textos
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_grande = pygame.font.Font(None, 72)
    
    def inicializar_juego(self):
        """Inicializa el gestor de niveles y empieza desde el nivel 1"""
        self.gestor_niveles = GestorNiveles(
            tile_suelo=self.tile_suelo,
            imagen_pj=self.pj_imagen,
            animaciones_pj=self.animaciones
        )
        print("🎮 Juego inicializado correctamente")
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        resultado = self.menu.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'INTRODUCCION'
<<<<<<< HEAD
            self.gestor_niveles.reiniciar_nivel()
=======
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
            return True
        elif resultado == 'salir':
            return False
        
        return True
<<<<<<< HEAD


=======
    
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
    def mostrar_introduccion(self):
        """Muestra la introducción animada"""
        self.introduccion.activo = True
        self.introduccion.tiempo_transcurrido = 0
        self.introduccion.fade_in = 0
        
        resultado = self.introduccion.mostrar(self.clock, FPS)
        
        if resultado == 'jugar':
            self.estado = 'JUGANDO'
<<<<<<< HEAD
            self.inicializar_nivel()
=======
            self.inicializar_juego()
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
            return True
        elif resultado == 'salir':
            return False
        return True
    
    def mostrar_pantalla_nivel_completado(self):
        """Muestra una pantalla de transición entre niveles"""
        esperando = True
        tiempo_inicio = pygame.time.get_ticks()
        tiempo_minimo = 2000  # 2 segundos mínimo
        
        while esperando:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'salir'
                
                # Permitir saltar después del tiempo mínimo
                if tiempo_transcurrido > tiempo_minimo:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        esperando = False
            
            # Auto-avanzar después de 5 segundos
            if tiempo_transcurrido > 5000:
                esperando = False
            
            # Dibujar pantalla
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Título
            texto_titulo = self.fuente_grande.render("¡NIVEL COMPLETADO!", True, BLANCO)
            rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            self.pantalla.blit(texto_titulo, rect_titulo)
            
            # Estadísticas
            texto_puntos = self.fuente.render(
                f"Libros recogidos: {self.gestor_niveles.personaje.puntos // 100}", 
                True, BLANCO
            )
            rect_puntos = texto_puntos.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            self.pantalla.blit(texto_puntos, rect_puntos)
            
            texto_vidas = self.fuente.render(
                f"Vidas restantes: {self.gestor_niveles.personaje.vidas}", 
                True, BLANCO
            )
            rect_vidas = texto_vidas.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            self.pantalla.blit(texto_vidas, rect_vidas)
            
            # Instrucción
            if tiempo_transcurrido > tiempo_minimo:
                texto_continuar = self.fuente.render(
                    "Presiona cualquier tecla para continuar...", 
                    True, BLANCO
                )
                texto_continuar.set_alpha(int(abs(pygame.math.Vector2(1, 0).rotate(tiempo_transcurrido * 0.2).x) * 255))
                rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO - 100))
                self.pantalla.blit(texto_continuar, rect_continuar)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return 'continuar'
    
    def mostrar_pantalla_victoria(self):
        """Muestra la pantalla de victoria final"""
        esperando = True
        
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'salir'
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
            
            # Dibujar pantalla
            self.pantalla.blit(self.fondo, (0, 0))
            
            # Título
            texto_titulo = self.fuente_grande.render("¡VICTORIA!", True, (255, 215, 0))
            rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 80))
            self.pantalla.blit(texto_titulo, rect_titulo)
            
            # Mensaje
            texto_mensaje = self.fuente.render(
                "¡Has completado todos los niveles!", 
                True, BLANCO
            )
            rect_mensaje = texto_mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 10))
            self.pantalla.blit(texto_mensaje, rect_mensaje)
            
            # Puntos finales
            texto_puntos = self.fuente.render(
                f"Puntos totales: {self.gestor_niveles.personaje.puntos}", 
                True, BLANCO
            )
            rect_puntos = texto_puntos.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
            self.pantalla.blit(texto_puntos, rect_puntos)
            
            # Instrucción
            texto_continuar = self.fuente.render(
                "Presiona cualquier tecla para volver al menú", 
                True, BLANCO
            )
            rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO - 80))
            self.pantalla.blit(texto_continuar, rect_continuar)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return 'menu'
    
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
<<<<<<< HEAD
                    
                    # ✅ Presionar P para activar/desactivar debug
                    if event.key == pygame.K_p:
                        self.debug_mode = not self.debug_mode
                        print(f"🔍 Debug mode: {'ON ✅' if self.debug_mode else 'OFF ❌'}")

            # Lógica de GAME OVER
            if self.personaje.vidas <= 0 and not self.personaje.animacion_bloqueada:
                print("Volviendo al menú por Game Over")
                self.estado = 'MENU'
                self.menu.activo = True
                self.gestor_niveles.reiniciar_nivel()
                corriendo = False
                continue

            # Actualizar personaje
            self.personaje.update(self.nivel.plataformas)
            
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

            # ✅ Lógica de daño - ACTUALIZADA para usar hitbox
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
            
            # Verificar si llegó al punto final
            for punto_final in self.nivel.grupo_punto_final:
                if self.personaje.hitbox.colliderect(punto_final.rect):
                    if not self.cargar_siguiente_nivel():
                        corriendo = False
                        continue

            # Dibujar todo
            self.pantalla.blit(self.fondo, (0, 0))
            self.nivel.dibujar(self.pantalla, debug=self.debug_mode)
            self.todas.draw(self.pantalla)
            
            # ✅ Dibujar hitbox del personaje en modo debug
            if self.debug_mode and hasattr(self.personaje, 'hitbox'):
                pygame.draw.rect(self.pantalla, (0, 255, 255), self.personaje.hitbox, 2)  # Cian
                # Rect completo del personaje (amarillo)
                pygame.draw.rect(self.pantalla, (255, 255, 0), self.personaje.rect, 2)
            
            # HUD
            fuente = pygame.font.Font(None, 30)
            fps_texto = fuente.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.pantalla.blit(fps_texto, (10, 10))
            
            texto_puntos = fuente.render(f"Libros: {self.personaje.puntos}", True, (255, 255, 255))
            self.pantalla.blit(texto_puntos, (10, 40))
            
            # Mostrar sprite de vidas en lugar de texto
            if self.sprites_vidas:
                # Asegurar que las vidas estén entre 0 y 3
                vidas_actual = max(0, min(3, self.personaje.vidas))
                sprite_vida = self.sprites_vidas[vidas_actual]
                self.pantalla.blit(sprite_vida, (ANCHO - 140, 10))
            else:
                # Fallback a texto si no cargó la imagen
                texto_vidas = fuente.render(f"Vidas: {self.personaje.vidas}", True, (255, 255, 255))
                self.pantalla.blit(texto_vidas, (ANCHO - 150, 10))
            
            # ✅ Mostrar nivel actual - A LA IZQUIERDA de las vidas y en la misma altura
            texto_nivel = fuente.render(
                f"Nivel {self.gestor_niveles.nivel_actual + 1}/{self.gestor_niveles.total_niveles()}", 
                True, (255, 255, 255)
            )
            # Calcular posición para alinearlo a la izquierda del sprite de vidas
            pos_x_nivel = ANCHO - 160 - texto_nivel.get_width() - 10  # 10 píxeles de separación
            self.pantalla.blit(texto_nivel, (pos_x_nivel, 10))  # Misma altura que las vidas
            
            # ✅ Mostrar indicador de modo debug
            if self.debug_mode:
                debug_texto = fuente.render("DEBUG MODE [P para desactivar]", True, (255, 255, 0))
                self.pantalla.blit(debug_texto, (10, 70))
            
            pygame.display.flip()
            self.clock.tick(FPS)
=======
            
            # Obtener estado del juego
            estado_juego = self.gestor_niveles.obtener_estado_juego()
            
            # Manejar según el estado
            if estado_juego == 'game_over':
                print("🔄 Volviendo al menú por Game Over")
                self.estado = 'MENU'
                self.menu.activo = True
                corriendo = False
                continue
            
            elif estado_juego == 'nivel_completado':
                # Mostrar pantalla de nivel completado
                resultado = self.mostrar_pantalla_nivel_completado()
                
                if resultado == 'salir':
                    corriendo = False
                    continue
                
                # Intentar cargar el siguiente nivel
                if not self.gestor_niveles.siguiente_nivel():
                    # No hay más niveles, mostrar victoria
                    self.estado = 'VICTORIA'
                    resultado = self.mostrar_pantalla_victoria()
                    
                    if resultado == 'menu':
                        self.estado = 'MENU'
                        self.menu.activo = True
                        corriendo = False
                    else:
                        corriendo = False
                    continue
            
            elif estado_juego == 'jugando':
                # Actualizar
                self.gestor_niveles.actualizar()
                
                # Dibujar fondo
                self.pantalla.blit(self.fondo, (0, 0))
                
                # Dibujar nivel
                self.gestor_niveles.dibujar(self.pantalla)
                
                # HUD
                fuente = pygame.font.Font(None, 30)
                
                # FPS
                fps_texto = fuente.render(f"FPS: {int(self.clock.get_fps())}", True, BLANCO)
                self.pantalla.blit(fps_texto, (10, 10))
                
                # Nivel actual
                nivel_texto = fuente.render(
                    f"Nivel: {self.gestor_niveles.nivel_actual_numero}/3", 
                    True, BLANCO
                )
                self.pantalla.blit(nivel_texto, (10, 40))
                
                # Puntos
                texto_puntos = fuente.render(
                    f"Libros: {self.gestor_niveles.personaje.puntos // 100}", 
                    True, BLANCO
                )
                self.pantalla.blit(texto_puntos, (10, 70))
                
                # Vidas
                texto_vidas = fuente.render(
                    f"Vidas: {self.gestor_niveles.personaje.vidas}", 
                    True, BLANCO
                )
                self.pantalla.blit(texto_vidas, (ANCHO - 150, 10))
                
                pygame.display.flip()
                self.clock.tick(FPS)
>>>>>>> 7db16d33ac49fa39dd7377eddf10bf14d52ea2ed
        
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
