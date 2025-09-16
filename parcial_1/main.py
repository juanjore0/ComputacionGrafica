import numpy as np
import matplotlib.pyplot as plt

def unir_4_imagenes(img1, img2, img3, img4, marco_color=(255,255,255), margen=20, salida="union.jpg"):
    """
    Une 4 imágenes en una cuadrícula 2x2 con márgenes y marcos usando solo numpy y matplotlib.

    Parámetros:
        img1, img2, img3, img4 : numpy.ndarray
            Imágenes en arrays RGB (H, W, 3).
        marco_color : tuple (R, G, B)
            Color del marco/margen (ej. (255,255,255)=blanco).
        margen : int
            Tamaño del margen alrededor de cada imagen.
        salida : str
            Nombre del archivo JPG resultante.

    Retorna:
        result : numpy.ndarray
            Imagen final combinada.
    """
    # Asegurar que todas tengan 3 canales
    def asegurar_rgb(im):
        if im.ndim == 2:  # Escala de grises
            im = np.stack([im]*3, axis=-1)
        return im

    imgs = [asegurar_rgb(im) for im in [img1, img2, img3, img4]]

    # Normalizar tamaños (usar el más pequeño)
    min_h = min(im.shape[0] for im in imgs)
    min_w = min(im.shape[1] for im in imgs)
    imgs = [im[:min_h, :min_w, :] for im in imgs]  # recortar

    # Agregar margen alrededor
    imgs_margen = []
    for im in imgs:
        h, w, c = im.shape
        nueva = np.ones((h+2*margen, w+2*margen, 3), dtype=np.uint8) * np.array(marco_color, dtype=np.uint8)
        nueva[margen:margen+h, margen:margen+w, :] = im
        imgs_margen.append(nueva)

    # Dimensiones finales
    h, w, _ = imgs_margen[0].shape
    result = np.ones((2*h, 2*w, 3), dtype=np.uint8) * np.array(marco_color, dtype=np.uint8)

    # Colocar imágenes
    result[0:h, 0:w] = imgs_margen[0]
    result[0:h, w:2*w] = imgs_margen[1]
    result[h:2*h, 0:w] = imgs_margen[2]
    result[h:2*h, w:2*w] = imgs_margen[3]

    # Guardar
    plt.imsave(salida, result.astype(np.uint8))

    return result

if __name__ == "__main__":
    # Ejemplo de uso
    img1 = np.random.randint(0, 255, (100, 150, 3), dtype=np.uint8)
    img2 = np.random.randint(0, 255, (120, 130, 3), dtype=np.uint8)
    img3 = np.random.randint(0, 255, (110, 140, 3), dtype=np.uint8)
    img4 = np.random.randint(0, 255, (90, 160, 3), dtype=np.uint8)

    resultado = unir_4_imagenes(img1, img2, img3, img4, marco_color=(0,0,0), margen=10, salida="union.jpg")
    plt.imshow(resultado)
    plt.axis('off')
    plt.show()