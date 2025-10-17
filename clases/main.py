import pygame 
import sys
# Inicializar pygame
pygame.init()


def mostrar_rectangulo():
    # Dimensiones
    ANCHO = 250
    ALTO = 400
    
    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AZUL = (0, 0, 255)

    dibujar_rectangulo = False

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dibujar_rectangulo = True

        # Dibujar
        if dibujar_rectangulo:
            pygame.draw.rect(pantalla, ROJO, (270, 190, 150, 100))
        pygame.display.flip()


def mostrar_circulo():

    # Dimensiones
    ANCHO = 250
    ALTO = 400
    
    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    AZUL = (0, 120, 255)
    GRIS = (200, 200, 200)

    # Control del círculo
    dibujar_circulo = False

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()      
                
        dibujar_circulo = True

        # Círculo (si fue activado)
        if dibujar_circulo:
            pygame.draw.circle(pantalla, AZUL, (ANCHO // 2, ALTO // 2 + 50), 50)

        pygame.display.flip()


# Clase Boton
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, color_texto=(255, 255, 255), fuente=None):
        """
        Constructor de la clase Boton
        :param x: posición X del botón
        :param y: posición Y del botón
        :param ancho: ancho del botón
        :param alto: alto del botón
        :param texto: texto que se mostrará en el botón
        :param color_normal: color normal del botón (tuple RGB)
        :param color_hover: color cuando el mouse pasa sobre el botón
        :param color_texto: color del texto (tuple RGB)
        :param fuente: objeto pygame.font.Font o None
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 36)
        self.hover = False

    def dibujar(self, pantalla):
        """Dibuja el botón en pantalla."""
        color_actual = self.color_hover if self.hover else self.color_normal
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)

        # Renderizar texto centrado
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def actualizar(self, eventos):
        """Actualiza el estado del botón (detecta hover y clics)."""
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.hover:
                    return True  # Retorna True si se hace clic sobre el botón
            
        return False

# ---------------------------
# Ejemplo de uso
# ---------------------------
if __name__ == "__main__":
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ejemplo de Botones con POO y Pygame")
    reloj = pygame.time.Clock()

    # Crear un botón
    
    boton_circulo = Boton(30, 50, 200, 60, "CIRCULO", (0, 120, 250), (0, 180, 255))
    boton_rectangulo = Boton(250, 50, 200, 60, "RECTANGULO", (200, 50, 50), (255, 80, 80))
    boton_poligono = Boton(470, 50, 200, 60, "POLIGONO", (50, 200, 50), (80, 255, 80))
    ejecutando = True
    while ejecutando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Actualizar botones
        if boton_circulo.actualizar(eventos):
            mostrar_circulo()

        if boton_rectangulo.actualizar(eventos):
            mostrar_rectangulo()

        # Dibujar fondo y botones
        pantalla.fill((30, 30, 30))
        boton_rectangulo.dibujar(pantalla)
        #boton_salir.dibujar(pantalla)
        boton_circulo.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()