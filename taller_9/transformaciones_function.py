import numpy as np
import matplotlib.pyplot as plt

def create_img(path):
    img = np.array(plt.imread(path)).astype(float)
    if img.max() > 1.0:   # si está en [0..255]
        img = img / 255.0
    return img

def gray(img):
    img_gris = np.mean(img, axis=2)
    return img_gris

def brightness_adjust(img, factor):
    img_ab = img + factor  # Ajuste brillo

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(img)
    axs[0].set_title('Original')
    axs[0].axis('off')

    axs[1].imshow(img_ab)
    axs[1].set_title('Ajuste brillo')
    axs[1].axis('off')

    plt.show()

def adjust_channel_brightness(img, factor, channel):
    img_adjust = img + factor
    img_mod = np.copy(img)
    img_mod[:,:,channel] = img_adjust[:,:,channel]
    plt.imshow(img_mod)
    plt.title('Ajuste brillo')
    plt.axis('off')
    plt.show()

def contrast_adjust(img, factor):
    dark_constrast = factor * np.log10(1 + img)
    light_constrast = factor * np.exp(img - 1)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].imshow(img)
    axs[0].set_title('Original')
    axs[0].axis('off')

    axs[1].imshow(dark_constrast)
    axs[1].set_title('Contraste oscuro')
    axs[1].axis('off')

    axs[2].imshow(light_constrast)
    axs[2].set_title('Contraste claro')
    axs[2].axis('off')
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

def zoom_image(img, x_start, x_end, y_start, y_end):
    """
    Realiza un zoom a una parte de la imagen.
    
    Parámetros:
    - img: imagen en forma de array numpy
    - x_start, x_end: rango en el eje horizontal (columnas)
    - y_start, y_end: rango en el eje vertical (filas)
    """
    # Recortar la región de interés (ROI)
    zoomed = img[y_start:y_end, x_start:x_end]

    # Mostrar original y zoom
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(zoomed)
    plt.title("Zoom")
    plt.axis("off")

    plt.show()

    return zoomed

def binary(img, threshold):
    img_gray = np.mean(img, axis=2)
    img_bin = img_gray > threshold  # Binarización
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('Imagen original')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_bin, cmap='gray')
    plt.title('Imagen binarizada')
    plt.axis('off')
    plt.show()

def rotate(img, ang):
    rad = np.radians(ang)
    img_rot = np.zeros_like(img)
    x, y = img.shape[:2] # Dimensiones de la imagen
    x_c, y_c = x//2, y//2 # Centro de la imagen
    for i in range(x):
        for j in range(y):
            x_r = int((i - x_c) * np.cos(rad) - (j - y_c) * np.sin(rad) + x_c) # Rotación
            y_r = int((i - x_c) * np.sin(rad) + (j - y_c) * np.cos(rad) + y_c) 
            if x_r >= 0 and x_r < x and y_r >= 0 and y_r < y:
                img_rot[x_r, y_r] = img[i, j]
    plt.imshow(img_rot, cmap='gray')
    plt.title('Rotar imagen')
    plt.axis('off')
    plt.show()


def rgb_histogram(imagen):
    """
    Calcula y muestra los histogramas RGB de cualquier imagen en un solo lienzo.
    
    Parámetros:
    imagen : numpy array
        Imagen de cualquier tipo: RGB, RGBA o escala de grises.
    
    Retorna:
    hist_r, hist_g, hist_b : numpy arrays
        Histogramas de cada canal.
    """
    # Asegurar 3 canales
    if imagen.ndim == 2:  # Escala de grises
        imagen = np.stack([imagen]*3, axis=-1)
    elif imagen.shape[2] == 4:  # RGBA
        imagen = imagen[:, :, :3]
    elif imagen.shape[2] != 3:
        raise ValueError("La imagen debe tener 1, 3 o 4 canales.")

    # Normalizar valores a rango 0-255
    if imagen.max() <= 1.0:
        imagen = (imagen * 255).astype(np.uint8)
    else:
        imagen = np.clip(imagen, 0, 255).astype(np.uint8)

    # Separar canales
    canal_r = imagen[:, :, 0].flatten()
    canal_g = imagen[:, :, 1].flatten()
    canal_b = imagen[:, :, 2].flatten()

    # Calcular histogramas
    hist_r, _ = np.histogram(canal_r, bins=256, range=(0, 255))
    hist_g, _ = np.histogram(canal_g, bins=256, range=(0, 255))
    hist_b, _ = np.histogram(canal_b, bins=256, range=(0, 255))

    # Graficar
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.bar(np.arange(256), hist_r, color='red', alpha=0.7)
    plt.title('Histograma Canal Rojo')
    plt.xlabel('Intensidad')
    plt.ylabel('Frecuencia')

    plt.subplot(3, 1, 2)
    plt.bar(np.arange(256), hist_g, color='green', alpha=0.7)
    plt.title('Histograma Canal Verde')
    plt.xlabel('Intensidad')
    plt.ylabel('Frecuencia')

    plt.subplot(3, 1, 3)
    plt.bar(np.arange(256), hist_b, color='blue', alpha=0.7)
    plt.title('Histograma Canal Azul')
    plt.xlabel('Intensidad')
    plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()

    return hist_r, hist_g, hist_b