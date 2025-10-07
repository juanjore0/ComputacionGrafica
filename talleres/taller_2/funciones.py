import math
import string

#1. Operaciones basicas (Calculadora)
def calculadora(num1, num2, operacion):
    if operacion == '+':
        return num1 + num2
    elif operacion == '-':
        return num1 - num2
    elif operacion == '*':
        return num1 * num2
    elif operacion == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division por cero"
    else:
        return "Operacion no valida"
    
#2. Filtrado de lista por numeros pares
def filtrar_pares(lista):
    return [num for num in lista if num % 2 == 0]

#3. Conversion de temperaturas de Celsius a Fahrenheit
def celsius_a_fahrenheit_lista(lista_celsius):
    return list(map(lambda c: (c * 9/5) + 32, lista_celsius))

#4. Sistema de calificaciones a letras
def calificacion_a_letra(calificacion):
    if 90 <= calificacion <= 100:
        return 'A'
    elif 80 <= calificacion < 90:
        return 'B'
    elif 70 <= calificacion < 80:
        return 'C'
    elif 60 <= calificacion < 70:
        return 'D'
    elif 0 <= calificacion < 60:
        return 'F'
    else:
        return "Calificacion no valida"
    
#5. Conteo de palabras en una cadena
def contar_palabras(texto):
    # Convertir todo a minúsculas
    texto = texto.lower()
    
    # Eliminar signos de puntuación
    for signo in string.punctuation:
        texto = texto.replace(signo, "")
    
    # Dividir en palabras
    palabras = texto.split()
    
    # Crear diccionario de conteo
    conteo = {}
    for palabra in palabras:
        conteo[palabra] = conteo.get(palabra, 0) + 1
    
    return conteo

#6. Busqueda de elemento en lista
def buscar_elemento(lista, elemento):
    for i in range(len(lista)):   
        if lista[i] == elemento:
            return i              
    return -1

#7. Validacion de secuencia de parentesis
def parentesis_valido(cadena):
    contador = 0
    
    for c in cadena:
        if c == "(":
            contador += 1   # abrimos un paréntesis
        elif c == ")":
            contador -= 1   # cerramos un paréntesis
            
        if contador < 0:
            return False
    
    return contador == 0

#8. Ordenamiento personalizado de lista de tuplas (nombre,  edad)
def ingresar_tuplas():
    lista_tuplas = []
    n = int(input("Ingrese la cantidad de personas: "))
    
    for _ in range(n):
        nombre = input("Ingrese el nombre: ").strip()
        edad = int(input("Ingrese la edad: ").strip())
        lista_tuplas.append((nombre, edad))

    return lista_tuplas

def ordenar_tuplas(lista):
    return sorted(lista, key=lambda persona: (persona[1], persona[0]))

#9. Generador de contrasenas aleatorias
def generar_contrasena(longitud):
    import random
    
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    
    return contrasena

#10. Gestion de agenda telefonica
class AgendaTelefonica:
    def __init__(self):
        self.agenda = {}
    
    def agregar_contacto(self, nombre, numero):
        self.agenda[nombre] = numero
    
    def eliminar_contacto(self, nombre):
        if nombre in self.agenda:
            del self.agenda[nombre]
    
    def buscar_contacto(self, nombre):
        return self.agenda.get(nombre, "Contacto no encontrado")
    
    def mostrar_agenda(self):
        return self.agenda

