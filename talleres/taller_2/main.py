import funciones as functions

#pagina 76 PDF
def main():
    while True:
        print("Elija una opcion: ")
        print("1. Operaciones basicas (Calculadora)")
        print("2. Filtrado de lista por numeros pares")
        print("3. Conversion de temperaturas de Celsius a Fahrenheit")
        print("4. Sistema de calificaciones a letras")
        print("5. Conteo de palabras en una cadena")
        print("6. Busqueda de elemento en lista")
        print("7. Validacion de secuencia de parentesis")
        print("8. Ordenamiento personalizado de lista de tuplas")
        print("9. Generador de contrasenas aleatorias")
        print("10. Gestion de agenda telefonica")
        print("11. Salir del programa")

        op = int(input("Opcion: "))

        if op == 1:
            num1 = float(input("Ingrese el primer numero: "))
            num2 = float(input("Ingrese el segundo numero: "))
            operador = input("Ingrese el operador (+, -, *, /): ")
            print(f"El resultado de la operacion es: {functions.calculadora(num1, num2, operador)}")

        if op == 2:
            lista = [int(x) for x in input("Ingrese una lista de numeros separados por espacios: ").split()]
            print(f"Los numeros pares en la lista son: {functions.filtrar_pares(lista)}")

        if op == 3:
            lista_celsius = [float(x) for x in input("Ingrese una lista de temperaturas en Celsius separadas por espacios: ").split()]
            lista_fahrenheit = functions.celsius_a_fahrenheit_lista(lista_celsius)
            print(f"Las temperaturas convertidas a Fahrenheit son: {lista_fahrenheit}")

        if op == 4:
            calificacion = float(input("Ingrese la calificacion (0-100): "))
            print(f"La calificacion en letras es: {functions.calificacion_a_letra(calificacion)}")
        
        if op == 5:
            cadena = input("Ingrese una cadena de texto: ")
            print(f"El numero de palabras en la cadena es: {functions.contar_palabras(cadena)}")
        
        if op == 6:
            lista = [int(x) for x in input("Ingrese una lista de numeros separados por espacios: ").split()]
            elemento = int(input("Ingrese el elemento a buscar: "))
            resultado = functions.buscar_elemento(lista, elemento)
            if resultado != -1:
                print(f"El elemento {elemento} se encuentra en la posicion {resultado} de la lista.")
            else:
                print(f"El elemento {elemento} no se encuentra en la lista.")

        if op == 7:
            secuencia = input("Ingrese una secuencia de parentesis: ")
            if functions.validar_parentesis(secuencia):
                print("La secuencia de parentesis es valida.")
            else:
                print("La secuencia de parentesis no es valida.")
        
        if op == 8:
            lista_tuplas = functions.ingresar_tuplas()
            print(f"Lista de tuplas ordenada: {functions.ordenar_tuplas(lista_tuplas)}")
        
        if op == 9:
            longitud = int(input("Ingrese la longitud de la contrasena: "))
            print(f"La contrasena generada es: {functions.generar_contrasena(longitud)}")

        if op == 10:
            agenda = functions.AgendaTelefonica()
            while True:
                print("Elija una opcion de agenda: ")
                print("1. Agregar contacto")
                print("2. Buscar contacto")
                print("3. Eliminar contacto")
                print("4. Mostrar todos los contactos")
                print("5. Salir de la agenda")
                
                op_agenda = int(input("Opcion: "))
                
                if op_agenda == 1:
                    nombre = input("Ingrese el nombre del contacto: ")
                    telefono = input("Ingrese el telefono del contacto: ")
                    agenda.agregar_contacto(nombre, telefono)
                    print(f"Contacto {nombre} agregado.")
                
                if op_agenda == 2:
                    nombre = input("Ingrese el nombre del contacto a buscar: ")
                    telefono = agenda.buscar_contacto(nombre)
                    if telefono:
                        print(f"El telefono de {nombre} es {telefono}.")
                    else:
                        print(f"Contacto {nombre} no encontrado.")
                
                if op_agenda == 3:
                    nombre = input("Ingrese el nombre del contacto a eliminar: ")
                    if agenda.eliminar_contacto(nombre):
                        print(f"Contacto {nombre} eliminado.")
                    else:
                        print(f"Contacto {nombre} no encontrado.")
                
                if op_agenda == 4:
                    contactos = agenda.mostrar_agenda()
                    if contactos:
                        for nombre, telefono in contactos.items():
                            print(f"{nombre}: {telefono}")
                    else:
                        print("No hay contactos en la agenda.")
                
                if op_agenda == 5:
                    break

if __name__ == '__main__':
    main()