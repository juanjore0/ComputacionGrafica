# gestor_niveles.py
"""
Gestor de niveles del juego.
Controla la carga, transición y progreso entre niveles.
"""

import pygame
from nivel import Nivel
from personaje import Personaje
from niveles_config import CONFIG_NIVELES, TOTAL_NIVELES


class GestorNiveles:
    """Clase que maneja la carga y transición entre niveles"""
    
    def __init__(self, tile_suelo, imagen_pj, animaciones_pj):
        """
        Inicializa el gestor de niveles.
        
        Args:
            tile_suelo: Surface del tile de suelo
            imagen_pj: Surface de la imagen del personaje
            animaciones_pj: Dict con las animaciones del personaje
        """
        self.tile_suelo = tile_suelo
        self.imagen_pj = imagen_pj
        self.animaciones_pj = animaciones_pj
        
        self.nivel_actual_numero = 1
        self.nivel_actual = None
        self.personaje = None
        self.todas = None
        
        # Estados
        self.nivel_completado = False
        self.juego_terminado = False
        
        # Cargar el primer nivel
        self.cargar_nivel(self.nivel_actual_numero)
    
    def cargar_nivel(self, numero_nivel):
        """
        Carga un nivel específico.
        
        Args:
            numero_nivel: Número del nivel a cargar (1-3)
        
        Returns:
            bool: True si se cargó correctamente, False si no existe
        """
        print(f"\n{'='*50}")
        print(f"CARGANDO NIVEL {numero_nivel}")
        print(f"{'='*50}")
        
        # Obtener configuración del nivel
        config = CONFIG_NIVELES.get(numero_nivel)
        
        if not config:
            print(f"Error: No existe el nivel {numero_nivel}")
            return False
        
        # Resetear estados
        self.nivel_completado = False
        self.nivel_actual_numero = numero_nivel
        
        # Mostrar información del nivel
        print(f"Nombre: {config['nombre']}")
        print(f"Libros: {len(config['libros'])}")
        print(f"Trampas: {len(config['trampas'])}")
        
        # Crear el nivel
        self.nivel_actual = Nivel(
            mapa=config['mapa'],
            tile_suelo=self.tile_suelo,
            libros_cfg=config['libros'],
            trampas_cfg=config['trampas'],
            punto_final_cfg=config['punto_final']
        )
        
        # Calcular posición inicial del personaje
        pj_x, pj_y = config['pj_pos']
        tile_alto = self.tile_suelo.get_height()
        
        # Ajustar Y si es 0 (poner en una posición segura)
        if pj_y == 0:
            pj_y = 2 * tile_alto
        
        # Crear el personaje
        self.personaje = Personaje(pj_x, pj_y, self.imagen_pj, self.animaciones_pj)
        
        # Crear grupo de sprites
        self.todas = pygame.sprite.Group(self.personaje)
        self.todas.add(self.nivel_actual.grupo_coleccionables)
        self.todas.add(self.nivel_actual.grupo_trampas)
        
        if self.nivel_actual.punto_final:
            self.todas.add(self.nivel_actual.punto_final)
        
        print(f"✅ Nivel {numero_nivel} cargado correctamente")
        print(f"   Personaje en: ({self.personaje.rect.x}, {self.personaje.rect.y})")
        print(f"{'='*50}\n")
        
        return True
    
    def siguiente_nivel(self):
        """Carga el siguiente nivel o termina el juego si era el último"""
        siguiente = self.nivel_actual_numero + 1
        
        if siguiente > TOTAL_NIVELES:
            print("\n🎉 ¡FELICIDADES! ¡HAS COMPLETADO TODOS LOS NIVELES! 🎉\n")
            self.juego_terminado = True
            return False
        else:
            return self.cargar_nivel(siguiente)
    
    def reiniciar_nivel(self):
        """Reinicia el nivel actual"""
        return self.cargar_nivel(self.nivel_actual_numero)
    
    def verificar_completado(self):
        """
        Verifica si el nivel ha sido completado.
        
        Returns:
            bool: True si el personaje llegó al punto final
        """
        if self.nivel_actual.punto_final and not self.nivel_completado:
            if self.personaje.hitbox.colliderect(self.nivel_actual.punto_final.rect):
                self.nivel_completado = True
                print(f"\n¡NIVEL {self.nivel_actual_numero} COMPLETADO! ✨")
                print(f"libros recogidos: {self.personaje.puntos // 100}")
                print(f"vidas restantes: {self.personaje.vidas}\n")
                return True
        return False
    
    def actualizar(self):
        """Actualiza el estado del nivel actual"""
        # Actualizar personaje
        self.personaje.update(self.nivel_actual.plataformas)
        
        # Verificar colecciones de libros
        libros_recogidos = []
        for libro in self.nivel_actual.grupo_coleccionables:
            if self.personaje.hitbox.colliderect(libro.rect):
                self.personaje.puntos += libro.valor
                libros_recogidos.append(libro)
                print(f"¡Libro recogido! Puntos: {self.personaje.puntos}")
        
        if libros_recogidos:
            self.nivel_actual.grupo_coleccionables.remove(libros_recogidos)
            self.todas.remove(libros_recogidos)
        
        # Verificar daño de trampas
        if not self.personaje.invencible:
            for trampa in self.nivel_actual.grupo_trampas:
                if self.personaje.hitbox.colliderect(trampa.rect):
                    self.personaje.recibir_daño(1)
                    break  # Solo una trampa por frame
        
        # Verificar si completó el nivel
        self.verificar_completado()
    
    def dibujar(self, pantalla):
        """Dibuja el nivel actual y todos sus elementos"""
        self.nivel_actual.dibujar(pantalla)
        self.todas.draw(pantalla)
    
    def obtener_estado_juego(self):
        """
        Devuelve el estado actual del juego.
        
        Returns:
            str: 'jugando', 'nivel_completado', 'game_over', 'juego_terminado'
        """
        if self.juego_terminado:
            return 'juego_terminado'
        elif self.personaje.vidas <= 0 and not self.personaje.animacion_bloqueada:
            return 'game_over'
        elif self.nivel_completado:
            return 'nivel_completado'
        else:
            return 'jugando'