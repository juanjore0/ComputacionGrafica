import transformaciones_function as tr

def menu():
    print('Selecciona una opción:')
    print('1. Ajuste de brillo')
    print('2. Ajuste canal')
    print('3. Ajuste de contraste')
    print('4. Zoom imágen')
    print('5. Binarizar imágen')
    print('6. Rotar imágen')
    print('7. Histograma RGB')
    print('8. Salir')

def main():
    barco = tr.create_img('imagenes/barco.png')
    
    while True:
        menu()
        opcion = int(input())
        if opcion == 1:
            factor = float(input('Ingrese el factor de brillo en valores entre 0 y 1: '))
            tr.brightness_adjust(barco, factor)
        elif opcion == 2:
            print('0. Rojo')
            print('1. Verde')
            print('2. Azul')
            channel = int(input('Ingrese el canal a ajustar (0, 1, 2): '))
            factor = float(input('Ingrese el factor de brillo en valores entre 0 y 1: '))
            tr.adjust_channel_brightness(barco, factor, channel)
        elif opcion == 3:
            factor = float(input('Ingrese el factor de contraste en valores entre 0 y 1: '))
            tr.contrast_adjust(barco, factor)
        elif opcion == 4:
            x1 = int(input('Ingrese el punto x inicial: '))
            x2 = int(input('Ingrese el punto x final: '))
            y1 = int(input('Ingrese el punto y inicial: '))
            y2 = int(input('Ingrese el punto y final: '))
            tr.zoom_image(barco, x1, x2, y1, y2)
        elif opcion == 5:
            umbral = float(input('Ingrese el umbral para binarizar la imágen: '))
            tr.binary(barco, umbral)
        elif opcion == 6:
            ang = float(input('Ingrese el ángulo de rotación: '))
            tr.rotate(barco, ang)
        elif opcion == 7:
            tr.rgb_histogram(barco)
        elif opcion == 8:
            print('Adios')
            break
        else:
            print('Opción no válida')

if __name__ == '__main__':
    main()