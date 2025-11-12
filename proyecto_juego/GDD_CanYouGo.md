# 🎮 Documento de Diseño del Videojuego
## Can You Go?

---

## 🕹️ 1. Título del Juego

**Can You Go?**

---

## 📝 2. Resumen del Juego y Objetivos del Jugador

**Can You Go?** es un videojuego de **plataformas 2D** con una narrativa nostálgica y emotiva que explora las historias del pasado a través de los ojos del presente. El juego presenta un estilo visual tipo **pixel art retro**, con colores cálidos y una estética que evoca nostalgia.

El juego comienza con el **abuelo** contando a su **nieto** las increíbles y peligrosas aventuras que vivía cada día solo para llegar a la escuela cuando era joven. A través de esta narrativa, el jugador asume el rol del abuelo en su juventud, enfrentando los diversos obstáculos, enemigos y desafíos que se interponían en su camino diario hacia su escuela.

La progresión del juego se desarrolla mediante **niveles secuenciales**, donde cada nivel representa una etapa diferente del trayecto a la escuela, con dificultad incremental y ambientaciones variadas.

### Objetivos del Jugador:
- **Superar obstáculos progresivos**: El jugador debe atravesar plataformas, saltar abismos, evitar trampas que representan los desafíos exagerados del relato del abuelo.
- **Recolectar libros**: Un libro por nivel, representando los conocimientos adquiridos en el camino.
- **Completar todos los niveles**: Cada nivel representa una parte del camino a la escuela, y el objetivo final es llegar al destino con los cinco libros recolectados.


## 🔁 3. Estructura de Navegación del Juego

### 3.1 Diagrama de navegación:

```
[Intro - Escena del Abuelo y Nieto]
              ↓
      [Menú Principal]
         ├── [Jugar]
         └── [Salir]
```

### 3.2 Descripción de secciones:

- **Intro**: Pantalla animada que muestra al abuelo sentado con su nieto haciendo una fogata, comenzando a contar su historia con diálogos introductorios y música nostálgica de fondo.
- **Menú Principal**: Interfaz con el título del juego y opciones claras para navegar. Fondo con ilustración del paisaje alrededor de la escuela.
- **Jugar**: Inicia la aventura del juego, cargando el primer nivel del recorrido hacia la escuela. Los niveles avanzan de forma automática, sin opción de selección.
- **Salir**: Cierra el juego con confirmación previa.

---

## 📖 4. Historia o Narrativa

### Universo del juego:
El juego se desarrolla en un **entorno rural/suburbano** de mediados del siglo XX, con caminos de tierra, pequeños pueblos y bosques.

### Ambientación:
Cada nivel representa una sección diferente del camino en diferentes horarios del día: el pueblo al amanecer, el bosque denso, el cruce del río, la montaña rocosa y finalmente, la llegada a la escuela.

### Personajes principales:
- **El Abuelo (joven)**: Protagonista jugable. Un niño/adolescente decidido y valiente que debe llegar a la escuela pese a todos los obstáculos
- **El Abuelo (anciano)**: Narrador de la historia.
- **El Nieto**: Personaje secundario que escucha fascinado las historias de su abuelo

### Obstáculos:
- Elementos naturales (rocas, troncos, desniveles, charcos de agua y agujeros).

### Conflicto central:
El desafío diario de **llegar a la escuela** superando innumerables obstáculos que, aunque exagerados en el relato nostálgico del abuelo.

### Desenlace:
Al completar todos los niveles, el abuelo joven finalmente llega a la escuela.
---

## ⚙️ 5. Mecánicas del Juego

### Acciones disponibles:
- **Moverse**: Izquierda y derecha para desplazarse horizontalmente
- **Saltar**: Saltar sobre obstáculos y alcanzar plataformas superiores
- **Agacharse**: Evitar proyectiles u obstáculos bajos
- **Recolectar libros**: 
- **Interactuar**: puertas o elementos del entorno

### Reglas de juego:
- El jugador cuenta con 3 vidas totales durante toda la partida.
- Al perder las 3 vidas, el juego termina y debe reiniciarse.
- El juego no incluye enemigos ni daño, pero puede haber caídas o errores de salto que hagan perder una vida.

### Reglas de victoria y derrota:
- **Victoria**: Llegar al final del último nivel con los cinco libros recolectados.
- **Derrota**: Perder las tres vidas antes de llegar al final.

---

## 🎮 6. Controles del Juego

### a) Teclado (control principal):
- **Flecha Izquierda/Derecha**: Movimiento horizontal del personaje
- **Flecha Arriba** o **Espacio**: Saltar
- **Flecha Abajo**: Agacharse
- **ESC**: Pausar el juego / Menú de pausa
- **Enter**: Confirmar en menús

---

## 🗺️ 7. Diseño de Niveles

### Cantidad de niveles: **5 Niveles secuenciales**

### Descripción de niveles:

**Nivel 1: El Pueblo al Amanecer**
- **Descripción**: Tutorial básico en el pueblo, con obstáculos simples
- **Dificultad**: Baja - introducción a las mecánicas
- **Elementos**: Plataformas básicas y monedas
- **Ambientación**: Casas de pueblo, caminos de tierra, sol naciente

**Nivel 2: El Bosque Denso**
- **Descripción**: Bosque con vegetación densa y más plataformas
- **Dificultad**: Media-baja
- **Elementos**: troncos, ramas como plataformas, arbustos con espinas
- **Ambientación**: Árboles altos, luz filtrada, sonidos de naturaleza

**Nivel 3: El Cruce del Río**
- **Descripción**: Nivel acuático con plataformas flotantes y corrientes
- **Dificultad**: Media
- **Elementos**: Troncos flotantes, peces, rocas resbaladizas
- **Ambientación**: Río caudaloso, puentes de madera

**Nivel 4: (PENDIENTE DE CREACION)**
- **Descripción**:
- **Dificultad**: 
- **Elementos**: 
- **Ambientación**: 

**Nivel 5: (FINAL)**
- **Descripción**:
- **Dificultad**: 
- **Elementos**: 
- **Ambientación**: 


### Progresión de dificultad:
Cada nivel incrementa la complejidad de los saltos y plataformas, manteniendo una experiencia tranquila y narrativa.

---

## 🎨 8. Elementos Visuales

### Estilo gráfico:
- **Pixel art retro** con paleta de colores cálidos (naranjas, marrones, verdes naturales)
- Estética nostálgica inspirada en los años 50-60
- Escala coherente de 32x32 o 64x64 píxeles para personajes

### Recursos gráficos:
- **Sprites del protagonista**: idle, caminar, saltar, agacharse,
- **Escenarios**: fondos de pueblo, bosque, río, montaña
- **Objetos coleccionables**: libros
- **Plataformas y tiles**: tierra, piedra, madera, pasto
- **UI**: marcos, botones, iconos de vida y contador de libros


### Sistema de animación:
- **Spritesheets** para ciclos de animación del personaje (walk cycle de 4-8 frames)
- Animaciones de enemigos con patrones de 2-4 frames
- Transiciones suaves entre estados usando lógica de frames en Pygame

---

## 🔊 9. Sonido y Música

### Música de fondo:
- **Menú principal**: Melodía nostálgica y relajante con instrumentos acústicos
- **Nivel 1-2**: Música alegre y aventurera
- **Nivel 3-4**: Música con tensión creciente
- **Pantalla de victoria**: Tema emotivo y satisfactorio

### Efectos de sonido:
- Salto del personaje
- Recolección de monedas/objetos
- Daño recibido
- Sonidos ambientales (pájaros, agua, viento)
- Clic en botones del menú

### Fuentes de audio:
*[Listar aquí las fuentes de música y efectos: FreeSounds.org, OpenGameArt.org, composiciones propias, etc., con licencias correspondientes]*

---

## 🧭 10. Interfaz de Usuario (UI)

### Pantallas necesarias:
- **Intro animada**: Abuelo y nieto en conversación
- **Menú principal**: Con logo del juego y botones claros
- **Pantalla de juego**: Con HUD completo
- **Pantalla de pausa**: Opciones de continuar, reiniciar, salir
- **Pantalla de victoria/derrota**: Con estadísticas y opción de reintentar

### Indicadores en pantalla (HUD):
- **Vidas**: Iconos de corazones (3 máximo) en esquina superior izquierda
- **Objetos recolectados**: Contador de libros con icono
- **Nivel actual**: Indicador de progreso (ej. "Nivel 2/5")

---

## 🧩 11. Arquitectura del Código

### Enfoque: **Programación Orientada a Objetos**

### Clases principales:
```python
# Clase principal del juego
class Juego:
    # Gestiona el loop del juego, estados y transiciones entre pantallas
    pass

# Clase del personaje jugable
class Personaje:
    # Atributos: posición, velocidad, vidas, sprites
    # Métodos: mover(), saltar(), recibir_daño(), animar()
    pass

# Clase para gestionar cada nivel
class Nivel:
    # Carga plataformas, enemigos, coleccionables desde archivo JSON
    # Métodos: cargar(), actualizar(), dibujar()
    pass

# Clase para elementos colisionables
class Plataforma:
    # Atributos: posición, tamaño, tipo (fija, móvil)
    # Métodos: actualizar(), dibujar()
    pass

# Clase para objetos recolectables
class Coleccionable:
    # Atributos: posición, tipo (moneda, libro), valor
    # Métodos: recolectar(), dibujar()
    pass

# Clase base para pantallas y menús
class Pantalla:
    # Métodos: actualizar(), dibujar(), manejar_eventos()
    pass

# Clase auxiliar para animaciones
class Animacion:
    # Gestiona spritesheets y frames
    # Métodos: actualizar_frame(), obtener_sprite_actual()
    pass
```

### Organización del proyecto:
```
└── 📁proyecto_juego
    └── 📁assets
        └── 📁images
            └── 📁backgrounds
                ├── Background_0.png
                ├── Background.png
            └── 📁decorations
                ├── escuela.png
            └── 📁menus
                ├── inicio_play.png
                ├── inicio_quit.png
                ├── inicio.ase
                ├── inicio.png
            └── 📁player
                ├── player.png
            └── 📁test_scenes
                ├── test_1.png
                ├── test_2.png
            └── 📁tiles
                ├── tiles.png
    └── 📁src
        └── 📁__pycache__
            ├── cargador_sprites.cpython-312.pyc
            ├── constantes.cpython-312.pyc
            ├── juego.cpython-312.pyc
            ├── menu.cpython-312.pyc
            ├── nivel.cpython-312.pyc
            ├── personaje.cpython-312.pyc
        ├── cargador_sprites.py
        ├── constantes.py
        ├── juego.py
        ├── main.py
        ├── menu.py
        ├── nivel.py
        ├── pantalla.py
        ├── personaje.py
        ├── plataforma.py
    └── GDD_CanYouGo.md
```


## 📅 12. Cronograma de Desarrollo

| Fase | Actividades principales | Duración | Fecha límite |
|------|------------------------|----------|--------------|
| **Diseño** | GDD completo, bocetos de niveles, diseño de personajes, prototipo en papel | 2 semanas | [Insertar fecha] |
| **Implementación Fase 1** | Programación de clases base (Juego, Personaje, Plataforma), menú principal, sistema de navegación | 2 semanas | [Insertar fecha] |
| **Implementación Fase 2** | Desarrollo de niveles 1-3, mecánicas de plataformas completas, enemigos básicos, sistema de colisiones | 2 semanas | [Insertar fecha] |
| **Implementación Fase 3** | Niveles 4-6, sistema de puntajes completo, HUD, integración de audio y música | 2 semanas | [Insertar fecha] |
| **Pruebas** | Testing de jugabilidad, balance de dificultad, corrección de bugs, optimización | 1 semana | [Insertar fecha] |
| **Entrega final** | Documentación completa, código comentado, presentación del proyecto, video demo | 1 semana | [Insertar fecha] |

### Hitos importantes:
- **Semana 2**: GDD aprobado y diseño de niveles completado
- **Semana 4**: Primer nivel jugable con mecánicas básicas funcionando
- **Semana 6**: Tres niveles completos y sistema de enemigos implementado
- **Semana 8**: Juego completo con todos los niveles y características
- **Semana 9**: Versión estable lista para pruebas
- **Semana 10**: Entrega final con documentación

---

## 👥 13. Créditos y Referencias

### Integrantes del equipo:
- **[Nombre del integrante 1]**: Programador principal y diseñador de niveles
- **[Nombre del integrante 2]**: Diseñador gráfico y animador
- **[Nombre del integrante 3]**: Diseñador de audio y tester
- **[Nombre del integrante 4]**: Documentación y diseño narrativo

### Recursos externos utilizados:

#### Sprites y gráficos:
- OpenGameArt.org - Licencia CC BY 3.0
- itch.io (Game Assets) - Licencia especificada en cada recurso
- Kenney.nl - Assets gratuitos CC0

#### Música:
- FreeMusicArchive.org - Licencia Creative Commons
- Incompetech.com - Licencia CC BY 4.0

#### Efectos de sonido:
- Freesound.org - Licencia CC0 y CC BY
- Zapsplat.com - Licencia gratuita

#### Fuentes:
- Google Fonts - Pixel fonts (Press Start 2P, VT323)
- Licencia Open Font License

### Herramientas utilizadas:
- **Python 3.x**: Lenguaje de programación principal
- **Pygame**: Librería para desarrollo de videojuegos
- **Visual Studio Code**: Editor de código
- **Tiled**: Editor de mapas para niveles
- **Aseprite/Piskel**: Editor de pixel art y animaciones
- **Audacity**: Edición de audio
- **Git/GitHub**: Control de versiones

### Documentación consultada:
- Documentación oficial de Pygame: https://www.pygame.org/docs/
- Tutorial de platformers en Pygame por DaFluffyPotato
- Artículos sobre diseño de niveles en Gamasutra
- Game Programming Patterns por Robert Nystrom
- Principios de Game Design por Jesse Schell

### Inspiración:
- Juegos clásicos de plataformas: Super Mario Bros, Celeste, Hollow Knight
- Narrativas nostálgicas: To the Moon, Finding Paradise

---

## 📊 14. Notas Adicionales

### Requisitos del sistema:
- **Sistema operativo**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 o superior
- **RAM**: 4 GB mínimo
- **Espacio en disco**: 200 MB
- **Resolución**: 1280x720 mínimo

### Características técnicas:
- **Resolución del juego**: 1280x720 píxeles (escalable)
- **Frame rate objetivo**: 60 FPS
- **Formato de guardado**: JSON para puntajes y progreso
- **Formato de niveles**: JSON con estructura definida

### Características opcionales (stretch goals):
- Sistema de logros/achievements
- Modo historia extendido con más cinemáticas
- Niveles secretos o bonus
- Modo desafío con tiempo límite
- Skin alternativas para el personaje
- Soporte para múltiples idiomas
- Modo cooperativo local (2 jugadores)

### Consideraciones de diseño:
- El juego debe ser accesible para jugadores casuales pero ofrecer desafío para jugadores experimentados
- La narrativa debe ser emotiva sin ser excesivamente melancólica
- Los niveles deben tener un balance entre exploración y acción
- El arte pixel debe ser consistente en todo el juego
- La música debe reforzar la atmósfera nostálgica sin ser repetitiva

---

## 📋 Lista de verificación para la entrega

- [ ] Código fuente completo y comentado
- [ ] Todos los assets (sprites, música, sonidos) organizados en carpetas
- [ ] Archivo README.md con instrucciones de instalación y ejecución
- [ ] Archivo requirements.txt con dependencias
- [ ] GDD completo (este documento)
- [ ] Video demo del juego (3-5 minutos)
- [ ] Presentación del proyecto (PowerPoint/PDF)
- [ ] Todos los niveles funcionales y testeados
- [ ] Sistema de puntajes funcionando correctamente
- [ ] Sin bugs críticos conocidos
- [ ] Créditos completos de todos los recursos utilizados
- [ ] Licencias apropiadas para recursos externos

---

**Este documento es un trabajo en progreso y será actualizado durante el desarrollo del juego.**

**Fecha de creación**: 06 de noviembre de 2025  
**Última actualización**: 06 de noviembre de 2025  
**Versión**: 1.0

---

© 2025 - Can You Go? - Proyecto Final de Computación Gráfica
