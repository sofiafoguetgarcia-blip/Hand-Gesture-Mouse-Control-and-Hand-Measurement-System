from pathlib import Path
import cv2

OUTPUT = Path("aruco_5cm_id0.png")
DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker = cv2.aruco.generateImageMarker(DICT, 0, 1000)
cv2.imwrite(str(OUTPUT), marker)
print(f"Marcador guardado en: {OUTPUT.resolve()}")
print("Imprimelo con 5 cm exactos de lado.")
