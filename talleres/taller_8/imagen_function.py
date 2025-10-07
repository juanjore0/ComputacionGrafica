import numpy as np
import matplotlib.pyplot as plt

def create_matriz_colors():
    matriz = np.zeros((3,3,3))  # igual, empieza en blanco

    matriz[0,0,1] = matriz[0,0,2] = 1     # cyan (R=0, G=1, B=1)
    matriz[0,1,0] = matriz[0,1,1] = matriz[0,1,2] = 1  # blanco (1,1,1)
    matriz[0,2,0] = 1     # rojo (1,0,0)
    matriz[1,0,0] = matriz[1,0,2] = 1     # magenta (1,0,1)
    matriz[1,1,0] = matriz[1,1,1] = matriz[1,1,2] = 0.5 # gris
    matriz[1,2,1] = 1     # verde (0,1,0)
    matriz[2,0,0] = matriz[2,0,1] = 1     # amarillo (1,1,0)
    # negro queda (0,0,0) por defecto
    matriz[2,2,2] = 1     # azul (0,0,1)

    plt.imshow(matriz)
    plt.show()


def create_tv():
    '''
    Crea una matriz de colores semejando al que se hace en la TV
    pero partiendo desde negro (np.zeros).
    '''
    # Arrancamos desde negro matriz 8 columnas x 11 filas
    matriz = np.zeros((8,11,3))  

    # Fila superior de colores 
    matriz[:6,0]    = [1,1,0]   # amarillo
    matriz[:6,1:3]  = [0,1,1]   # cyan
    matriz[:6,3:5]  = [0,1,0]   # verde
    matriz[:6,5:7]  = [1,0,1]   # magenta
    matriz[:6,7:9]  = [1,0,0]   # rojo
    matriz[:6,9:11] = [0,0,1]   # azul

    # Fila inferior de grises 
    matriz[6:8,0]  = 1 #Blanco 
    matriz[6:8,1]  = 0.9
    matriz[6:8,2]  = 0.7
    matriz[6:8,3]  = 0.6 #[0.6,0.6,0.6]
    matriz[6:8,4]  = 0.5
    matriz[6:8,5]  = 0.3
    matriz[6:8,6]  = 0.2
    matriz[6:8,7:11]  = 0.1
 

    # Factor de atenuación 
    factor = 0.6
    matriz = matriz * factor 

    # Mostrar imagen
    plt.imshow(matriz) 
    plt.axis("off") 
    plt.show()

def invert_color(img):
    '''
    Invierte los colores de una imagen (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)

    # Normalizar si está en 0–255
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    # Si tiene canal alfa, separamos
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen[..., :3], imagen[..., 3:]
        imagen_invertida = np.concatenate([1 - rgb, alpha], axis=-1)
    else:
        imagen_invertida = 1 - imagen

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_invertida)
    axs[1].set_title("Invertida")
    axs[1].axis("off")
    plt.show()

def red_cape(img):
    '''
    Cambia los colores de una imagen a rojo (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_roja = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_roja[..., :3], imagen_roja[..., 3:]
        rgb[..., 1] = rgb[..., 2] = 0
        imagen_roja = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_roja[..., 1] = imagen_roja[..., 2] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_roja)
    axs[1].set_title("Capa Roja")
    axs[1].axis("off")
    plt.show()


def green_cape(img):
    '''
    Cambia los colores de una imagen a verde (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_verde = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_verde[..., :3], imagen_verde[..., 3:]
        rgb[..., 0] = rgb[..., 2] = 0
        imagen_verde = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_verde[..., 0] = imagen_verde[..., 2] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_verde)
    axs[1].set_title("Capa Verde")
    axs[1].axis("off")
    plt.show()


def blue_cape(img):
    '''
    Cambia los colores de una imagen a azul (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_azul = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_azul[..., :3], imagen_azul[..., 3:]
        rgb[..., 0] = rgb[..., 1] = 0
        imagen_azul = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_azul[..., 0] = imagen_azul[..., 1] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_azul)
    axs[1].set_title("Capa Azul")
    axs[1].axis("off")
    plt.show()


def magenta_cape(img):
    '''
    Cambia los colores de una imagen a magenta (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_magenta = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_magenta[..., :3], imagen_magenta[..., 3:]
        rgb[..., 1] = 0
        imagen_magenta = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_magenta[..., 1] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_magenta)
    axs[1].set_title("Capa Magenta")
    axs[1].axis("off")
    plt.show()


def cyan_cape(img):
    '''
    Cambia los colores de una imagen a cyan (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_cyan = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_cyan[..., :3], imagen_cyan[..., 3:]
        rgb[..., 0] = 0
        imagen_cyan = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_cyan[..., 0] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_cyan)
    axs[1].set_title("Capa Cyan")
    axs[1].axis("off")
    plt.show()


def yellow_cape(img):
    '''
    Cambia los colores de una imagen a amarillo (sin tocar el alfa)
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    imagen_amarilla = imagen.copy()
    if imagen.shape[-1] == 4:
        rgb, alpha = imagen_amarilla[..., :3], imagen_amarilla[..., 3:]
        rgb[..., 2] = 0
        imagen_amarilla = np.concatenate([rgb, alpha], axis=-1)
    else:
        imagen_amarilla[..., 2] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen)
    axs[0].set_title("Original")
    axs[0].axis("off")
    axs[1].imshow(imagen_amarilla)
    axs[1].set_title("Capa Amarilla")
    axs[1].axis("off")
    plt.show()

#separar imagen 
def separate_channels(img):
    '''
    Separa las capas de color de una imagen en R, G y B.
    Retorna tres arrays 2D correspondientes a cada capa.
    '''
    imagen = np.array(plt.imread(img)).astype(float)
    if imagen.max() > 1.0:
        imagen = imagen / 255.0

    if imagen.shape[-1] == 4:
        rgb = imagen[..., :3]
    else:
        rgb = imagen

    red = rgb[..., 0]
    green = rgb[..., 1]
    blue = rgb[..., 2]

    return red, green, blue

def sum_channels(red, green, blue):
    '''
    Reconstruye una imagen a color a partir de sus capas R, G y B.
    Se asume que R, G y B son arrays 2D del mismo tamaño.
    '''
    if red.shape != green.shape or red.shape != blue.shape:
        raise ValueError("Las capas deben tener el mismo tamaño")
    
    imagen_reconstruida = np.stack([red, green, blue], axis=-1)
    plt.imshow(imagen_reconstruida)
    plt.axis("off")
    plt.show()

def fusion_images(img1, img2):
    '''
    Fusiona dos imágenes sin ecualizar (promedio de píxeles)
    '''
    img_1 = np.array(plt.imread(img1))
    img_2 = np.array(plt.imread(img2))

    # Asegurar que ambas imágenes sean RGB (3 canales)
    if img_1.shape[2] == 4:
        img_1 = img_1[:, :, :3]
    if img_2.shape[2] == 4:
        img_2 = img_2[:, :, :3]

    # Normalizar si están en [0..255]
    if img_1.max() > 1:
        img_1 = img_1 / 255
    if img_2.max() > 1:
        img_2 = img_2 / 255

    img_3 = (img_1 + img_2)

    # Mostrar
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    axs[0].imshow(img_1)
    axs[0].set_title("Imagen 1")
    axs[0].axis("off")

    axs[1].imshow(img_2)
    axs[1].set_title("Imagen 2")
    axs[1].axis("off")

    axs[2].imshow(img_3)
    axs[2].set_title("Fusión")
    axs[2].axis("off")

    plt.show()

    return img_3

def fusion_images_equalized(img1, img2):
    """
    Fusiona dos imágenes aplicando una mezcla ponderada.
    """
    # Leer imágenes
    img_1 = np.array(plt.imread(img1))
    img_2 = np.array(plt.imread(img2))

    # Quitar alfa si existe
    if img_1.shape[2] == 4:
        img_1 = img_1[:, :, :3]
    if img_2.shape[2] == 4:
        img_2 = img_2[:, :, :3]

    # Normalizar si están en [0..255]
    if img_1.max() > 1:
        img_1 = img_1 / 255.0
    if img_2.max() > 1:
        img_2 = img_2 / 255.0

    # Fusión ponderada
    factor = 0.3
    fusion = img_1 * factor + img_2 * (1 - factor)

    # Mostrar resultados
    fig, axs = plt.subplots(1, 3, figsize=(12, 6))

    axs[0].imshow(img_1)
    axs[0].set_title("Imagen 1")
    axs[0].axis("off")

    axs[1].imshow(img_2)
    axs[1].set_title("Imagen 2")
    axs[1].axis("off")

    axs[2].imshow(fusion)
    axs[2].set_title("Fusión")
    axs[2].axis("off")

    plt.tight_layout()
    plt.show()

    return fusion

def equalizate_image(img, factor):
    '''
    Ecualiza una imagen multiplicando por un factor
    '''
    capa_original = np.array(plt.imread(img)).astype(float)

    # Normalizar a [0,1] si está en 0-255
    if capa_original.max() > 1.0:
        capa_original = capa_original / 255.0

    # Aplicar el factor y asegurar que quede en [0,1]
    capa_ecualizada = capa_original * factor

    # Mostrar resultados
    plt.subplot(1,2,1)
    plt.imshow(capa_original)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(capa_ecualizada)
    plt.title(f"Ecualizada (x{factor})")
    plt.axis("off")

    plt.show()
    return capa_ecualizada

def average(img):
    '''
    Promedia los colores de una imagen
    '''
    capa_original = np.array(plt.imread(img)).astype(float)

    capa_modificada = np.mean(capa_original, axis=2) #average

    # Mostrar resultados
    plt.subplot(1,2,1)
    plt.imshow(capa_original)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(capa_modificada)
    plt.title("Promediada")
    plt.axis("off")
    plt.show()

    return capa_modificada

def average_gray(img):
    '''
    Promedia los colores de una imagen
    '''
    capa_original = np.array(plt.imread(img)).astype(float)

    capa_grises = np.mean(capa_original, axis=2) #average

    # Mostrar resultados
    plt.subplot(1,2,1)
    plt.imshow(capa_original)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(capa_grises, cmap="gray")
    plt.title("Promediada")
    plt.axis("off")
    plt.show()

    return capa_grises

def luminosity(img):
    '''
    Convierte una imagen a escala de grises con la tecnica luminosity
    '''
    imagen = np.array(plt.imread(img))/255 # Normalizar la imagen

    capa_grises =  0.2989*imagen[:,:,0] + 0.5870*imagen[:,:,1] + 0.1140*imagen[:,:,2] #luminosity

    plt.imshow(capa_grises, cmap="gray")
    plt.axis("off")

    plt.show()
    return capa_grises

def midgray(img):
    '''
    Convierte una imagen a escala de grises con la tecnica midgray
    '''
    imagen = np.array(plt.imread(img))/255 # Normalizar la imagen

    capa_grises = (np.maximum(imagen[:,:,0], imagen[:,:,1], imagen[:,:,2]) + np.minimum(imagen[:,:,0], imagen[:,:,1], imagen[:,:,2])) / 2 # midgray

    plt.imshow(capa_grises, cmap="gray")
    plt.axis("off")

    plt.show()
    return capa_grises