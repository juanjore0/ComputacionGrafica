import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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

def zoom(img, factor, center_x=None, center_y=None):
    """
    Aplica zoom a la imagen desde un punto específico y redimensiona al tamaño original
    
    Parameters:
    -----------
    img : numpy.ndarray
        Imagen a la que aplicar zoom
    factor : float
        Factor de zoom (0.5 = zoom 2x, 0.25 = zoom 4x)
        Valores menores = más zoom
    center_x : int, optional
        Coordenada X del centro del zoom (fila). Si es None, usa el centro de la imagen
    center_y : int, optional
        Coordenada Y del centro del zoom (columna). Si es None, usa el centro de la imagen
    
    Returns:
    --------
    numpy.ndarray
        Imagen con zoom aplicado y redimensionada al tamaño original
    """
    x, y = img.shape[:2]
    original_shape = img.shape  # Guardar forma original (incluye canales de color)
    
    # Si no se especifican coordenadas, usar el centro de la imagen
    if center_x is None:
        center_x = x // 2
    if center_y is None:
        center_y = y // 2
    
    # Asegurar que las coordenadas estén dentro de los límites
    center_x = max(0, min(center_x, x - 1))
    center_y = max(0, min(center_y, y - 1))
    
    # Calcular el tamaño de la región a extraer
    half_width = int(x * factor / 2)
    half_height = int(y * factor / 2)
    
    # Calcular los límites de la región
    x_start = max(0, center_x - half_width)
    x_end = min(x, center_x + half_width)
    y_start = max(0, center_y - half_height)
    y_end = min(y, center_y + half_height)
    
    # Extraer la región (recorte)
    img_cropped = img[x_start:x_end, y_start:y_end]
    
    # Redimensionar la región recortada al tamaño original para simular el zoom
    # Convertir a formato de 8 bits para PIL
    img_cropped_8bit = (np.clip(img_cropped, 0, 1) * 255).astype(np.uint8)
    
    # Manejar imágenes en escala de grises vs color
    if len(img_cropped_8bit.shape) == 2:
        # Escala de grises
        img_pil = Image.fromarray(img_cropped_8bit, mode='L')
    else:
        # Color
        img_pil = Image.fromarray(img_cropped_8bit)
    
    # Redimensionar al tamaño original usando interpolación de alta calidad
    img_pil_resized = img_pil.resize((y, x), Image.LANCZOS)
    
    # Convertir de vuelta a numpy array y normalizar a [0, 1]
    img_zoomed = np.array(img_pil_resized).astype(np.float32) / 255.0
    
    # Si la imagen original era en escala de grises pero tenía 3 dimensiones,
    # mantener esa estructura
    if len(original_shape) == 3 and len(img_zoomed.shape) == 2:
        img_zoomed = np.stack([img_zoomed] * original_shape[2], axis=-1)
    
    return img_zoomed

def fusion_images(img_base, img_fusion, factor):
    '''
    Función que fusiona dos imágenes con transparencia
    Las imágenes deben tener las mismas dimensiones
    
    Parameters:
    -----------
    img_base : numpy.ndarray
        Imagen base sobre la que se fusionará
    img_fusion : numpy.ndarray
        Imagen que se fusionará sobre la base
    factor : float
        Factor de transparencia (0-1). 
        0 = solo img_base, 1 = solo img_fusion, 0.5 = 50/50
    
    Returns:
    --------
    numpy.ndarray
        Imagen fusionada
    '''
    # Verificar que ambas imágenes tengan las mismas dimensiones
    if img_base.shape != img_fusion.shape:
        raise ValueError(f"Las imágenes deben tener las mismas dimensiones. "
                        f"Base: {img_base.shape}, Fusión: {img_fusion.shape}")
    
    # Crear una copia para no modificar la original
    img_result = np.copy(img_base)
    
    # Aplicar la fusión usando operaciones vectorizadas (mucho más rápido)
    img_result = img_base * (1 - factor) + img_fusion * factor
    
    # Asegurar que los valores estén en el rango [0, 1]
    img_result = np.clip(img_result, 0, 1)
    
    return img_result