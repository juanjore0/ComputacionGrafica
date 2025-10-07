"""
Visor de Imágenes Interactivo
Autor: [Tu nombre]
Fecha: Octubre 2025
Descripción: Aplicación de escritorio para visualización y transformación de imágenes
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSlider, QLineEdit,
                             QFileDialog, QGroupBox, QCheckBox, QRadioButton,
                             QSpinBox, QMessageBox, QComboBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

# Importar las librerías personalizadas
from Transformaciones import *
from image_processor import *


class ImageViewer(QMainWindow):
    """Clase principal del visor de imágenes"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Imágenes")
        self.setGeometry(100, 100, 1400, 800)
        
        # Variables de estado
        self.img_original = None
        self.img_actual = None
        self.img_fusion = None
        self.ruta_imagen = ""
        
        self.initUI()
        
    def initUI(self):
        """Inicializa la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel izquierdo (visualización de imagen)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 7)
        
        # Panel derecho (controles)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 3)
        
    def create_left_panel(self):
        """Crea el panel izquierdo con la visualización de imagen"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Título
        titulo = QLabel("VISOR DE IMÁGENES")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Campo de ruta de archivo
        ruta_layout = QHBoxLayout()
        ruta_label = QLabel("Archivo de imagen:")
        self.ruta_texto = QLineEdit()
        self.ruta_texto.setReadOnly(True)
        ruta_layout.addWidget(ruta_label)
        ruta_layout.addWidget(self.ruta_texto)
        layout.addLayout(ruta_layout)
        
        # Botones principales
        botones_layout = QHBoxLayout()
        btn_explorar = QPushButton("EXPLORAR")
        btn_cargar = QPushButton("CARGAR")
        btn_fusion = QPushButton("FUSIONAR")
        
        btn_explorar.clicked.connect(self.explorar_imagen)
        btn_cargar.clicked.connect(self.cargar_imagen)
        btn_fusion.clicked.connect(self.fusionar_imagenes)
        
        botones_layout.addWidget(btn_explorar)
        botones_layout.addWidget(btn_cargar)
        botones_layout.addWidget(btn_fusion)
        layout.addLayout(botones_layout)
        
        # Área de visualización de imagen
        self.imagen_label = QLabel()
        self.imagen_label.setAlignment(Qt.AlignCenter)
        self.imagen_label.setStyleSheet("background-color: #2b2b2b; border: 2px solid #555;")
        self.imagen_label.setMinimumSize(800, 500)
        self.imagen_label.setText("No hay imagen cargada")
        self.imagen_label.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 16px;")
        
        scroll = QScrollArea()
        scroll.setWidget(self.imagen_label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Botones inferiores
        botones_inf_layout = QHBoxLayout()
        btn_actualizar = QPushButton("ACTUALIZAR")
        btn_zoom = QPushButton("ZOOM")
        btn_guardar = QPushButton("GUARDAR")
        
        btn_actualizar.clicked.connect(self.actualizar_imagen)
        btn_zoom.clicked.connect(self.aplicar_zoom)
        btn_guardar.clicked.connect(self.guardar_imagen)
        
        botones_inf_layout.addWidget(btn_actualizar)
        botones_inf_layout.addWidget(btn_zoom)
        botones_inf_layout.addWidget(btn_guardar)
        layout.addLayout(botones_inf_layout)
        
        return panel
    
    def create_right_panel(self):
        """Crea el panel derecho con todos los controles"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Scroll para los controles
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Control de Brillo
        brillo_group = self.create_slider_control("Brillo", -1.0, 1.0, 0.0)
        self.slider_brillo = brillo_group['slider']
        self.spin_brillo = brillo_group['spin']
        scroll_layout.addWidget(brillo_group['widget'])
        
        # Control de Contraste
        contraste_group = self.create_slider_control("Contraste", 0.1, 3.0, 1.0)
        self.slider_contraste = contraste_group['slider']
        self.spin_contraste = contraste_group['spin']
        scroll_layout.addWidget(contraste_group['widget'])
        
        # Control de Rotación
        rotacion_group = self.create_slider_control("Rotación", 0, 360, 0, is_int=True)
        self.slider_rotacion = rotacion_group['slider']
        self.spin_rotacion = rotacion_group['spin']
        scroll_layout.addWidget(rotacion_group['widget'])
        
        # Control de Transparencia (para fusión)
        transparencia_group = self.create_slider_control("Transparencia Fusión", 0.0, 1.0, 0.5)
        self.slider_transparencia = transparencia_group['slider']
        self.spin_transparencia = transparencia_group['spin']
        scroll_layout.addWidget(transparencia_group['widget'])
        
        # Control de Binarización
        binarizar_group = self.create_slider_control("Umbral Binarización", 0.0, 1.0, 0.5)
        self.slider_binarizar = binarizar_group['slider']
        self.spin_binarizar = binarizar_group['spin']
        scroll_layout.addWidget(binarizar_group['widget'])
        
        # Filtros de zonas
        zonas_group = QGroupBox("Filtros de Zona")
        zonas_layout = QVBoxLayout()
        self.radio_claras = QRadioButton("Zonas Claras")
        self.radio_oscuras = QRadioButton("Zonas Oscuras")
        self.radio_normal = QRadioButton("Normal")
        self.radio_normal.setChecked(True)
        zonas_layout.addWidget(self.radio_normal)
        zonas_layout.addWidget(self.radio_claras)
        zonas_layout.addWidget(self.radio_oscuras)
        zonas_group.setLayout(zonas_layout)
        scroll_layout.addWidget(zonas_group)
        
        # Canales RGB
        rgb_group = QGroupBox("Canales RGB")
        rgb_layout = QVBoxLayout()
        self.check_red = QCheckBox("Red (Rojo)")
        self.check_green = QCheckBox("Green (Verde)")
        self.check_blue = QCheckBox("Blue (Azul)")
        self.check_red.setChecked(True)
        self.check_green.setChecked(True)
        self.check_blue.setChecked(True)
        rgb_layout.addWidget(self.check_red)
        rgb_layout.addWidget(self.check_green)
        rgb_layout.addWidget(self.check_blue)
        rgb_group.setLayout(rgb_layout)
        scroll_layout.addWidget(rgb_group)
        
        # Canales CMY
        cmy_group = QGroupBox("Canales CMY")
        cmy_layout = QVBoxLayout()
        self.check_cyan = QCheckBox("Cyan")
        self.check_magenta = QCheckBox("Magenta")
        self.check_yellow = QCheckBox("Yellow (Amarillo)")
        cmy_layout.addWidget(self.check_cyan)
        cmy_layout.addWidget(self.check_magenta)
        cmy_layout.addWidget(self.check_yellow)
        cmy_group.setLayout(cmy_layout)
        scroll_layout.addWidget(cmy_group)
        
        # Opciones adicionales
        opciones_group = QGroupBox("Opciones Adicionales")
        opciones_layout = QVBoxLayout()
        self.check_negativo = QCheckBox("Negativo")
        self.check_binarizar = QCheckBox("Aplicar Binarización")
        self.check_histograma = QCheckBox("Visualizar Histograma")
        opciones_layout.addWidget(self.check_negativo)
        opciones_layout.addWidget(self.check_binarizar)
        opciones_layout.addWidget(self.check_histograma)
        
        self.check_histograma.stateChanged.connect(self.toggle_histograma)
        
        opciones_group.setLayout(opciones_layout)
        scroll_layout.addWidget(opciones_group)
        
        # Botón de restablecer
        btn_restablecer = QPushButton("RESTABLECER")
        btn_restablecer.clicked.connect(self.restablecer_imagen)
        scroll_layout.addWidget(btn_restablecer)
        
        scroll_layout.addStretch()
        
        return panel
    
    def create_slider_control(self, nombre, min_val, max_val, default_val, is_int=False):
        """Crea un control con slider y spinbox"""
        group = QGroupBox(nombre)
        layout = QVBoxLayout()
        
        # Layout horizontal para el slider y el spinbox
        control_layout = QHBoxLayout()
        
        # Slider
        slider = QSlider(Qt.Horizontal)
        if is_int:
            slider.setMinimum(int(min_val))
            slider.setMaximum(int(max_val))
            slider.setValue(int(default_val))
        else:
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default_val * 100))
        
        # SpinBox
        if is_int:
            spin = QSpinBox()
            spin.setMinimum(int(min_val))
            spin.setMaximum(int(max_val))
            spin.setValue(int(default_val))
        else:
            spin = QSpinBox()
            spin.setMinimum(int(min_val * 100))
            spin.setMaximum(int(max_val * 100))
            spin.setValue(int(default_val * 100))
            spin.setSuffix(" %")
        
        # Conectar slider y spinbox
        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        
        control_layout.addWidget(slider)
        control_layout.addWidget(spin)
        layout.addLayout(control_layout)
        
        group.setLayout(layout)
        
        return {
            'widget': group,
            'slider': slider,
            'spin': spin
        }
    
    def explorar_imagen(self):
        """Abre un diálogo para seleccionar una imagen"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp);;Todos los archivos (*.*)"
        )
        if archivo:
            self.ruta_imagen = archivo
            self.ruta_texto.setText(archivo)
    
    def cargar_imagen(self):
        """Carga la imagen seleccionada"""
        if not self.ruta_imagen:
            QMessageBox.warning(self, "Advertencia", "Primero selecciona una imagen")
            return
        
        try:
            self.img_original = create_img(self.ruta_imagen)
            self.img_actual = np.copy(self.img_original)
            self.mostrar_imagen(self.img_actual)
            QMessageBox.information(self, "Éxito", "Imagen cargada correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar la imagen: {str(e)}")
    
    def mostrar_imagen(self, img):
        """Muestra la imagen en el QLabel"""
        if img is None:
            return
        
        # Convertir imagen de numpy a QImage
        img_display = np.copy(img)
        
        # Asegurar que los valores estén en el rango [0, 1]
        img_display = np.clip(img_display, 0, 1)
        
        # Convertir a 8 bits
        img_display = (img_display * 255).astype(np.uint8)
        
        # Manejar imágenes en escala de grises
        if len(img_display.shape) == 2:
            height, width = img_display.shape
            bytes_per_line = width
            q_img = QImage(img_display.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:
            height, width, channel = img_display.shape
            bytes_per_line = 3 * width
            q_img = QImage(img_display.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        
        # Escalar la imagen para que quepa en el label manteniendo la proporción
        scaled_pixmap = pixmap.scaled(self.imagen_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imagen_label.setPixmap(scaled_pixmap)
    
    def actualizar_imagen(self):
        """Aplica todas las transformaciones seleccionadas"""
        if self.img_original is None:
            QMessageBox.warning(self, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Iniciar con la imagen original
            img = np.copy(self.img_original)
            
            # Aplicar brillo
            brillo_val = self.slider_brillo.value() / 100.0
            if brillo_val != 0:
                img = brightness_adjust(img, brillo_val)
            
            # Aplicar contraste (usando ajuste de claridad u oscuridad)
            contraste_val = self.slider_contraste.value() / 100.0
            if contraste_val != 1.0:
                if contraste_val > 1.0:
                    img = contrast_adjust_brightness(img, contraste_val)
                else:
                    img = contrast_adjust_darkness(img, contraste_val)
            
            # Aplicar rotación
            angulo = self.spin_rotacion.value()
            if angulo != 0:
                img = rotate(img, angulo)
            
            # Aplicar canales RGB
            if not self.check_red.isChecked():
                img[:,:,0] = 0
            if not self.check_green.isChecked():
                img[:,:,1] = 0
            if not self.check_blue.isChecked():
                img[:,:,2] = 0
            
            # Aplicar canales CMY
            if self.check_cyan.isChecked():
                img[:,:,0] = 0  # Sin rojo = cyan
            if self.check_magenta.isChecked():
                img[:,:,1] = 0  # Sin verde = magenta
            if self.check_yellow.isChecked():
                img[:,:,2] = 0  # Sin azul = amarillo
            
            # Aplicar zonas claras/oscuras
            if self.radio_claras.isChecked():
                img_gray = gris(img)
                mascara = img_gray > 0.5
                img = img * mascara[:,:,np.newaxis]
            elif self.radio_oscuras.isChecked():
                img_gray = gris(img)
                mascara = img_gray <= 0.5
                img = img * mascara[:,:,np.newaxis]
            
            # Aplicar negativo
            if self.check_negativo.isChecked():
                img = invert_color(img)
            
            # Aplicar binarización
            if self.check_binarizar.isChecked():
                umbral = self.slider_binarizar.value() / 100.0
                img = binary(img, umbral)
            
            # Aplicar fusión si hay imagen secundaria
            if self.img_fusion is not None:
                factor = self.slider_transparencia.value() / 100.0
                img = fusion_images(img, self.img_fusion, factor)
            
            # Asegurar que los valores están en el rango correcto
            img = np.clip(img, 0, 1)
            
            self.img_actual = img
            self.mostrar_imagen(img)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar transformaciones: {str(e)}")
    
    def fusionar_imagenes(self):
        """Permite seleccionar una segunda imagen para fusionar"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen para Fusionar",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp)"
        )
        if archivo:
            try:
                img_temp = create_img(archivo)
                
                # Redimensionar la imagen de fusión si es necesario
                if self.img_original is not None:
                    if img_temp.shape != self.img_original.shape:
                        # Redimensionar usando PIL
                        img_pil = Image.fromarray((img_temp * 255).astype(np.uint8))
                        img_pil = img_pil.resize((self.img_original.shape[1], self.img_original.shape[0]))
                        img_temp = np.array(img_pil).astype(np.float32) / 255.0
                
                self.img_fusion = img_temp
                QMessageBox.information(self, "Éxito", "Imagen para fusión cargada. Presiona ACTUALIZAR para aplicar.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar imagen de fusión: {str(e)}")
    
    def aplicar_zoom(self):
        """Aplica zoom a la imagen"""
        if self.img_actual is None:
            QMessageBox.warning(self, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Factor de zoom fijo de 0.5 (50% del centro)
            img_zoom = zoom(self.img_actual, 0.5)
            self.img_actual = img_zoom
            self.mostrar_imagen(img_zoom)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar zoom: {str(e)}")
    
    def guardar_imagen(self):
        """Guarda la imagen actual"""
        if self.img_actual is None:
            QMessageBox.warning(self, "Advertencia", "No hay imagen para guardar")
            return
        
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Imagen",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )
        if archivo:
            try:
                # Convertir a 8 bits
                img_save = (np.clip(self.img_actual, 0, 1) * 255).astype(np.uint8)
                
                # Guardar usando PIL
                if len(img_save.shape) == 2:
                    img_pil = Image.fromarray(img_save, mode='L')
                else:
                    img_pil = Image.fromarray(img_save)
                
                img_pil.save(archivo)
                QMessageBox.information(self, "Éxito", "Imagen guardada correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar la imagen: {str(e)}")
    
    def restablecer_imagen(self):
        """Restablece la imagen a su estado original"""
        if self.img_original is None:
            return
        
        self.img_actual = np.copy(self.img_original)
        self.img_fusion = None
        
        # Restablecer controles
        self.slider_brillo.setValue(0)
        self.slider_contraste.setValue(100)
        self.slider_rotacion.setValue(0)
        self.slider_transparencia.setValue(50)
        self.slider_binarizar.setValue(50)
        
        self.radio_normal.setChecked(True)
        self.check_red.setChecked(True)
        self.check_green.setChecked(True)
        self.check_blue.setChecked(True)
        self.check_cyan.setChecked(False)
        self.check_magenta.setChecked(False)
        self.check_yellow.setChecked(False)
        self.check_negativo.setChecked(False)
        self.check_binarizar.setChecked(False)
        
        self.mostrar_imagen(self.img_actual)
    
    def toggle_histograma(self, state):
        """Muestra u oculta el histograma"""
        if state == Qt.Checked:
            if self.img_actual is not None:
                self.mostrar_histograma()
            else:
                self.check_histograma.setChecked(False)
                QMessageBox.warning(self, "Advertencia", "Primero carga una imagen")
    
    def mostrar_histograma(self):
        """Muestra el histograma de la imagen actual"""
        if self.img_actual is None:
            return
        
        try:
            RGB_Histogram(self.img_actual)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar histograma: {str(e)}")


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()