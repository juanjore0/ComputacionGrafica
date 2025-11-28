"""
Gestor de niveles del juego
Cada nivel es un array donde:
0 = Vacío
1 = Plataforma
2 = Libro (coleccionable)
3 = Espinas (trampa)
4 = Punto final
"""

class GestorNiveles:
    """Clase para gestionar todos los niveles del juego"""
    
    def __init__(self):
        self.nivel_actual = 0
        self.niveles = self.cargar_niveles()
    
    def cargar_niveles(self):
        """Carga todos los niveles del juego"""
        return [
            self.nivel_1(),
            self.nivel_2(),
            self.nivel_3(),
            # Agrega más niveles aquí
        ]
    
    def nivel_1(self):
        """Tutorial - Nivel simple sin trampas"""
        return {
            'nombre': 'Tutorial',
            'mapa': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 5, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 5, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 4, 0],
                [1, 1, 1, 1, 1, 1, 0, 1, 1],
            ],
            'spawn_x': 100,
            'spawn_y': 300
        }
    
    def nivel_2(self):
        """Primeras trampas - Introducción a las espinas"""
        return {
            'nombre': 'Cuidado con las Espinas',
            'mapa': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 0, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'spawn_x': 100,
            'spawn_y': 300
        }
    
    def nivel_3(self):
        """Desafío - Nivel más complejo"""
        return {
            'nombre': 'El Desafío',
            'mapa': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0],
                [0, 0, 0, 3, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'spawn_x': 100,
            'spawn_y': 300
        }
    
    def obtener_nivel(self, indice=None):
        """Obtiene un nivel específico o el nivel actual"""
        if indice is None:
            indice = self.nivel_actual
        
        if 0 <= indice < len(self.niveles):
            return self.niveles[indice]
        return None
    
    def siguiente_nivel(self):
        """Avanza al siguiente nivel"""
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1
            return True
        return False
    
    def reiniciar_nivel(self):
        """Reinicia al primer nivel"""
        self.nivel_actual = 0
    
    def hay_mas_niveles(self):
        """Verifica si hay más niveles disponibles"""
        return self.nivel_actual < len(self.niveles) - 1
    
    def total_niveles(self):
        """Retorna el número total de niveles"""
        return len(self.niveles)