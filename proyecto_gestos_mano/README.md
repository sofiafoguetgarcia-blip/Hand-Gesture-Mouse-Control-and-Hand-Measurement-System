# Control del ordenador con gestos + medicion de mano

Proyecto en Python que usa la webcam para controlar el raton con gestos y medir la mano en centimetros usando un marcador ArUco.

## Funciones

- mover el cursor con el dedo indice
- click izquierdo con pinza pulgar-indice
- scroll con indice + medio
- medir en cm:
  - ancho de palma
  - largo de palma
  - pulgar
  - indice
  - medio
  - anular
  - menique
- descarga automatica del modelo `hand_landmarker.task` en el primer arranque

## Instalacion con uv

```bash
uv init .
uv venv
uv pip install -r requirements.txt
```

## Ejecutar

```bash
uv run main.py
```

## Crear el marcador ArUco

```bash
uv run generate_aruco_marker.py
```

Esto crea `aruco_5cm_id0.png`. Debes imprimirlo con un lado real de 5 cm.

## Controles

- `E` activa o pausa el control del raton
- `Q` sale del programa
- indice arriba: mueve el cursor
- pinza pulgar-indice: click izquierdo
- indice y medio arriba: scroll

## Consejos

- coloca la mano y el marcador en el mismo plano
- usa buena iluminacion
- si la webcam no abre, cambia `CAMERA_INDEX = 0` por `1`
- si el cursor se mueve demasiado, ajusta la funcion `smooth_point()`
