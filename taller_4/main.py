import numpy as np

def main():
    while True:
        print("\nMenú de opciones:")
        print("1. Array Unidimensional")
        print("2. Array Multidimensional")
        print("3. Suma de arrays")
        print("4. Calcular exponencial")
        print("5. Indexación y Segmentación")
        print("6. Generación de Datos Aleatorios")
        print("7. Funciones de Agregación")
        print("8. Arrays con Funciones de Fábrica")
        print("9. Alineación y Broadcasting")
        print("10. Transformación y Redimensionamiento")
        print("0. Salir")
        opcion = input("Ingresa la opción: ")

        if opcion == "1":
            arrayU = np.array([1,2,3,4,5,6,7,8,9,10])
            print("Array unidimensional", arrayU)
        
        elif opcion == "2":
            arrayM = np.array([[1,2,3],[4,5,6],[7,8,9]])
            print("Array multidimensional:\n", arrayM)
        
        elif opcion == "3":
            array1 = np.array([1,2,3,4,5])
            array2 = np.array([1,2,3,4,5])
            add = np.array([array1, array2])
            print("La suma del array 1", array1, "y el array 2", array2, "es:\n", add)

        elif opcion == "4":
            array1 = np.array([1,2,3,4,5])
            exponential = np.exp(array1)
            print("El exponencial del array es:", exponential)

        elif opcion == "5":
            arrayU = np.array([1,2,3,4,5,6,7,8,9,10])
            pairs = arrayU[arrayU % 2 == 0]
            print(f"Elementos pares: {pairs} ")

        elif opcion == "6":
            randomArray = np.random.rand(10)
            print("Array aleatorio generado:\n", randomArray)

        elif opcion == '7':
            array1 = np.array([1,2,3,4,5])
            mean1 = np.mean(array1)
            print("la media del array es:", mean1)

        elif opcion == '8':
            arrayFull = np.full(5,7)
            print("Array con función de fábrica:\n", arrayFull)

        elif opcion == '9':
            array1 = np.array([1,2,3])
            array2 = np.array([4,5,6])
            add = array1 + array2
            print("La suma de los arrays es:", add)

        elif opcion == '10':
            array1 = np.array([[1,2,3,4,5,6]])
            changed = np.reshape(array1, (2,3))
            print("Array cambiado de forma:\n", changed)

        elif opcion == "0":
            print("Saliendo del programa...")
            break

if __name__ == '__main__':
    main()
