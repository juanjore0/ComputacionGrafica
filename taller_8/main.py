import imagen_function as ip

def menu():
    print("Elija una opcion: ")
    print("1. Matriz de colores")
    print("2. Matriz de colores con filtro")
    print("3. Invertir colores de una imágen")
    print("4. Capa roja de una imágen")
    print("5. Capa verde de una imágen")
    print("6. Capa azul de una imágen") 
    print("7. Capa magenta de una imágen")
    print("8. Capa cyan de una imágen")
    print("9. Capa amarilla de una imágen")
    print("10. Sumar capas de una imágen")
    print("11. Fusionar imágenes")
    print("12. Ecualizar imágenes")
    print("13. Ecualizar imágen individual")
    print("14. Promediar imágen")
    print("15. Escala de grises por average")
    print("16. Escala de grises por luminosity")
    print("17. Escala de grises por midgray")
    print("18. Salir")

def main():
    mar = "imagenes/mar.png"
    barco = "imagenes/barco.png"
    utp = "imagenes/utp.png"
    
    while True:
        menu()
        op = int(input("Opcion: "))
        if op == 1:
            ip.create_matriz_colors()
        elif op == 2:
            ip.create_tv()
        elif op == 3:
            ip.invert_color(utp)
        elif op == 4:
            ip.red_cape(utp)
        elif op == 5:
            ip.green_cape(utp)
        elif op == 6:
            ip.blue_cape(utp)
        elif op == 7:
            ip.magenta_cape(utp)
        elif op == 8:
            ip.cyan_cape(utp)
        elif op == 9:
            ip.yellow_cape(utp)
        elif op == 10:
            R, G, B = ip.separate_channels(utp)
            ip.sum_channels(R, G, B)
        elif op == 11:
            ip.fusion_images(mar, barco)
        elif op == 12:
            ip.fusion_images_equalized(mar, barco)
        elif op == 13:
            ip.equalizate_image(mar, 0.5)
        elif op == 14:
            ip.average(mar)
        elif op == 15:
            ip.average_gray(barco)
        elif op == 16:
            ip.luminosity(barco)
        elif op == 17:
            ip.midgray(barco)
        elif op == 18:
            print("Saliendo...")
            break

if __name__ == '__main__':
    main()