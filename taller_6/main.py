import numpy as np
import matplotlib.pyplot as plt

#Crear un array de 1 a 15 y luego darle forma de 3 filas y 5 columnas
A = np.arange(1, 16)
print(A)

A = A.reshape(3, 5)
print(A)

#Operaciones basicas
print("Suma de todos los elementos:", np.sum(A))
print("Media de los elementos:", np.mean(A))
print("Producto de todos los elementos:", np.prod(A))

#acceso y slicing (2 y 3 elemento de la fila 2)
print("Elemento en la fila 2, columna 3:", A[1, 1:3])

#Indexación booleana (elementos mayores a 7)
B = A[A > 7]

#Calcula el determinante y la inversa de una matriz cuadrada C de 3x3 que crees. 
C = np.array([[4, 7, 2],
              [3, 6, 1],
              [2, 5, 3]])

det_C = np.linalg.det(C)
inv_C = np.linalg.inv(C)
print("Matriz C:\n", C)
print("Determinante de C:", det_C)
print("Inversa de C:\n", inv_C)

#Estadisitca (array D de 100 elementos aleatorios entre 1 y 100)
D = np.random.randint(1, 101, size=100)
max_D = np.max(D)
min_D = np.min(D)
mean_D = np.mean(D)
std_D = np.std(D)

print("Array D:\n", D)
print("Máximo de D:", max_D)
print("Mínimo de D:", min_D)
print("Media de D:", mean_D)
print("Desviación estándar de D:", std_D)

#Grafico basico (funcion seno y coseno rango -2pi a 2pi)
x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

# Funciones seno y coseno
y_sin = np.sin(x)
y_cos = np.cos(x)

# Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(x, y_sin, label='sin(x)')
plt.plot(x, y_cos, label='cos(x)')

# Detalles del gráfico
plt.title('Funciones seno y coseno en [-2π, 2π]')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.7)  # eje x
plt.axvline(0, color='black', linewidth=0.7)  # eje y
plt.legend()
plt.grid(True)

# Colocar ticks en múltiplos de π
xticks = [-2*np.pi, -1.5*np.pi, -np.pi, -0.5*np.pi, 0,
          0.5*np.pi, np.pi, 1.5*np.pi, 2*np.pi]
xtick_labels = [r'$-2\pi$', r'$-3\pi/2$', r'$-\pi$', r'$-\pi/2$', '0',
                r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$']
plt.xticks(xticks, xtick_labels)

plt.tight_layout()
plt.show()

#Grafico de dispersion del array D
plt.figure(figsize=(10, 5))
plt.scatter(range(len(D)), D, color='blue', alpha=0.6)
plt.title('Gráfico de dispersión del array D')
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.show()

#Histograma del array D
plt.figure(figsize=(10, 5))
plt.hist(D, bins=10, color='green', alpha=0.7, edgecolor='black')
plt.title('Histograma del array D')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.show()

#Leer imagen y convertir a escala de grises
imagen = plt.imread("C:\\Users\\risin\\Desktop\\Sexto Semestre\\Computación grafica\\taller_6\\imagen.png")

if imagen.ndim == 3:
    imagen_gris = np.mean(imagen, axis=2)
else:
    imagen_gris = imagen

plt.figure(figsize=(8, 8))

#imagen original
plt.subplot(1, 2, 1)
plt.imshow(imagen)
plt.title('Imagen Original')
plt.axis('off')

#imagen en escala de grises
plt.subplot(1, 2, 2)
plt.imshow(imagen_gris, cmap='gray')
plt.title('Imagen en Escala de Grises')
plt.axis('off')
plt.show()