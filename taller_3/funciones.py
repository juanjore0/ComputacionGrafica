import math
import numpy as np


# 3. Indexación y Slicing
def desplazamiento(velocidad_inicial, aceleracion, tiempo):
    return velocidad_inicial * tiempo + 0.5 * aceleracion * tiempo**2

# 4. Suma de vectores
def suma_vectorial(v1, v2):
    if len(v1) == len(v2):
        return [v1[i] + v2[i] for i in range(len(v1))]
    else:
        return 'Los vectores deben tener la misma longitud'

# 5. Producto escalar de vectores (es la suma de los productos de sus componentes)
def producto_escalar(v1, v2):
    if len(v1) == len(v2):
        return sum(v1[i] * v2[i] for i in range(len(v1)))
    else:
        return 'Los vectores deben tener la misma longitud'
    
# 6. Lanzamiento de proyectil
def alcance_maximo(velocidad_inicial, angulo):
    angulo_rad = math.radians(angulo)
    return (velocidad_inicial**2) * math.sin(2 * angulo_rad) / 9.81

def altura_maxima(velocidad_inicial, angulo):
    angulo_rad = math.radians(angulo)
    return (velocidad_inicial**2 * (math.sin(angulo_rad)**2)) / (2 * 9.81)

def seleccion(opcion, velocidad_inicial, angulo):
    if opcion == 1:
        return alcance_maximo(velocidad_inicial, angulo)
    elif opcion == 2:
        return altura_maxima(velocidad_inicial, angulo)
    else:
        return "Opcion invalida"