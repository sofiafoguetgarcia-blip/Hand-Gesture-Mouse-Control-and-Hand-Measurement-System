# Sistema de control del ordenador mediante gestos de la mano y medición en centímetros

## Descripción general

Este proyecto implementa un sistema de visión por computador en tiempo real que permite controlar el cursor del sistema operativo mediante gestos de la mano capturados a través de una webcam.

Adicionalmente, el sistema incorpora un mecanismo de calibración geométrica que permite estimar medidas físicas de la mano en centímetros utilizando un marcador ArUco como referencia.

El sistema integra detección de landmarks de la mano, reconocimiento de gestos y calibración espacial para proporcionar una interfaz natural de interacción humano-computador.

---

## Funcionalidades

* Detección y seguimiento de la mano en tiempo real
* Control del cursor mediante gestos
* Click del ratón mediante reconocimiento de gestos
* Control de scroll mediante gestos de múltiples dedos
* Medición de dimensiones de la mano en centímetros:

  * Ancho de la palma
  * Largo de la palma
  * Longitud de los dedos (pulgar, índice, medio, anular, meñique)
* Calibración mediante marcador ArUco
* Descarga automática del modelo en la primera ejecución

---

## Tecnologías utilizadas

* Python 3.12
* OpenCV
* OpenCV (módulo ArUco)
* MediaPipe Tasks API (Hand Landmarker)
* PyAutoGUI
* NumPy

---

## Arquitectura del sistema

El funcionamiento del sistema sigue el siguiente flujo:

1. Captura de vídeo desde la webcam mediante OpenCV
2. Detección de la mano usando MediaPipe
3. Extracción de los 21 puntos clave (landmarks)
4. Reconocimiento de gestos mediante relaciones geométricas
5. Control del cursor mediante PyAutoGUI
6. Detección del marcador ArUco
7. Cálculo de escala real (cm/píxel)
8. Conversión de medidas de píxeles a centímetros
9. Visualización en tiempo real

---

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto_gestos_mano.git
cd proyecto_gestos_mano
```

### Crear entorno virtual (recomendado con uv)

```bash
uv venv
uv pip install -r requirements.txt
```

---

## Ejecución

```bash
uv run generate_aruco_marker.py
uv run main.py
```

---

## Procedimiento de calibración

Para obtener medidas precisas en centímetros:

1. Generar el marcador ArUco:

```bash
uv run generate_aruco_marker.py
```

2. Imprimir el marcador asegurando que su lado mide exactamente **5 cm**
3. Colocar la mano y el marcador en el mismo plano
4. Asegurarse de que ambos son completamente visibles en la cámara
5. Evitar inclinaciones o distorsiones de perspectiva

---

## Control mediante gestos

| Acción          | Descripción del gesto     |
| --------------- | ------------------------- |
| Activar sistema | Tecla `E`                 |
| Salir           | Tecla `Q`                 |
| Mover cursor    | Dedo índice extendido     |
| Click izquierdo | Pinza pulgar + índice     |
| Scroll          | Índice + medio extendidos |

---

## Estructura del proyecto

```
proyecto_gestos_mano/
├── main.py
├── generate_aruco_marker.py
├── requirements.txt
└── README.md
```

---

## Metodología de medición

Las medidas de la mano se calculan mediante distancias euclidianas entre puntos clave:

* Ancho de palma: distancia entre MCP del índice y del meñique
* Largo de palma: distancia entre la muñeca y el MCP del dedo medio
* Longitud de dedos: distancia entre la base (MCP) y la punta

Estas distancias se obtienen inicialmente en píxeles y posteriormente se convierten a centímetros utilizando un factor de escala derivado del marcador ArUco.

---

## Limitaciones

* La precisión depende de una correcta calibración
* Sensible a condiciones de iluminación
* Depende de la calidad de la webcam
* Requiere visibilidad del marcador para medidas reales
* Solo admite una mano

---

## Resolución de problemas

### La webcam no funciona

Modificar en `main.py`:

```python
CAMERA_INDEX = 1
```

---

### Medidas incorrectas

Posibles causas:

* Marcador mal impreso
* Marcador inclinado
* Mano y marcador en diferentes planos
* Iluminación insuficiente

---

### Movimiento inestable del cursor

Ajustar el suavizado en la función:

```python
smooth_point()
```

---

## Posibles mejoras

* Click derecho y arrastre
* Detección de múltiples manos
* Clasificación de gestos mediante aprendizaje automático
* Exportación de datos
* Interfaz gráfica
* Integración con otros dispositivos

---

## Licencia

Proyecto desarrollado con fines educativos y de investigación.

---

## Autor

Sofía
