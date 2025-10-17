"""
Visor de Imágenes Interactivo - PyQt5
Autor: Juan Jose Arango && Valeria Ramirez Muñoz
Descripción: Aplicación de escritorio para visualización y transformación de imágenes
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSlider, QLineEdit,
                             QGroupBox, QCheckBox, QRadioButton,
                             QSpinBox, QComboBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Importar el handler de lógica
from ui_handlers import ImageHandler


class ImageViewer(QMainWindow):
    """Clase principal del visor de imágenes - Solo maneja la UI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Imágenes")
        self.setGeometry(50, 50, 1400, 800)
        
        # Variables de estado (solo referencias, la lógica está en handler)
        self.img_original = None
        self.img_actual = None
        self.img_fusion = None
        self.ruta_imagen = ""
        
        # Inicializar UI
        self.initUI()
        
        # Crear el handler que manejará toda la lógica
        self.handler = ImageHandler(self)
        
        # Conectar eventos después de crear la UI
        self.conectar_eventos()
        
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
        self.aplicar_estilos()
    
    def aplicar_estilos(self):
        """Aplica los estilos CSS a la aplicación"""
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
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
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
        self.btn_explorar = QPushButton("EXPLORAR")
        self.btn_cargar = QPushButton("CARGAR")
        self.btn_fusion = QPushButton("FUSIONAR IMÁGENES")
        
        botones_layout.addWidget(self.btn_explorar)
        botones_layout.addWidget(self.btn_cargar)
        botones_layout.addWidget(self.btn_fusion)
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
        self.btn_actualizar = QPushButton("ACTUALIZAR")
        self.btn_zoom = QPushButton("ZOOM")
        self.btn_guardar = QPushButton("GUARDAR")
        self.btn_restablecer = QPushButton("RESTABLECER")
        
        self.btn_restablecer.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        botones_inf_layout.addWidget(self.btn_actualizar)
        botones_inf_layout.addWidget(self.btn_zoom)
        botones_inf_layout.addWidget(self.btn_guardar)
        botones_inf_layout.addWidget(self.btn_restablecer)
        layout.addLayout(botones_inf_layout)
        
        return panel

    def create_right_panel(self):
        """Crea el panel derecho con todos los controles de transformación"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # ========== CONTROLES BÁSICOS ==========
        grupo_basicos = QGroupBox("CONTROLES BÁSICOS")
        layout_basicos = QVBoxLayout()
        
        # Brillo
        brillo_layout = QHBoxLayout()
        brillo_label = QLabel("Brillo:")
        self.slider_brillo = QSlider(Qt.Horizontal)
        self.slider_brillo.setRange(-100, 100)
        self.slider_brillo.setValue(0)
        self.label_brillo = QLabel("0%")
        brillo_layout.addWidget(brillo_label)
        brillo_layout.addWidget(self.slider_brillo)
        brillo_layout.addWidget(self.label_brillo)
        layout_basicos.addLayout(brillo_layout)
        
        # Contraste
        contraste_layout = QHBoxLayout()
        contraste_label = QLabel("Contraste:")
        self.slider_contraste = QSlider(Qt.Horizontal)
        self.slider_contraste.setRange(0, 200)
        self.slider_contraste.setValue(100)
        self.label_contraste = QLabel("100%")
        contraste_layout.addWidget(contraste_label)
        contraste_layout.addWidget(self.slider_contraste)
        contraste_layout.addWidget(self.label_contraste)
        layout_basicos.addLayout(contraste_layout)
        
        # Rotación
        rotacion_layout = QHBoxLayout()
        rotacion_label = QLabel("Rotación:")
        self.slider_rotacion = QSlider(Qt.Horizontal)
        self.slider_rotacion.setRange(0, 360)
        self.slider_rotacion.setValue(0)
        self.spin_rotacion = QSpinBox()
        self.spin_rotacion.setRange(0, 360)
        self.spin_rotacion.setValue(0)
        self.spin_rotacion.setSuffix("°")
        rotacion_layout.addWidget(rotacion_label)
        rotacion_layout.addWidget(self.slider_rotacion)
        rotacion_layout.addWidget(self.spin_rotacion)
        layout_basicos.addLayout(rotacion_layout)
        
        grupo_basicos.setLayout(layout_basicos)
        layout.addWidget(grupo_basicos)
        
        # ========== CANALES RGB ==========
        grupo_rgb = QGroupBox("CANALES RGB")
        layout_rgb = QHBoxLayout()
        
        self.check_red = QCheckBox("Rojo")
        self.check_green = QCheckBox("Verde")
        self.check_blue = QCheckBox("Azul")
        
        self.check_red.setChecked(True)
        self.check_green.setChecked(True)
        self.check_blue.setChecked(True)
        
        layout_rgb.addWidget(self.check_red)
        layout_rgb.addWidget(self.check_green)
        layout_rgb.addWidget(self.check_blue)
        
        grupo_rgb.setLayout(layout_rgb)
        layout.addWidget(grupo_rgb)
        
        # ========== CANALES CMY ==========
        grupo_cmy = QGroupBox("CANALES CMY")
        layout_cmy = QHBoxLayout()
        
        self.check_cyan = QCheckBox("Cyan")
        self.check_magenta = QCheckBox("Magenta")
        self.check_yellow = QCheckBox("Amarillo")
        
        layout_cmy.addWidget(self.check_cyan)
        layout_cmy.addWidget(self.check_magenta)
        layout_cmy.addWidget(self.check_yellow)
        
        grupo_cmy.setLayout(layout_cmy)
        layout.addWidget(grupo_cmy)
        
        # ========== FILTROS DE ZONA ==========
        grupo_zona = QGroupBox("FILTROS DE ZONA")
        layout_zona = QVBoxLayout()
        
        self.radio_normal = QRadioButton("Normal")
        self.radio_claras = QRadioButton("Zonas Claras")
        self.radio_oscuras = QRadioButton("Zonas Oscuras")
        
        self.radio_normal.setChecked(True)
        
        layout_zona.addWidget(self.radio_normal)
        layout_zona.addWidget(self.radio_claras)
        layout_zona.addWidget(self.radio_oscuras)
        
        grupo_zona.setLayout(layout_zona)
        layout.addWidget(grupo_zona)
        
        # ========== TRANSFORMACIONES ESPECIALES ==========
        grupo_especiales = QGroupBox("TRANSFORMACIONES ESPECIALES")
        layout_especiales = QVBoxLayout()
        
        self.check_negativo = QCheckBox("Negativo")
        self.check_binarizar = QCheckBox("Binarizar")
        
        # Control de binarización
        binarizar_layout = QHBoxLayout()
        binarizar_label = QLabel("Umbral:")
        self.slider_binarizar = QSlider(Qt.Horizontal)
        self.slider_binarizar.setRange(0, 100)
        self.slider_binarizar.setValue(50)
        self.label_binarizar = QLabel("50%")
        binarizar_layout.addWidget(binarizar_label)
        binarizar_layout.addWidget(self.slider_binarizar)
        binarizar_layout.addWidget(self.label_binarizar)
        
        layout_especiales.addWidget(self.check_negativo)
        layout_especiales.addWidget(self.check_binarizar)
        layout_especiales.addLayout(binarizar_layout)
        
        grupo_especiales.setLayout(layout_especiales)
        layout.addWidget(grupo_especiales)
        
        # ========== FUSIÓN DE IMÁGENES ==========
        grupo_fusion = QGroupBox("FUSIÓN DE IMÁGENES")
        layout_fusion = QVBoxLayout()
        
        transparencia_layout = QHBoxLayout()
        transparencia_label = QLabel("Transparencia:")
        self.slider_transparencia = QSlider(Qt.Horizontal)
        self.slider_transparencia.setRange(0, 100)
        self.slider_transparencia.setValue(50)
        self.label_transparencia = QLabel("50%")
        transparencia_layout.addWidget(transparencia_label)
        transparencia_layout.addWidget(self.slider_transparencia)
        transparencia_layout.addWidget(self.label_transparencia)
        
        layout_fusion.addLayout(transparencia_layout)
        
        grupo_fusion.setLayout(layout_fusion)
        layout.addWidget(grupo_fusion)
        
        # ========== ZOOM ==========
        grupo_zoom = QGroupBox("CONTROL DE ZOOM")
        layout_zoom = QGridLayout()
        
        # Coordenadas
        layout_zoom.addWidget(QLabel("Coordenada X:"), 0, 0)
        self.spin_zoom_x = QSpinBox()
        self.spin_zoom_x.setRange(0, 1000)
        self.spin_zoom_x.setValue(0)
        layout_zoom.addWidget(self.spin_zoom_x, 0, 1)
        
        layout_zoom.addWidget(QLabel("Coordenada Y:"), 1, 0)
        self.spin_zoom_y = QSpinBox()
        self.spin_zoom_y.setRange(0, 1000)
        self.spin_zoom_y.setValue(0)
        layout_zoom.addWidget(self.spin_zoom_y, 1, 1)
        
        # Factor de zoom
        layout_zoom.addWidget(QLabel("Factor Zoom:"), 2, 0)
        self.combo_zoom_factor = QComboBox()
        self.combo_zoom_factor.addItems([
            "2x (factor 0.5)",
            "4x (factor 0.25)", 
            "8x (factor 0.125)"
        ])
        layout_zoom.addWidget(self.combo_zoom_factor, 2, 1)
        
        # Botón de ayuda
        self.btn_ayuda_zoom = QPushButton("?")
        self.btn_ayuda_zoom.setMaximumWidth(30)
        layout_zoom.addWidget(self.btn_ayuda_zoom, 2, 2)
        
        grupo_zoom.setLayout(layout_zoom)
        layout.addWidget(grupo_zoom)
        
        # ========== HISTOGRAMA ==========
        grupo_histograma = QGroupBox("HISTOGRAMA")
        layout_histograma = QVBoxLayout()
        
        self.btn_histograma = QPushButton("MOSTRAR HISTOGRAMA RGB")
        layout_histograma.addWidget(self.btn_histograma)
        
        grupo_histograma.setLayout(layout_histograma)
        layout.addWidget(grupo_histograma)
        
        # Espaciador
        layout.addStretch()
        
        return panel

    def conectar_eventos(self):
        """Conecta todos los eventos de la interfaz con sus handlers"""
        # Botones principales
        self.btn_explorar.clicked.connect(self.handler.explorar_imagen)
        self.btn_cargar.clicked.connect(self.handler.cargar_imagen)
        self.btn_fusion.clicked.connect(self.handler.fusionar_imagenes)
        self.btn_actualizar.clicked.connect(self.handler.actualizar_imagen)
        self.btn_zoom.clicked.connect(self.handler.aplicar_zoom)
        self.btn_guardar.clicked.connect(self.handler.guardar_imagen)
        self.btn_restablecer.clicked.connect(self.handler.restablecer_imagen)
        self.btn_ayuda_zoom.clicked.connect(self.handler.mostrar_ayuda_zoom)
        self.btn_histograma.clicked.connect(self.handler.mostrar_histograma)
        
        # Sliders con actualización de labels
        self.slider_brillo.valueChanged.connect(
            lambda v: self.label_brillo.setText(f"{v}%"))
        self.slider_contraste.valueChanged.connect(
            lambda v: self.label_contraste.setText(f"{v}%"))
        self.slider_rotacion.valueChanged.connect(self.spin_rotacion.setValue)
        self.spin_rotacion.valueChanged.connect(self.slider_rotacion.setValue)
        self.slider_transparencia.valueChanged.connect(
            lambda v: self.label_transparencia.setText(f"{v}%"))
        self.slider_binarizar.valueChanged.connect(
            lambda v: self.label_binarizar.setText(f"{v}%"))


def main():
    """Función principal que inicia la aplicación"""
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana principal
    viewer = ImageViewer()
    viewer.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()