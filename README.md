# Hand Gesture Mouse Control and Hand Measurement System

## Overview

This project implements a real-time computer vision system that enables mouse control through hand gestures using a standard webcam. In addition, it incorporates a geometric calibration method to estimate physical measurements of the hand in centimeters.

The system combines hand landmark detection, gesture recognition, and spatial calibration to provide an interactive and measurable interface between the user and the computer.

---

## Features

* Real-time hand detection and tracking
* Cursor control using hand gestures
* Mouse click through gesture recognition
* Scroll control using multi-finger gestures
* Measurement of hand dimensions in centimeters:

  * Palm width
  * Palm length
  * Finger lengths (thumb, index, middle, ring, little)
* Calibration using ArUco marker for real-world scale estimation
* Automatic model download on first execution

---

## Technologies Used

* Python 3.12
* OpenCV (cv2)
* OpenCV ArUco module
* MediaPipe Tasks API (Hand Landmarker)
* PyAutoGUI
* NumPy

---

## System Architecture

The system operates through the following pipeline:

1. Video capture from webcam using OpenCV
2. Hand landmark detection using MediaPipe Hand Landmarker
3. Extraction of key points (21 landmarks)
4. Gesture recognition based on landmark geometry
5. Cursor control via PyAutoGUI
6. ArUco marker detection for scale calibration
7. Conversion from pixel measurements to centimeters
8. Visualization of results in real time

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/hand-gesture-mouse-control.git
cd hand-gesture-mouse-control
```

### Create virtual environment (recommended with uv)

```bash
uv venv
uv pip install -r requirements.txt
```

---

## Execution

```bash
uv run generate_aruco_marker.py
uv run main.py
```

---

## Calibration Procedure

To obtain accurate measurements in centimeters:

1. Generate the ArUco marker:

```bash
uv run generate_aruco_marker.py
```

2. Print the generated marker ensuring its side length is exactly 5 cm
3. Place the marker and the hand on the same plane
4. Ensure both are fully visible in the camera frame
5. Avoid perspective distortion for better accuracy

---

## Gesture Controls

| Action           | Gesture Description                        |
| ---------------- | ------------------------------------------ |
| Activate system  | Press key `E`                              |
| Exit application | Press key `Q`                              |
| Move cursor      | Index finger extended                      |
| Left click       | Thumb and index finger pinch               |
| Scroll           | Index and middle fingers extended together |

---

## Project Structure

```
project/
├── main.py
├── generate_aruco_marker.py
├── requirements.txt
└── README.md
```

---

## Measurement Methodology

Hand measurements are computed using Euclidean distances between selected landmarks:

* Palm width: distance between index MCP and pinky MCP
* Palm length: distance between wrist and middle MCP
* Finger lengths: distance from MCP to fingertip

These distances are initially measured in pixels and then converted to centimeters using a scale factor obtained from the detected ArUco marker.

---

## Limitations

* Accuracy depends on correct calibration
* Sensitive to lighting conditions
* Performance may vary depending on webcam quality
* Requires the marker to be visible for real-world measurements
* Only supports single-hand detection

---

## Troubleshooting

### Webcam not detected

Modify the camera index in `main.py`:

```python
CAMERA_INDEX = 1
```

---

### Inaccurate measurements

Possible causes:

* Incorrect marker size
* Marker not in the same plane as the hand
* Poor lighting conditions
* Partial occlusion of marker or hand

---

### Cursor instability

Adjust smoothing factor in the function:

```python
smooth_point()
```

---

## Future Improvements

* Right-click and drag support
* Multi-hand detection
* Gesture classification using machine learning
* Data logging and export
* Graphical user interface
* Depth estimation using stereo vision

---

## License

This project is intended for educational and research purposes.

---

## Author

Sofía
