# niveles_config.py
"""
Configuración de todos los niveles del juego.
Cada nivel define: mapa, posición inicial del jugador, libros, trampas y punto final.
"""

# ================ NIVEL 1: TUTORIAL ================
# Nivel sencillo para aprender los controles
MAPA_NIVEL_1 = [
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1],
    [0,0,1,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1],
    [0,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
]

# ================ NIVEL 2: DESAFÍO MEDIO ================
# Más plataformas, más huecos, más trampas
MAPA_NIVEL_2 = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1],
    [0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
]

# ================ NIVEL 3: DESAFÍO DIFÍCIL ================
# Nivel más complejo con saltos precisos
MAPA_NIVEL_3 = [
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1],
]

# ================ CONFIGURACIÓN DE NIVELES ================
CONFIG_NIVELES = {
    1: {
        "nombre": "Nivel 1: El Comienzo",
        "mapa": MAPA_NIVEL_1,
        "pj_pos": (100, 0),  # Posición inicial del jugador (x, y)
        
        # Libros coleccionables: (x, y, tipo)
        "libros": [
            (200, 330, "libro"),   # Libro en plataforma media
            (400, 180, "libro"),   # Libro en plataforma alta
            (600, 450, "libro"),   # Libro en zona baja
        ],
        
        # Trampas: (x, y, tipo)
        "trampas": [
            (285, 518, "espinas"),  # Trampa en el suelo
        ],
        
        # Punto final: (x, y, ancho, alto)
        "punto_final": (750, 350, 50, 100),
    },
    
    2: {
        "nombre": "Nivel 2: El Ascenso",
        "mapa": MAPA_NIVEL_2,
        "pj_pos": (50, 0),
        
        "libros": [
            (150, 150, "libro"),   # Libro en primera plataforma
            (300, 330, "libro"),   # Libro flotante
            (500, 250, "libro"),   # Libro en plataforma media
            (650, 80, "libro"),    # Libro en zona alta
            (400, 470, "libro"),   # Libro en zona baja
        ],
        
        "trampas": [
            #(95, 330, "espinas"),   # Trampa en plataforma 1
            (285, 330, "espinas"),  # Trampa en plataforma 2
            (475, 518, "espinas"),  # Trampa en el suelo
           # (665, 518, "espinas"),  # Trampa en el suelo 2
        ],
        
        "punto_final": (750, 470, 50, 100),
    },
    
    3: {
        "nombre": "Nivel 3: La Prueba Final",
        "mapa": MAPA_NIVEL_3,
        "pj_pos": (50, 0),
        
        "libros": [
            (100, 200, "libro"),   # Libro en plataforma izquierda
            (350, 300, "libro"),   # Libro en plataforma central
            (600, 150, "libro"),   # Libro en plataforma derecha alta
            (300, 450, "libro"),   # Libro en zona media-baja
            (650, 470, "libro"),   # Libro antes del final
        ],
        
        "trampas": [
            (190, 424, "espinas"),  # Trampa en plataforma
           # (380, 330, "espinas"),  # Trampa en zona media
            #(570, 424, "espinas"),  # Trampa en plataforma derecha
           # (285, 518, "espinas"),  # Trampa en el suelo
            (665, 518, "espinas"),  # Trampa cerca del final
        ],
        
        "punto_final": (750, 470, 50, 100),
    },
}

# Función auxiliar para obtener la configuración de un nivel
def obtener_config_nivel(numero_nivel):
    """
    Devuelve la configuración del nivel solicitado.
    
    Args:
        numero_nivel: Número del nivel (1, 2 o 3)
    
    Returns:
        dict: Configuración del nivel o None si no existe
    """
    return CONFIG_NIVELES.get(numero_nivel, None)

# Constantes útiles
TOTAL_NIVELES = len(CONFIG_NIVELES)
NIVEL_INICIAL = 1