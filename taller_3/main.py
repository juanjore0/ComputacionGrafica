import funciones as functions
import numpy as np

def main():
    while True:
        print("Elija una opcion: ")
        print("1. Creación y Propiedades de Arrays ")
        print("2. Operaciones Básicas ")
        print("3. Indexación y Slicing")
        print("4. Broadcasting y Funciones Universales")
        print("5. Manipulación de Formas y Algebra Lineal")
        print("6. Trabajo con Datos Faltantes")
        print("7. Guardar y Cargar Arrays")
        print("8. Salir")

        op = int(input("Opcion: "))
        
        if op == 1:
            arr = np.array(range(1, 11))
            arr_reshape = arr.reshape(2, 5)

            print("Forma:", arr_reshape.shape)
            print("Tamaño:", arr_reshape.size)
            print("Dimensiones:", arr_reshape.ndim)

        elif op == 2:
            arr1 = np.array([1, 2, 3])
            arr2 = np.array([4, 5, 6])
            suma = arr1 + arr2
            resta = arr1 - arr2
            multiplicacion = arr1 * arr2
            suma_elementos = np.sum(arr1)

            print("Arreglo 1:", arr1)
            print("Arreglo 2:", arr2)
            print("Suma:", suma)
            print("Resta:", resta)
            print("Multiplicacion:", multiplicacion)
            print("Suma de elementos:", suma_elementos)

        elif op == 3:
            arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

            quinto_elemento = arr[4]
            subseccion = arr[2:7]

            print("Quinto elemento:", quinto_elemento)
            print("Subsección (índices 2 a 6):", subseccion)
        
        elif op == 4:
            A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

            print("Matriz A:")
            print(A)

            B = A + 10
            print("\nA + 10:")
            print(B)

            C = np.sqrt(A)
            print("\nRaíz cuadrada de A:")
            print(C)
        
        elif op == 5:
            M = np.array([1, 2, 3, 4, 5, 6])
            print("Arreglo original M:")
            print(M)
            M = M.reshape(3, 2)
            print("\nM en forma (3,2):")
            print(M)
            # Transponer la matriz
            producto = np.dot(M, M.T)
            print("\nProducto punto M · M.T:")
            print(producto)
        
        elif op == 6:
            data = np.array([1, 2, np.nan, 4, 5])
            
            data_filled = np.nan_to_num(data, nan=0)
            print("Datos originales:", data)
            print("Datos sin NaN:", data_filled)
        
        elif op == 7:
            arr = np.array([1, 2, 3, 4, 5])
            np.save('mi_array.npy', arr)
            print("Arreglo guardado como 'mi_array.npy'")

            loaded_arr = np.load('mi_array.npy')
            print("Arreglo cargado:", loaded_arr)

        
        elif op == 8:
            print("Adios")
            break
        else:
            print("Opcion no valida, intente de nuevo.")
        
if __name__ == '__main__':
    main()