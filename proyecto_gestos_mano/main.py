import math
import sys
import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = Path("hand_landmarker.task")

ARUCO_DICT = cv2.aruco.DICT_4X4_50
ARUCO_ID = 0
MARKER_SIZE_CM = 5.0

CAMERA_INDEX = 0
SCREEN_W, SCREEN_H = pyautogui.size()
pyautogui.FAILSAFE = True

def ensure_model():
    if MODEL_PATH.exists():
        return
    print("Descargando modelo de MediaPipe...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"Modelo guardado en: {MODEL_PATH.resolve()}")

def dist(a, b):
    return float(math.hypot(a[0] - b[0], a[1] - b[1]))

def lm_to_xy(lm, width, height):
    return np.array([lm.x * width, lm.y * height], dtype=np.float32)

def hand_box(points):
    xs = points[:, 0]
    ys = points[:, 1]
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

def finger_is_up(landmarks, tip_idx, pip_idx):
    return landmarks[tip_idx].y < landmarks[pip_idx].y

def wrap_text(text, max_chars=52):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines

def draw_panel(frame, lines):
    panel_lines = []
    for line in lines:
        panel_lines.extend(wrap_text(line, max_chars=50))

    x, y = 12, 28
    font_scale = 0.58
    thickness = 2
    line_h = 24
    margin = 12

    max_width = 0
    for line in panel_lines:
        (w, _), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        max_width = max(max_width, w)

    box_w = max_width + margin * 2
    box_h = len(panel_lines) * line_h + margin * 2 + 8

    cv2.rectangle(frame, (6, 6), (6 + box_w, 6 + box_h), (20, 20, 20), -1)
    cv2.rectangle(frame, (6, 6), (6 + box_w, 6 + box_h), (0, 255, 0), 2)

    for i, line in enumerate(panel_lines):
        cv2.putText(
            frame,
            line,
            (x, y + i * line_h),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA,
        )

def detect_scale_cm_per_px(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    corners, ids, _ = detector.detectMarkers(gray)
    if ids is None:
        return None, None

    ids = ids.flatten()
    for marker_corners, marker_id in zip(corners, ids):
        if int(marker_id) != ARUCO_ID:
            continue
        pts = marker_corners[0].astype(np.float32)
        side_px = np.mean([
            dist(pts[0], pts[1]),
            dist(pts[1], pts[2]),
            dist(pts[2], pts[3]),
            dist(pts[3], pts[0]),
        ])
        if side_px <= 0:
            continue
        return MARKER_SIZE_CM / side_px, pts
    return None, None

def create_landmarker():
    base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.55,
        min_hand_presence_confidence=0.55,
        min_tracking_confidence=0.55,
    )
    return vision.HandLandmarker.create_from_options(options)

def detect_hand(frame_bgr, landmarker, timestamp_ms):
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    return landmarker.detect_for_video(mp_image, timestamp_ms)

def smooth_point(prev_pt, new_pt, alpha=0.25):
    if prev_pt is None:
        return new_pt
    return prev_pt * (1 - alpha) + new_pt * alpha

def main():
    ensure_model()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("No se pudo abrir la webcam.")
        sys.exit(1)

    try:
        landmarker = create_landmarker()
    except Exception as e:
        print("No se pudo iniciar MediaPipe.")
        print(e)
        sys.exit(1)

    control_active = False
    last_click_time = 0.0
    last_toggle_time = 0.0
    last_scroll_y = None
    prev_cursor_point = None
    status_text = "Pausado"

    print("Controles:")
    print("- Tecla E: activar/desactivar control del raton")
    print("- Tecla Q: salir")
    print("- Pinza pulgar-indice: click izquierdo")
    print("- Indice arriba: mover cursor")
    print("- Indice y medio arriba: scroll")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer un frame de la webcam.")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        timestamp_ms = int(time.time() * 1000)

        cm_per_px, marker_pts = detect_scale_cm_per_px(frame)
        result = detect_hand(frame, landmarker, timestamp_ms)

        lines = [
            f"Control raton: {'ACTIVO' if control_active else 'PAUSADO'} (tecla E)",
            f"Estado: {status_text}",
            "Gestos: indice = mover | pinza pulgar-indice = click | indice + medio = scroll",
        ]

        if marker_pts is not None:
            marker_pts_int = marker_pts.astype(int)
            cv2.polylines(frame, [marker_pts_int], True, (255, 255, 0), 2)
            lines.append(f"Escala: {cm_per_px:.4f} cm/px")

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            points = np.array([[int(lm.x * w), int(lm.y * h)] for lm in hand], dtype=np.int32)

            for p in points:
                cv2.circle(frame, tuple(p), 3, (0, 255, 0), -1)
            hull = cv2.convexHull(points)
            cv2.polylines(frame, [hull], True, (255, 0, 255), 2)

            wrist = lm_to_xy(hand[0], w, h)
            thumb_cmc = lm_to_xy(hand[1], w, h)
            thumb_tip = lm_to_xy(hand[4], w, h)
            index_mcp = lm_to_xy(hand[5], w, h)
            index_tip = lm_to_xy(hand[8], w, h)
            middle_mcp = lm_to_xy(hand[9], w, h)
            middle_tip = lm_to_xy(hand[12], w, h)
            ring_mcp = lm_to_xy(hand[13], w, h)
            ring_tip = lm_to_xy(hand[16], w, h)
            pinky_mcp = lm_to_xy(hand[17], w, h)
            pinky_tip = lm_to_xy(hand[20], w, h)

            palm_width_px = dist(index_mcp, pinky_mcp)
            palm_length_px = dist(wrist, middle_mcp)

            if cm_per_px is not None:
                palm_width_cm = palm_width_px * cm_per_px
                palm_length_cm = palm_length_px * cm_per_px
                thumb_cm = dist(thumb_cmc, thumb_tip) * cm_per_px
                index_cm = dist(index_mcp, index_tip) * cm_per_px
                middle_cm = dist(middle_mcp, middle_tip) * cm_per_px
                ring_cm = dist(ring_mcp, ring_tip) * cm_per_px
                pinky_cm = dist(pinky_mcp, pinky_tip) * cm_per_px

                lines.extend([
                    f"Ancho palma: {palm_width_cm:.2f} cm",
                    f"Largo palma: {palm_length_cm:.2f} cm",
                    f"Pulgar: {thumb_cm:.2f} cm | Indice: {index_cm:.2f} cm",
                    f"Medio: {middle_cm:.2f} cm | Anular: {ring_cm:.2f} cm | Menique: {pinky_cm:.2f} cm",
                ])
            else:
                lines.append("Para medir en cm, muestra el marcador ArUco ID 0 de 5 cm.")

            index_up = finger_is_up(hand, 8, 6)
            middle_up = finger_is_up(hand, 12, 10)
            ring_up = finger_is_up(hand, 16, 14)
            pinky_up = finger_is_up(hand, 20, 18)

            pinch_thumb_index = dist(lm_to_xy(hand[4], w, h), lm_to_xy(hand[8], w, h)) < max(22, palm_width_px * 0.18)

            x1, y1, x2, y2 = hand_box(points)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 160, 255), 2)

            cursor_point = lm_to_xy(hand[8], w, h)
            prev_cursor_point = smooth_point(prev_cursor_point, cursor_point, alpha=0.30)

            if control_active:
                if index_up and not middle_up and not ring_up and not pinky_up:
                    screen_x = np.interp(prev_cursor_point[0], [40, w - 40], [0, SCREEN_W - 1])
                    screen_y = np.interp(prev_cursor_point[1], [40, h - 40], [0, SCREEN_H - 1])
                    pyautogui.moveTo(int(screen_x), int(screen_y), _pause=False)
                    status_text = "Moviendo cursor"

                elif pinch_thumb_index and (time.time() - last_click_time) > 0.7:
                    pyautogui.click()
                    last_click_time = time.time()
                    status_text = "Click izquierdo"

                elif index_up and middle_up and not ring_up and not pinky_up:
                    if last_scroll_y is None:
                        last_scroll_y = prev_cursor_point[1]
                    delta = prev_cursor_point[1] - last_scroll_y
                    if abs(delta) > 12:
                        pyautogui.scroll(int(delta * 2), _pause=False)
                        last_scroll_y = prev_cursor_point[1]
                    status_text = "Scroll"
                else:
                    last_scroll_y = None
                    status_text = "Mano detectada"
            else:
                status_text = "Pausado"

        draw_panel(frame, lines)
        cv2.imshow("Control por gestos + medicion de mano", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord("e") and (time.time() - last_toggle_time) > 0.35:
            control_active = not control_active
            last_toggle_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
