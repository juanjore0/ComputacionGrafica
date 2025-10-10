import numpy as np
import matplotlib.pyplot as plt
    
def invert_color(img):
    '''
    Invierte los colores de una img
    '''
    img_invertida = 1 - img
    
    return img_invertida

def red_cape(img):
    '''
    Cambia los colores de una img a rojo
    '''
    img[:,:,0] = 0
    
    return img
    
def green_cape(img):
    '''
    Cambia los colores de una img a verde
    '''
    img[:,:,1] = 0
    
    return img

def blue_cape(img):
    '''
    Cambia los colores de una img a azul
    '''
    img[:,:,2] = 0
    
    return img
    
def join_color(img):
    '''
    Une las capas de color de una img
    '''
    capa_roja = np.copy(img)
    capa_roja[:,:,1] = capa_roja[:,:,2] = 0
    capa_verde = np.copy(img)
    capa_verde[:,:,0] = capa_verde[:,:,2] = 0
    capa_azul = np.copy(img)
    capa_azul[:,:,0] = capa_azul[:,:,1] = 0

    capa_original = capa_roja + capa_verde + capa_azul

    return capa_original
    
def fusion_images(img1, img2):
    '''
    Ecualiza dos imges
    '''
    img_3 = img1 + img2

    return img_3
    
def fusion_images_fix(img1, img2):
    '''
    Fusiona dos imges
    '''

    factor = 0.3

    img_3 = img1*factor + img2*(1-factor)

    return img_3

def equalizate_image(img):
    '''
    Ecualiza una img
    '''
    factor = 0.3

    img_ecualizada = img * factor

    return img_ecualizada

def average(img):
    '''
    Promedia los colores de una img
    '''
    capa_grises = np.mean(img, axis=2) #average

    return capa_grises
    
def average_gray(img):
    '''
    Promedia los colores de una img y la convierte a escala de grises
    '''
    capa_grises = np.mean(img, axis=2) #average

    return capa_grises
    
def luminosity(img):
    '''
    Convierte una img a escala de grises con la tecnica luminosity
    '''
    capa_grises =  0.2989*img[:,:,0] + 0.5870*img[:,:,1] + 0.1140*img[:,:,2] #luminosity

    return  capa_grises
    
def midgray(img):
    '''
    Convierte una img a escala de grises con la tecnica midgray
    '''
    capa_grises = (np.maximum(img[:,:,0], img[:,:,1], img[:,:,2]) + np.minimum(img[:,:,0], img[:,:,1], img[:,:,2])) / 2 # midgray

    img_rgb = np.stack((capa_grises,)*3, axis=-1)
    
    return img_rgb