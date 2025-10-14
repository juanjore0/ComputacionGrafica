"""
UI Handlers - Módulo de lógica de botones y controles
Contiene toda la lógica de manejo de eventos y transformaciones de imagen
"""

import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image

from Transformaciones import *
from image_processor import *


class ImageHandler:
    """
    Clase que maneja todas las operaciones sobre las imágenes
    y la lógica de los controles de la interfaz
    """
    
    def __init__(self, viewer):
        """
        Inicializa el handler con referencia al viewer principal
        
        Parameters:
        -----------
        viewer : ImageViewer
            Referencia a la ventana principal
        """
        self.viewer = viewer
    
    # ==================== CARGA DE IMÁGENES ====================
    
    def explorar_imagen(self):
        """Abre un diálogo para seleccionar una imagen"""
        archivo, _ = QFileDialog.getOpenFileName(
            self.viewer,
            "Seleccionar Imagen",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp);;Todos los archivos (*.*)"
        )
        if archivo:
            self.viewer.ruta_imagen = archivo
            self.viewer.ruta_texto.setText(archivo)
            print(f"Imagen seleccionada: {archivo}")
    
    def cargar_imagen(self):
        # 1. Verifica que se haya seleccionado una ruta
        # 2. Carga la imagen usando create_img()
        # 3. Ajusta los límites de los controles según el tamaño de la imagen

        """Carga la imagen seleccionada"""
        if not self.viewer.ruta_imagen:
            QMessageBox.warning(
                self.viewer, 
                "Advertencia", 
                "Primero selecciona una imagen usando el botón EXPLORAR"
            )
            return
        
        try:
            self.viewer.img_original = create_img(self.viewer.ruta_imagen)
            self.viewer.img_actual = np.copy(self.viewer.img_original)
            
            # Ajustar los límites de los SpinBox de zoom según el tamaño de la imagen
            altura, ancho = self.viewer.img_original.shape[:2]
            self.viewer.spin_zoom_x.setMaximum(altura - 1)
            self.viewer.spin_zoom_y.setMaximum(ancho - 1)
            
            # Establecer valores iniciales en el centro
            self.viewer.spin_zoom_x.setValue(altura // 2)
            self.viewer.spin_zoom_y.setValue(ancho // 2)
            
            self.mostrar_imagen(self.viewer.img_actual)
            QMessageBox.information(
                self.viewer, 
                "Éxito", 
                f"Imagen cargada correctamente\n"
                f"Dimensiones: {altura} x {ancho} píxeles"
            )
            print(f"Imagen cargada: {self.viewer.img_original.shape}")
            print(f"Límites de zoom ajustados: X(0-{altura-1}), Y(0-{ancho-1})")
            
        except Exception as e:
            QMessageBox.critical(
                self.viewer, 
                "Error", 
                f"Error al cargar la imagen:\n{str(e)}"
            )
            print(f"Error: {e}")
    
    def mostrar_imagen(self, img):
        """
        Muestra la imagen en el QLabel
        
        Parameters:
        -----------
        img : numpy.ndarray
            Imagen a mostrar
        """
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
                q_img = QImage(
                    img_display.data, 
                    width, 
                    height, 
                    bytes_per_line, 
                    QImage.Format_Grayscale8
                )
            else:
                height, width, channel = img_display.shape
                bytes_per_line = 3 * width
                q_img = QImage(
                    img_display.data, 
                    width, 
                    height, 
                    bytes_per_line, 
                    QImage.Format_RGB888
                )
            
            pixmap = QPixmap.fromImage(q_img)
            
            # Escalar la imagen para que quepa en el label manteniendo la proporción
            scaled_pixmap = pixmap.scaled(
                self.viewer.imagen_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.viewer.imagen_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Error al mostrar imagen: {e}")
            QMessageBox.critical(
                self.viewer, 
                "Error", 
                f"Error al mostrar la imagen:\n{str(e)}"
            )
    
    # ==================== TRANSFORMACIONES ====================
    
    def actualizar_imagen(self):
        """Aplica todas las transformaciones seleccionadas"""
        if self.viewer.img_original is None:
            QMessageBox.warning(self.viewer, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Iniciar con la imagen original
            img = np.copy(self.viewer.img_original)
            
            # Aplicar brillo
            img = self._aplicar_brillo(img)
            
            # Aplicar contraste
            img = self._aplicar_contraste(img)
            
            # Aplicar rotación
            img = self._aplicar_rotacion(img)
            
            # Aplicar canales RGB
            img = self._aplicar_canales_rgb(img)
            
            # Aplicar canales CMY
            img = self._aplicar_canales_cmy(img)
            
            # Aplicar filtros de zona
            img = self._aplicar_filtros_zona(img)
            
            # Aplicar negativo
            if self.viewer.check_negativo.isChecked():
                img = invert_color(img)
                print("Negativo aplicado")
            
            # Aplicar binarización
            if self.viewer.check_binarizar.isChecked():
                umbral = self.viewer.slider_binarizar.value() / 100.0
                img = binary(img, umbral)
                print(f"Binarización aplicada con umbral: {umbral}")
            
            # Aplicar fusión si hay imagen secundaria
            img = self._aplicar_fusion(img)
            
            # Asegurar que los valores están en el rango correcto
            img = np.clip(img, 0, 1)
            
            self.viewer.img_actual = img
            self.mostrar_imagen(img)
            print("Imagen actualizada correctamente")
            
        except Exception as e:
            QMessageBox.critical(
                self.viewer, 
                "Error", 
                f"Error al aplicar transformaciones:\n{str(e)}"
            )
            print(f"Error en actualizar_imagen: {e}")
            import traceback
            traceback.print_exc()
    
    def _aplicar_brillo(self, img):
        """Aplica ajuste de brillo"""
        brillo_val = self.viewer.slider_brillo.value() / 100.0
        if brillo_val != 0:
            img = brightness_adjust(img, brillo_val)
            print(f"Brillo aplicado: {brillo_val}")
        return img
    
    def _aplicar_contraste(self, img):
        """Aplica ajuste de contraste"""
        contraste_val = self.viewer.slider_contraste.value() / 100.0
        if contraste_val != 1.0:
            if contraste_val > 1.0:
                img = contrast_adjust_brightness(img, contraste_val)
            else:
                img = contrast_adjust_darkness(img, contraste_val)
            print(f"Contraste aplicado: {contraste_val}")
        return img
    
    def _aplicar_rotacion(self, img):
        """Aplica rotación a la imagen"""
        angulo = self.viewer.spin_rotacion.value()
        if angulo != 0:
            img = rotate(img, angulo)
            print(f"Rotación aplicada: {angulo}°")
        return img
    
    def _aplicar_canales_rgb(self, img):
        """Aplica filtros de canales RGB"""
        if not self.viewer.check_red.isChecked():
            img[:,:,0] = 0
            print("Canal rojo desactivado")
        if not self.viewer.check_green.isChecked():
            img[:,:,1] = 0
            print("Canal verde desactivado")
        if not self.viewer.check_blue.isChecked():
            img[:,:,2] = 0
            print("Canal azul desactivado")
        return img
    
    def _aplicar_canales_cmy(self, img):
        """Aplica filtros de canales CMY"""
        if self.viewer.check_cyan.isChecked():
            img[:,:,0] = 0  # Sin rojo = cyan
            print("Canal cyan activado")
        if self.viewer.check_magenta.isChecked():
            img[:,:,1] = 0  # Sin verde = magenta
            print("Canal magenta activado")
        if self.viewer.check_yellow.isChecked():
            img[:,:,2] = 0  # Sin azul = amarillo
            print("Canal yellow activado")
        return img
    
    def _aplicar_filtros_zona(self, img):
        """Aplica filtros de zonas claras u oscuras"""
        if self.viewer.radio_claras.isChecked():
            img_gray = gris(img)
            mascara = img_gray > 0.5
            img = img * mascara[:,:,np.newaxis]
            print("Filtro zonas claras aplicado")
        elif self.viewer.radio_oscuras.isChecked():
            img_gray = gris(img)
            mascara = img_gray <= 0.5
            img = img * mascara[:,:,np.newaxis]
            print("Filtro zonas oscuras aplicado")
        return img
    
    def _aplicar_fusion(self, img):
        """Aplica fusión con imagen secundaria si existe"""
        if self.viewer.img_fusion is not None:
            factor = self.viewer.slider_transparencia.value() / 100.0
            
            try:
                # Asegurar que ambas imágenes tengan las mismas dimensiones
                if img.shape != self.viewer.img_fusion.shape:
                    print(f"Dimensiones no coinciden: Base {img.shape}, Fusión {self.viewer.img_fusion.shape}")
                    img_fusion_adjusted = self._redimensionar_para_fusion(self.viewer.img_fusion)
                else:
                    img_fusion_adjusted = self.viewer.img_fusion
                
                # Verificar que las dimensiones coincidan después del ajuste
                if img.shape != img_fusion_adjusted.shape:
                    raise ValueError(f"No se pudieron igualar dimensiones: Base {img.shape}, Fusión {img_fusion_adjusted.shape}")
                
                # Usar la función de Transformaciones.py que acepta 3 parámetros
                from Transformaciones import fusion_images
                img = fusion_images(img, img_fusion_adjusted, factor)
                print(f"Fusión aplicada con transparencia: {factor}")
                
            except Exception as e:
                print(f"Error al aplicar fusión: {e}")
                QMessageBox.warning(
                    self.viewer,
                    "Advertencia",
                    f"No se pudo aplicar la fusión:\n{str(e)}\n\n"
                    "Las imágenes pueden tener formatos incompatibles."
                )
        return img
    
    def _redimensionar_para_fusion(self, img_fusion):
        """
        Redimensiona la imagen de fusión para que coincida con las dimensiones de la imagen base
        manteniendo la relación de aspecto y centrando la imagen
        """
        if self.viewer.img_original is None:
            return img_fusion
        
        altura_base, ancho_base = self.viewer.img_original.shape[:2]
        altura_fusion, ancho_fusion = img_fusion.shape[:2]
        
        print(f"Redimensionando: {ancho_fusion}x{altura_fusion} -> {ancho_base}x{altura_base}")
        
        # Si ya tienen las mismas dimensiones, no hacer nada
        if (altura_fusion == altura_base and ancho_fusion == ancho_base):
            return img_fusion
        
        # Convertir a formato de 8 bits para PIL
        img_fusion_8bit = (np.clip(img_fusion, 0, 1) * 255).astype(np.uint8)
        
        # Crear imagen PIL
        if len(img_fusion_8bit.shape) == 2:
            img_pil = Image.fromarray(img_fusion_8bit, mode='L')
        else:
            img_pil = Image.fromarray(img_fusion_8bit)
        
        # Redimensionar manteniendo la relación de aspecto
        img_pil_resized = img_pil.resize((ancho_base, altura_base), Image.LANCZOS)
        
        # Convertir de vuelta a numpy y normalizar
        img_redimensionada = np.array(img_pil_resized).astype(np.float32) / 255.0
        
        # Ajustar número de canales si es necesario
        img_redimensionada = self._ajustar_canales_fusion(img_redimensionada)
        
        print(f"Imagen redimensionada: {img_redimensionada.shape}")
        return img_redimensionada
    
    def _ajustar_canales_fusion(self, img_fusion):
        """Ajusta el número de canales de la imagen de fusión para que coincida con la base"""
        if self.viewer.img_original is None:
            return img_fusion
        
        # Si la imagen base es color (3 canales) y la fusión es escala de grises (2 canales)
        if len(self.viewer.img_original.shape) == 3 and len(img_fusion.shape) == 2:
            # Convertir escala de grises a RGB
            img_fusion = np.stack([img_fusion] * 3, axis=-1)
            print("Imagen de fusión convertida de escala de grises a RGB")
        
        # Si la imagen base es escala de grises (2 canales) y la fusión es color (3 canales)
        elif len(self.viewer.img_original.shape) == 2 and len(img_fusion.shape) == 3:
            # Convertir RGB a escala de grises
            img_fusion = np.mean(img_fusion, axis=2)
            print("Imagen de fusión convertida de RGB a escala de grises")
        
        return img_fusion
    
    # ==================== FUSIÓN DE IMÁGENES ====================
    
    def fusionar_imagenes(self):
        """Permite seleccionar una segunda imagen para fusionar"""
        if self.viewer.img_original is None:
            QMessageBox.warning(
                self.viewer,
                "Advertencia",
                "Primero debes cargar una imagen base.\n\n"
                "Pasos:\n"
                "1. Presiona EXPLORAR y selecciona una imagen\n"
                "2. Presiona CARGAR\n"
                "3. Luego presiona FUSIONAR IMÁGENES"
            )
            return
            
        archivo, _ = QFileDialog.getOpenFileName(
            self.viewer,
            "Seleccionar Imagen para Fusionar",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp *.gif *.tiff);;Todos los archivos (*.*)"
        )
        if archivo:
            try:
                # Cargar la imagen de fusión
                img_temp = create_img(archivo)
                
                print(f"Imagen de fusión original: {img_temp.shape}")
                print(f"Imagen base: {self.viewer.img_original.shape}")
                
                # Redimensionar automáticamente para que coincida con la imagen base
                img_temp = self._redimensionar_para_fusion(img_temp)
                
                self.viewer.img_fusion = img_temp
                
                QMessageBox.information(
                    self.viewer, 
                    "Éxito", 
                    f"Imagen para fusión cargada correctamente.\n\n"
                    f"Dimensiones originales: {img_temp.shape[1]} x {img_temp.shape[0]}\n"
                    f"Redimensionada a: {self.viewer.img_original.shape[1]} x {self.viewer.img_original.shape[0]}\n\n"
                    "Ahora:\n"
                    "1. Ajusta el control de Transparencia (0-100%)\n"
                    "2. Presiona ACTUALIZAR para ver la fusión\n\n"
                    "💡 Tip: 50% muestra ambas imágenes por igual"
                )
                print(f"Imagen de fusión cargada exitosamente: {self.viewer.img_fusion.shape}")
                
            except Exception as e:
                QMessageBox.critical(
                    self.viewer, 
                    "Error", 
                    f"Error al cargar imagen de fusión:\n\n{str(e)}\n\n"
                    f"Asegúrate de seleccionar un archivo de imagen válido\n"
                    f"(.jpg, .png, .bmp, etc.)"
                )
                print(f"Error al cargar imagen de fusión: {e}")
                import traceback
                traceback.print_exc()
    
    # ==================== ZOOM ====================
    
    def aplicar_zoom(self):
        """Aplica zoom a la imagen desde un punto central con factor seleccionable"""
        if self.viewer.img_actual is None:
            QMessageBox.warning(self.viewer, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Obtener coordenadas del punto central del zoom
            center_x = self.viewer.spin_zoom_x.value()
            center_y = self.viewer.spin_zoom_y.value()
            
            # Validar coordenadas
            if not self._validar_coordenadas_zoom(center_x, center_y):
                return
            
            # Obtener el factor de zoom
            factor = self._obtener_factor_zoom()
            
            # Aplicar zoom
            img_zoomed = zoom(self.viewer.img_actual, factor, center_x, center_y)
            
            self.viewer.img_actual = img_zoomed
            self.mostrar_imagen(img_zoomed)
            
            zoom_text = self.viewer.combo_zoom_factor.currentText()
            zoom_level = zoom_text.split(" ")[0]
            print(f"Zoom {zoom_level} aplicado desde punto ({center_x}, {center_y})")
            print(f"Dimensión de la imagen: {img_zoomed.shape}")
            
        except Exception as e:
            QMessageBox.critical(
                self.viewer, 
                "Error", 
                f"Error al aplicar zoom:\n{str(e)}"
            )
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _validar_coordenadas_zoom(self, center_x, center_y):
        """Valida que las coordenadas de zoom estén dentro de los límites"""
        altura, ancho = self.viewer.img_actual.shape[:2]
        
        if center_x >= altura or center_y >= ancho:
            QMessageBox.warning(
                self.viewer, 
                "Advertencia", 
                f"Las coordenadas están fuera de los límites de la imagen.\n"
                f"Tamaño de la imagen: {altura} x {ancho}\n"
                f"Coordenadas ingresadas: ({center_x}, {center_y})"
            )
            return False
        return True
    
    def _obtener_factor_zoom(self):
        """Obtiene el factor de zoom desde el ComboBox"""
        zoom_text = self.viewer.combo_zoom_factor.currentText()
        # Extraer el factor del texto "2x (factor 0.5)"
        return float(zoom_text.split("factor ")[1].rstrip(")"))
    
    def mostrar_ayuda_zoom(self):
        """Muestra información sobre cómo usar el zoom"""
        QMessageBox.information(
            self.viewer,
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
    
    # ==================== GUARDAR Y RESTABLECER ====================
    
    def guardar_imagen(self):
        """Guarda la imagen actual"""
        if self.viewer.img_actual is None:
            QMessageBox.warning(self.viewer, "Advertencia", "No hay imagen para guardar")
            return
        
        archivo, _ = QFileDialog.getSaveFileName(
            self.viewer,
            "Guardar Imagen",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )
        if archivo:
            try:
                # Convertir a 8 bits
                img_save = (np.clip(self.viewer.img_actual, 0, 1) * 255).astype(np.uint8)
                
                # Guardar usando PIL
                if len(img_save.shape) == 2:
                    img_pil = Image.fromarray(img_save, mode='L')
                else:
                    img_pil = Image.fromarray(img_save)
                
                img_pil.save(archivo)
                QMessageBox.information(
                    self.viewer, 
                    "Éxito", 
                    f"Imagen guardada correctamente en:\n{archivo}"
                )
                print(f"Imagen guardada: {archivo}")
            except Exception as e:
                QMessageBox.critical(
                    self.viewer, 
                    "Error", 
                    f"Error al guardar la imagen:\n{str(e)}"
                )
                print(f"Error: {e}")
    
    def restablecer_imagen(self):
        """Restablece la imagen a su estado original"""
        if self.viewer.img_original is None:
            QMessageBox.warning(self.viewer, "Advertencia", "No hay imagen cargada")
            return
        
        self.viewer.img_actual = np.copy(self.viewer.img_original)
        self.viewer.img_fusion = None
        
        # Restablecer todos los controles
        self._restablecer_controles()
        
        self.mostrar_imagen(self.viewer.img_actual)
        QMessageBox.information(
            self.viewer, 
            "Éxito", 
            "Imagen restablecida a su estado original"
        )
        print("Imagen restablecida")
    
    def _restablecer_controles(self):
        """Restablece todos los controles a sus valores por defecto"""
        # Sliders
        self.viewer.slider_brillo.setValue(0)
        self.viewer.slider_contraste.setValue(100)
        self.viewer.slider_rotacion.setValue(0)
        self.viewer.slider_transparencia.setValue(50)
        self.viewer.slider_binarizar.setValue(50)
        
        # Radio buttons
        self.viewer.radio_normal.setChecked(True)
        
        # Checkboxes RGB
        self.viewer.check_red.setChecked(True)
        self.viewer.check_green.setChecked(True)
        self.viewer.check_blue.setChecked(True)
        
        # Checkboxes CMY
        self.viewer.check_cyan.setChecked(False)
        self.viewer.check_magenta.setChecked(False)
        self.viewer.check_yellow.setChecked(False)
        
        # Checkboxes opciones
        self.viewer.check_negativo.setChecked(False)
        self.viewer.check_binarizar.setChecked(False)
        
        # Eliminar imagen de fusión
        self.viewer.img_fusion = None
        
        # Zoom
        if self.viewer.img_original is not None:
            altura, ancho = self.viewer.img_original.shape[:2]
            self.viewer.spin_zoom_x.setValue(altura // 2)
            self.viewer.spin_zoom_y.setValue(ancho // 2)
        self.viewer.combo_zoom_factor.setCurrentIndex(0)
    
    # ==================== HISTOGRAMA ====================
    
    def mostrar_histograma(self):
        """Muestra el histograma de la imagen actual"""
        if self.viewer.img_actual is None:
            QMessageBox.warning(self.viewer, "Advertencia", "Primero carga una imagen")
            return
        
        try:
            # Usar la función de la librería
            RGB_Histogram(self.viewer.img_actual)
            print("Histograma mostrado")
        except Exception as e:
            QMessageBox.critical(
                self.viewer, 
                "Error", 
                f"Error al mostrar histograma:\n{str(e)}"
            )
            print(f"Error: {e}")