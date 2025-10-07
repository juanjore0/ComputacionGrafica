import numpy as np
import matplotlib.pyplot as plt

def create_img(path):
    img = plt.imread(path)

    if img.dtype == np.uint8:
        img = img.astype(np.float32) / 255.0

    # Si tiene canal alfa, lo eliminamos
    if img.shape[-1] == 4:
        img = img[:, :, :3]

    return img


def gris(img):
    img_gris = np.mean(img, axis=2)
    return img_gris

def brightness_adjust(img, factor):
    img_ab = img + factor # Ajuste brillo
    return img_ab

def adjust_cape_brightness(img, factor, cape):
    img_ab = img + factor
    img_acb = np.copy(img)
    img_acb[:,:,cape] = img_ab[:,:,cape]
    return img_acb

def contrast_adjust_brightness(img, factor): 
    img_acl = factor * np.exp(img - 1) 
    return img_acl

def contrast_adjust_darkness(img, factor):
    img_acd = factor * np.log10(1 + img)
    return img_acd

def binary(img, umbral):
    img_gris = np.mean(img, axis=2)  # Convertir a escala de grises (H, W)
    img_bin = (img_gris > umbral).astype(np.float32)  # Convertir a float32 con 0.0 y 1.0

    # Convertir a RGB (H, W, 3)
    img_rgb = np.stack((img_bin,)*3, axis=-1)

    return img_rgb


def snip(img, x1, y1, x2, y2):
    img_snip = img[x1:x2, y1:y2]
    return img_snip

def rotate(img, ang):
    if ang is None:
        return img
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
    return img_rot

def RGB_Histogram(img):
    R = img[:,:,0] # Capa roja
    G = img[:,:,1] # Capa verde
    B = img[:,:,2] # Capa azul
    
    # Crear la figura
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.hist(R.ravel(), bins=256, range=(0, 1), color='red', alpha=0.5)
    plt.title('Rojo')
    
    plt.subplot(1, 3, 2)
    plt.hist(G.ravel(), bins=256, range=(0, 1), color='green', alpha=0.5)
    plt.title('Verde')
    
    plt.subplot(1, 3, 3)
    plt.hist(B.ravel(), bins=256, range=(0, 1), color='blue', alpha=0.5)
    plt.title('Azul')
    
    plt.show()

def translation(img, x, y):
    img_tr = np.zeros_like(img)
    i, j = img.shape[:2] # Dimensiones de la imagen
    img_tr[x:, y:] = img[:i-x, :j-y]
    return img_tr

def zoom(img, factor):
    x, y = img.shape[:2]
    x_c, y_c = x//2, y//2 # Centro de la imagen
    x_start, x_end = x_c - int(x_c * factor), x_c + int(x_c * factor)
    y_start, y_end = y_c - int(y_c * factor), y_c + int(y_c * factor)
    img_z = img[x_start:x_end, y_start:y_end]
    return img_z

def fusion_images(img_base, img_fusion, factor):
    '''
    Función que junta dos imágenes a partir del centro
    '''
    ancho, largo = img_fusion.shape[:2]
    x, y = img_base.shape[:2]
    
    x_centro = (x-ancho) // 2
    y_centro = (y-largo) // 2

    for i in range(ancho):
        for j in range(largo):
                img_base[x_centro + i, y_centro + j ] = (img_base[x_centro + i, y_centro + j ] * (1 - factor)) + img_fusion[i, j] * factor
    return img_base
