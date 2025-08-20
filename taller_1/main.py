import funciones as functions

def main():
    while True:
        print("Elija una opcion: ")
        print("1. Tiempo caida libre")
        print("2. Conversion de unidades")
        print("3. Desplazamiento")
        print("4. Suma de vectores")
        print("5. Producto escalar")
        print("6. Lanzamiento de proyectil")
        print("7. Salir")

        op = int(input("Opcion: "))
        
        if op == 1:
            h = float(input("Ingrese la altura: "))
            print(f"El tiempo que se demora en caer de una altura {h} es {functions.mrua(h)}")
        elif op == 2:
            v = float(input("Ingrese la velocidad: "))
            u = input("Ingrese la unidad en la que ingreso la velocidad: ")
            print(f"La velocidad convertida es {functions.conversion(v, u)}")
        elif op == 3:
            v = float(input("Ingrese la velocidad inicial: "))
            a = float(input("Ingrese la aceleracion: "))
            t = float(input("Ingrese el tiempo: "))
            print(f"El desplazamiento es {functions.desplazamiento(v, a, t)}")
        elif op == 4:
            v1 = [int(x) for x in input("Ingrese el primer vector: ").split()]
            v2 = [int(x) for x in input("Ingrese el segundo vector: ").split()]
            print(f"La suma de los vectores es {functions.suma_vectorial(v1, v2)}")
        elif op == 5:
            v1 = [int(x) for x in input("Ingrese el primer vector: ").split()]
            v2 = [int(x) for x in input("Ingrese el segundo vector: ").split()]
            print(f"El producto escalar de los vectores es {functions.producto_escalar(v1, v2)}")
        elif op == 6:
            vo = float(input("Ingrese la velocidad inicial: "))
            theta = float(input("Ingrese el angulo: "))
            print("1. Alcance maximo")
            print("2. Altura maxima")
            sub_op = int(input("Opcion: "))
            print(functions.seleccion(sub_op, vo, theta))
        elif op == 7:
            print("Adios")
            break
        else:
            print("Opcion no valida, intente de nuevo.")
        
if __name__ == '__main__':
    main()