# Graficador Interactivo 2D - Proyecto 2025

Valeria Muñoz Y Juan José Arango

## 📋 Descripción del Proyecto

Aplicación gráfica interactiva desarrollada en Python que implementa algoritmos clásicos de rasterización para la generación de figuras geométricas en 2D. El proyecto enfatiza la implementación **manual** de algoritmos gráficos fundamentales sin utilizar funciones predefinidas de Pygame.

### Características Principales

- **8 herramientas de dibujo** con algoritmos implementados manualmente
- **Sistema de colores automático** diferenciado por tipo de figura
- **Vista previa en tiempo real** (rubber band)
- **Persistencia de dibujos** en canvas independiente
- **Cuadrícula y ejes** cartesianos opcionales
- **Deshacer y limpiar** canvas
- **Interfaz intuitiva** con panel de herramientas lateral

---

### Objetivo General
Diseñar e implementar una aplicación gráfica interactiva que permite visualizar y manipular algoritmos clásicos de generación de figuras geométricas en 2D.

---

## 🛠️ Requisitos del Sistema

### Software Necesario
- **Python 3.8+** (recomendado 3.10 o superior)
- **Pygame 2.0+**

### Instalación de Dependencias

```bash
# Instalar Pygame
pip install pygame

# O usando requirements.txt
pip install -r requirements.txt
```

**Archivo `requirements.txt`:**
```
pygame>=2.0.0
```
---

## 📚 Algoritmos Implementados

### 1. Línea DDA (Digital Differential Analyzer)
**Descripción:** Algoritmo incremental que usa operaciones de punto flotante para calcular píxeles intermedios.

**Características:**
- Usa aritmética de punto flotante
- Calcula incrementos uniformes
- Redondea coordenadas al píxel más cercano

---

### 2. Línea Bresenham
**Descripción:** Algoritmo optimizado que usa solo aritmética de enteros para dibujar líneas.

**Ventajas sobre DDA:**
- Más rápido (solo operaciones enteras)
- No requiere redondeo
- Más preciso

---

### 3. Circunferencia de Bresenham
**Descripción:** Algoritmo que aprovecha la simetría de 8 octantes para dibujar circunferencias eficientemente.

**Características:**
- Calcula solo 1/8 del círculo
- Usa simetría para generar los 8 octantes
- Solo aritmética entera

---

### 4. Elipse de Bresenham
**Descripción:** Adaptación del algoritmo de Bresenham para elipses, dividido en dos regiones.

**Características:**
- Región 1: pendiente < 1
- Región 2: pendiente ≥ 1
- Simetría en 4 cuadrantes

---

### 5. Curva de Bézier Cúbica
**Descripción:** Curva paramétrica definida por 4 puntos de control usando la fórmula de Bernstein.

**Fórmula:**
```
B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
donde t ∈ [0, 1]
```

**Características:**
- 4 puntos de control
- Interpolación suave
- Control de curvatura
---

### 6. Polígonos
**Descripción:** Figuras cerradas de n lados formadas conectando vértices consecutivos.

**Implementación:**
- Conecta vértices usando líneas de Bresenham
- Cierra automáticamente (último vértice conecta con el primero)
---


## 🎮 Guía de Uso Rápida

### Herramientas de 2 Puntos
**Línea DDA, Línea Bresenham, Círculo, Elipse, Rectángulo, Triángulo**

1. Selecciona la herramienta en el panel izquierdo
2. Haz **clic y arrastra** en el canvas
3. Suelta para finalizar la figura

### Polígono (N lados)
1. Selecciona **"Polígono"**
2. Haz **clic** en cada vértice
3. Presiona **ENTER** o **ESPACIO** para finalizar
4. Presiona **ESC** para cancelar

### Curva de Bézier
1. Selecciona **"Bezier"**
2. Haz **clic** en 4 puntos de control
3. La curva se dibuja automáticamente al colocar el 4to punto

### Controles Generales
- **Deshacer:** Elimina la última figura dibujada
- **Limpiar:** Borra todas las figuras del canvas
- **Toggle Cuadrícula:** Muestra/oculta la cuadrícula
- **Toggle Ejes:** Muestra/oculta los ejes cartesianos

---

## 📊 Cumplimiento de Requisitos

| Requisito | Estado | Nota |
|-----------|--------|------|
| Algoritmos DDA y Bresenham | ✅ | Implementados manualmente |
| Circunferencia de Bresenham | ✅ | Con simetría de 8 octantes |
| Curvas de Bézier cúbicas | ✅ | 4 puntos de control |
| Elipses | ✅ | Algoritmo en 2 regiones |
| Polígonos y formas cerradas | ✅ | Triángulos, rectángulos, polígonos |
| Interfaz funcional | ✅ | Panel lateral + canvas |
| Visualización inmediata | ✅ | Con preview en tiempo real |
| Colores configurables | ✅ | Automáticos por tipo |
| Modularización | ✅ | Separación algoritmos/GUI |
| Limpiar/Deshacer | ✅ | Implementado |
| Grid y ejes | ✅ | Toggleables |

---


**Última actualización:** Octubre 2025  
**Versión:** 1.0.0