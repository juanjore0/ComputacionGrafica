"""
Visor de Imágenes Interactivo - PyQt5
Autor: [Tu nombre]
Fecha: Octubre 2025
Descripción: Aplicación de escritorio para visualización y transformación de imágenes
Cumple con todos los requerimientos del proyecto académico
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
                             QSpinBox, QMessageBox, QComboBox, QScrollArea,
                             QDoubleSpinBox, QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PIL import Image

# Importar las librerías personalizadas
from Transformaciones import *
from image_processor import *


class ImageViewer(QMainWindow):
    """Clase principal del visor de imágenes"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Imágenes")
        self.setGeometry(50, 50, 1400, 800)
        
        # Variables de estado
        self.img_original = None
        self.img_actual = None
        self.img_fusion = None
        self.ruta_imagen = ""
        self.histograma_window = None
        
        # Coordenadas para zoom
        self.zoom_x = 0
        self.zoom_y = 0
        
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
        
        # Aplicar estilos
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
    def create_left_panel(self):
        """Crea el panel izquierdo con la visualización de imagen"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Título
        titulo = QLabel("VISOR DE IMÁGENES")
        titulo.setFont(QFont("Arial", 24, QFont.Bold))
        titulo.setStyleSheet("color: #333; padding: 10px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Campo de ruta de archivo
        ruta_layout = QHBoxLayout()
        ruta_label = QLabel("Archivo de imagen:")
        ruta_label.setFont(QFont("Arial", 11))
        self.ruta_texto = QLineEdit()
        self.ruta_texto.setReadOnly(True)
        self.ruta_texto.setStyleSheet("background-color: white; padding: 5px;")
        ruta_layout.addWidget(ruta_label)
        ruta_layout.addWidget(self.ruta_texto)
        layout.addLayout(ruta_layout)
        
        # Botones principales superiores
        botones_layout = QHBoxLayout()
        btn_explorar = QPushButton("EXPLORAR")
        btn_cargar = QPushButton("CARGAR")
        btn_fusion = QPushButton("FUSIONAR IMÁGENES")
        
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
        self.imagen_label.setMinimumSize(800, 450)
        self.imagen_label.setText("No hay imagen cargada")
        self.imagen_label.setStyleSheet("""
            background-color: #2b2b2b; 
            color: white; 
            font-size: 16px;
            border: 3px solid #555;
            border-radius: 5px;
        """)
        
        scroll = QScrollArea()
        scroll.setWidget(self.imagen_label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Botones inferiores
        botones_inf_layout = QHBoxLayout()
        btn_actualizar = QPushButton("ACTUALIZAR")
        btn_zoom = QPushButton("ZOOM")
        btn_guardar = QPushButton("GUARDAR")
        btn_restablecer = QPushButton("RESTABLECER")
        
        btn_actualizar.clicked.connect(self.actualizar_imagen)
        btn_zoom.clicked.connect(self.aplicar_zoom)
        btn_guardar.clicked.connect(self.guardar_imagen)
        btn_restablecer.clicked.connect(self.restablecer_imagen)
        
        btn_restablecer.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        botones_inf_layout.addWidget(btn_actualizar)
        botones_inf_layout.addWidget(btn_zoom)
        botones_inf_layout.addWidget(btn_guardar)
        botones_inf_layout.addWidget(btn_restablecer)
        layout.addLayout(botones_inf_layout)
        
        return panel
    
    def create_right_panel(self):
        """Crea el panel derecho con todos los controles"""
        panel = QWidget()
        main_layout = QVBoxLayout()
        panel.setLayout(main_layout)
        
        # Título del panel
        panel_title = QLabel("CONTROLES DE TRANSFORMACIÓN")
        panel_title.setFont(QFont("Arial", 12, QFont.Bold))
        panel_title.setAlignment(Qt.AlignCenter)
        panel_title.setStyleSheet("color: #333; padding: 5px;")
        main_layout.addWidget(panel_title)
        
        # Scroll para los controles
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # === CONTROLES DE AJUSTE ===
        ajustes_group = QGroupBox("Ajustes de Imagen")
        ajustes_layout = QVBoxLayout()
        
        # Control de Brillo
        self.slider_brillo, self.spin_brillo = self.create_slider_control(
            "Brillo:", -100, 100, 0, ajustes_layout
        )
        
        # Control de Contraste
        self.slider_contraste, self.spin_contraste = self.create_slider_control(
            "Contraste:", 10, 300, 100, ajustes_layout, suffix="%"
        )
        
        # Control de Rotación
        self.slider_rotacion, self.spin_rotacion = self.create_slider_control(
            "Rotación:", 0, 360, 0, ajustes_layout, suffix="°"
        )
        
        ajustes_group.setLayout(ajustes_layout)
        scroll_layout.addWidget(ajustes_group)
        
        # === FUSIÓN DE IMÁGENES ===
        fusion_group = QGroupBox("Fusión de Imágenes")
        fusion_layout = QVBoxLayout()
        
        # Control de Transparencia
        self.slider_transparencia, self.spin_transparencia = self.create_slider_control(
            "Transparencia:", 0, 100, 50, fusion_layout, suffix="%"
        )
        
        fusion_group.setLayout(fusion_layout)
        scroll_layout.addWidget(fusion_group)
        
        # === BINARIZACIÓN ===
        binarizar_group = QGroupBox("Binarización")
        binarizar_layout = QVBoxLayout()
        
        # Checkbox para activar binarización
        self.check_binarizar = QCheckBox("Aplicar Binarización")
        binarizar_layout.addWidget(self.check_binarizar)
        
        # Control de Umbral
        self.slider_binarizar, self.spin_binarizar = self.create_slider_control(
            "Umbral:", 0, 100, 50, binarizar_layout, suffix="%"
        )
        
        binarizar_group.setLayout(binarizar_layout)
        scroll_layout.addWidget(binarizar_group)
        
        # === FILTROS DE ZONA ===
        zonas_group = QGroupBox("Filtros de Zona")
        zonas_layout = QVBoxLayout()
        
        self.radio_normal = QRadioButton("Normal (sin filtro)")
        self.radio_claras = QRadioButton("Zonas Claras")
        self.radio_oscuras = QRadioButton("Zonas Oscuras")
        self.radio_normal.setChecked(True)
        
        zonas_layout.addWidget(self.radio_normal)
        zonas_layout.addWidget(self.radio_claras)
        zonas_layout.addWidget(self.radio_oscuras)
        
        zonas_group.setLayout(zonas_layout)
        scroll_layout.addWidget(zonas_group)
        
        # === CANALES RGB ===
        rgb_group = QGroupBox("Canales RGB")
        rgb_layout = QHBoxLayout()
        
        self.check_red = QCheckBox("Red")
        self.check_green = QCheckBox("Green")
        self.check_blue = QCheckBox("Blue")
        
        self.check_red.setChecked(True)
        self.check_green.setChecked(True)
        self.check_blue.setChecked(True)
        
        rgb_layout.addWidget(self.check_red)
        rgb_layout.addWidget(self.check_green)
        rgb_layout.addWidget(self.check_blue)
        
        rgb_group.setLayout(rgb_layout)
        scroll_layout.addWidget(rgb_group)
        
        # === CANALES CMY ===
        cmy_group = QGroupBox("Canales CMY")
        cmy_layout = QHBoxLayout()
        
        self.check_cyan = QCheckBox("Cyan")
        self.check_magenta = QCheckBox("Magenta")
        self.check_yellow = QCheckBox("Yellow")
        
        cmy_layout.addWidget(self.check_cyan)
        cmy_layout.addWidget(self.check_magenta)
        cmy_layout.addWidget(self.check_yellow)
        
        cmy_group.setLayout(cmy_layout)
        scroll_layout.addWidget(cmy_group)
        
        # === OPCIONES ADICIONALES ===
        opciones_group = QGroupBox("Opciones Adicionales")
        opciones_layout = QVBoxLayout()
        
        self.check_negativo = QCheckBox("Negativo Imagen")
        self.check_histograma = QCheckBox("Visualizar Histograma")
        
        self.check_histograma.stateChanged.connect(self.toggle_histograma)
        
        opciones_layout.addWidget(self.check_negativo)
        opciones_layout.addWidget(self.check_histograma)
        
        opciones_group.setLayout(opciones_layout)
        scroll_layout.addWidget(opciones_group)
        
        # === ZOOM ===
        zoom_group = QGroupBox("Configuración de Zoom")
        zoom_layout = QGridLayout()
        
        zoom_layout.addWidget(QLabel("Punto central X:"), 0, 0)
        self.spin_zoom_x = QSpinBox()
        self.spin_zoom_x.setRange(0, 5000)
        self.spin_zoom_x.setValue(0)
        zoom_layout.addWidget(self.spin_zoom_x, 0, 1)
        
        zoom_layout.addWidget(QLabel("Punto central Y:"), 1, 0)
        self.spin_zoom_y = QSpinBox()
        self.spin_zoom_y.setRange(0, 5000)
        self.spin_zoom_y.setValue(0)
        zoom_layout.addWidget(self.spin_zoom_y, 1, 1)
        
        # Control de factor de zoom
        zoom_layout.addWidget(QLabel("Factor de zoom:"), 2, 0)
        self.combo_zoom_factor = QComboBox()
        self.combo_zoom_factor.addItems([
            "2x (factor 0.5)",
            "3x (factor 0.33)",
            "4x (factor 0.25)",
            "5x (factor 0.2)",
            "8x (factor 0.125)"
        ])
        self.combo_zoom_factor.setCurrentIndex(0)  # 2x por defecto
        zoom_layout.addWidget(self.combo_zoom_factor, 2, 1)
        
        # Botón de ayuda
        btn_zoom_help = QPushButton("?")
        btn_zoom_help.setMaximumWidth(30)
        btn_zoom_help.clicked.connect(self.mostrar_ayuda_zoom)
        btn_zoom_help.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        zoom_layout.addWidget(btn_zoom_help, 2, 2)
        
        zoom_group.setLayout(zoom_layout)
        scroll_layout.addWidget(zoom_group)
        
        scroll_layout.addStretch()
        
        return panel
    
    def create_slider_control(self, label_text, min_val, max_val, default_val, parent_layout, suffix=""):
        """Crea un control con slider y spinbox sincronizados"""
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        
        # Label
        label = QLabel(label_text)
        label.setMinimumWidth(120)
        layout.addWidget(label)
        
        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        layout.addWidget(slider)
        
        # SpinBox
        spin = QSpinBox()
        spin.setMinimum(min_val)
        spin.setMaximum(max_val)
        spin.setValue(default_val)
        if suffix:
            spin.setSuffix(suffix)
        spin.setMinimumWidth(80)
        layout.addWidget(spin)
        
        # Conectar slider y spinbox
        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        
        parent_layout.addWidget(container)
        
        return slider, spin
    
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
            print(f"Imagen seleccionada: {archivo}")
    
    def cargar_imagen(self):
        """Carga la imagen seleccionada"""
        if not self.ruta_imagen:
            QMessageBox.warning(self, "Advertencia", "Primero selecciona una imagen usando el botón EXPLORAR")
            return
        
        try:
            self.img_original = create_img(self.ruta_imagen)
            self.img_actual = np.copy(self.img_original)
            
            # Ajustar los límites de los SpinBox de zoom según el tamaño de la imagen
            altura, ancho = self.img_original.shape[:2]
            self.spin_zoom_x.setMaximum(altura - 1)
            self.spin_zoom_y.setMaximum(ancho - 1)
            
            # Establecer valores iniciales en el centro
            self.spin_zoom_x.setValue(altura // 2)
            self.spin_zoom_y.setValue(ancho // 2)
            
            self.mostrar_imagen(self.img_actual)
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Imagen cargada correctamente\n"
                f"Dimensiones: {altura} x {ancho} píxeles"
            )
            print(f"Imagen cargada: {self.img_original.shape}")
            print(f"Límites de zoom ajustados: X(0-{altura-1}), Y(0-{ancho-1})")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar la imagen:\n{str(e)}")
            print(f"Error: {e}")
    
    def mostrar_imagen(self, img):
        """Muestra la imagen en el QLabel"""
        if img is None:
            return
        
        try:
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
            scaled_pixmap = pixmap.scaled(
                self.imagen_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.imagen_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Error al mostrar imagen: {e}")
            QMessageBox.critical(self, "Error", f"Error al mostrar la imagen:\n{str(e)}")
    
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
                print(f"Brillo aplicado: {brillo_val}")
            
            # Aplicar contraste
            contraste_val = self.slider_contraste.value() / 100.0
            if contraste_val != 1.0:
                if contraste_val > 1.0:
                    img = contrast_adjust_brightness(img, contraste_val)
                else:
                    img = contrast_adjust_darkness(img, contraste_val)
                print(f"Contraste aplicado: {contraste_val}")
            
            # Aplicar rotación
            angulo = self.spin_rotacion.value()
            if angulo != 0:
                img = rotate(img, angulo)
                print(f"Rotación aplicada: {angulo}°")
            
            # Aplicar canales RGB
            if not self.check_red.isChecked():
                img[:,:,0] = 0
                print("Canal rojo desactivado")
            if not self.check_green.isChecked():
                img[:,:,1] = 0
                print("Canal verde desactivado")
            if not self.check_blue.isChecked():
                img[:,:,2] = 0
                print("Canal azul desactivado")
            
            # Aplicar canales CMY
            if self.check_cyan.isChecked():
                img[:,:,0] = 0  # Sin rojo = cyan
                print("Canal cyan activado")
            if self.check_magenta.isChecked():
                img[:,:,1] = 0  # Sin verde = magenta
                print("Canal magenta activado")
            if self.check_yellow.isChecked():
                img[:,:,2] = 0  # Sin azul = amarillo
                print("Canal yellow activado")
            
            # Aplicar filtros de zona
            if self.radio_claras.isChecked():
                img_gray = gris(img)
                mascara = img_gray > 0.5
                img = img * mascara[:,:,np.newaxis]
                print("Filtro zonas claras aplicado")
            elif self.radio_oscuras.isChecked():
                img_gray = gris(img)
                mascara = img_gray <= 0.5
                img = img * mascara[:,:,np.newaxis]
                print("Filtro zonas oscuras aplicado")
            
            # Aplicar negativo
            if self.check_negativo.isChecked():
                img = invert_color(img)
                print("Negativo aplicado")
            
            # Aplicar binarización
            if self.check_binarizar.isChecked():
                umbral = self.slider_binarizar.value() / 100.0
                img = binary(img, umbral)
                print(f"Binarización aplicada con umbral: {umbral}")
            
            # Aplicar fusión si hay imagen secundaria
            if self.img_fusion is not None:
                factor = self.slider_transparencia.value() / 100.0
                img = fusion_images(img, self.img_fusion, factor)
                print(f"Fusión aplicada con transparencia: {factor}")
            
            # Asegurar que los valores están en el rango correcto
            img = np.clip(img, 0, 1)
            
            self.img_actual = img
            self.mostrar_imagen(img)
            print("Imagen actualizada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar transformaciones:\n{str(e)}")
            print(f"Error en actualizar_imagen: {e}")
            import traceback
            traceback.print_exc()
    
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
                    if img_temp.shape[:2] != self.img_original.shape[:2]:
                        # Redimensionar usando PIL
                        img_pil = Image.fromarray((img_temp * 255).astype(np.uint8))
                        img_pil = img_pil.resize(
                            (self.img_original.shape[1], self.img_original.shape[0]),
                            Image.LANCZOS
                        )
                        img_temp = np.array(img_pil).astype(np.float32) / 255.0
                
                self.img_fusion = img_temp
                QMessageBox.information(
                    self, 
                    "Éxito", 
                    "Imagen para fusión cargada.\n\nAjusta la transparencia y presiona ACTUALIZAR para aplicar la fusión."
                )
                print(f"Imagen de fusión cargada: {self.img_fusion.shape}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar imagen de fusión:\n{str(e)}")
                print(f"Error: {e}")
    
    def aplicar_zoom(self):
        """Aplica zoom a la imagen desde un punto central con factor seleccionable"""
        if self.img_actual is None:
            QMessageBox.warning(self, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Obtener coordenadas del punto central del zoom
            center_x = self.spin_zoom_x.value()
            center_y = self.spin_zoom_y.value()
            
            # Validar que las coordenadas estén dentro de los límites de la imagen
            altura, ancho = self.img_actual.shape[:2]
            
            if center_x >= altura or center_y >= ancho:
                QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    f"Las coordenadas están fuera de los límites de la imagen.\n"
                    f"Tamaño de la imagen: {altura} x {ancho}\n"
                    f"Coordenadas ingresadas: ({center_x}, {center_y})"
                )
                return
            
            # Obtener el factor de zoom desde el ComboBox
            zoom_text = self.combo_zoom_factor.currentText()
            # Extraer el factor del texto "2x (factor 0.5)"
            factor = float(zoom_text.split("factor ")[1].rstrip(")"))
            
            # Aplicar zoom usando la función modificada
            img_zoomed = zoom(self.img_actual, factor, center_x, center_y)
            
            self.img_actual = img_zoomed
            self.mostrar_imagen(img_zoomed)
            
            zoom_level = zoom_text.split(" ")[0]  # Obtener "2x", "3x", etc.
            print(f"Zoom {zoom_level} aplicado desde punto ({center_x}, {center_y})")
            print(f"Dimensión de la imagen: {img_zoomed.shape}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar zoom:\n{str(e)}")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_ayuda_zoom(self):
        """Muestra información sobre cómo usar el zoom"""
        QMessageBox.information(
            self,
            "Ayuda - Zoom",
            "📍 CÓMO USAR EL ZOOM:\n\n"
            "1. Las coordenadas X e Y indican el PUNTO CENTRAL del zoom\n"
            "   (no la esquina superior izquierda)\n\n"
            "2. El factor de zoom indica cuánto se ampliará:\n"
            "   • 2x = Amplía el doble (muestra el 50% de la imagen)\n"
            "   • 4x = Amplía 4 veces (muestra el 25% de la imagen)\n"
            "   • 8x = Amplía 8 veces (muestra el 12.5% de la imagen)\n\n"
            "3. Primero carga una imagen, luego selecciona las coordenadas\n"
            "   del punto donde quieres centrar el zoom\n\n"
            "4. Presiona el botón ZOOM para aplicar\n\n"
            "💡 TIP: Después de aplicar ACTUALIZAR, puedes hacer zoom\n"
            "sobre la imagen transformada"
        )
    
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
                QMessageBox.information(self, "Éxito", f"Imagen guardada correctamente en:\n{archivo}")
                print(f"Imagen guardada: {archivo}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar la imagen:\n{str(e)}")
                print(f"Error: {e}")
    
    def restablecer_imagen(self):
        """Restablece la imagen a su estado original"""
        if self.img_original is None:
            QMessageBox.warning(self, "Advertencia", "No hay imagen cargada")
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
        self.check_histograma.setChecked(False)
        
        # Restablecer zoom al centro
        altura, ancho = self.img_original.shape[:2]
        self.spin_zoom_x.setValue(altura // 2)
        self.spin_zoom_y.setValue(ancho // 2)
        self.combo_zoom_factor.setCurrentIndex(0)
        
        self.mostrar_imagen(self.img_actual)
        QMessageBox.information(self, "Éxito", "Imagen restablecida a su estado original")
        print("Imagen restablecida")
    
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
            # Usar la función de la librería
            RGB_Histogram(self.img_actual)
            print("Histograma mostrado")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar histograma:\n{str(e)}")
            print(f"Error: {e}")


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar el estilo de la aplicación
    app.setStyle('Fusion')
    
    viewer = ImageViewer()
    viewer.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()