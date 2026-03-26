import cv2
import numpy as np
from ultralytics import YOLO

# =========================
# CONFIG
# =========================
MODEL_PATH = r"C:\Disk D\Project\Python_Check_Oil\model_machine_new\yolo11_seg_singleclass7\weights\best.pt"
IMAGE_PATH = r"C:\Disk D\Project\Python_Check_Oil\data\img_and_label_crop_master_detect_new_machine\test_thu\images\train\img_260127_204727_042.jpg"
IMGSZ = 1024
CONF_THRES = 0.6
SCALE_SHOW = 1

POLY_COLOR = (0, 255, 0)
BOX_COLOR = (0, 255, 0)
TEXT_BG_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 0, 0)
INDEX_COLOR = (0, 0, 255)

# =========================
# DRAW POLYGON
# =========================
def draw_polylines_on_image(image, polygons_list, smooth=True):
    """
    Vẽ polygon trực tiếp lên ảnh gốc
    polygons_list: list [[x1,y1],[x2,y2],...]
    """
    for idx, polygon in enumerate(polygons_list, start=1):
        if polygon is None or len(polygon) < 3:
            continue

        pts = np.array(polygon, dtype=np.int32).reshape((-1, 1, 2))

        if smooth:
            epsilon = 0.003 * cv2.arcLength(pts, True)
            pts = cv2.approxPolyDP(pts, epsilon, True)

        cv2.polylines(image, [pts], True, POLY_COLOR, 2, cv2.LINE_AA)

        # Vẽ index tại centroid
        centroid = np.mean(pts.reshape(-1, 2), axis=0).astype(int)
        cx, cy = centroid
        cx = np.clip(cx, 0, image.shape[1] - 1)
        cy = np.clip(cy, 0, image.shape[0] - 1)

        cv2.putText(
            image, str(idx),
            (cx + 10, cy + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1, INDEX_COLOR, 2, cv2.LINE_AA
        )

    return image

# =========================
# MAIN
# =========================
def main():
    # Load model YOLOv11
    model = YOLO(MODEL_PATH)

    # Read image
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print("❌ Không đọc được ảnh")
        return

    img_draw = img.copy()

    # Predict
    results = model.predict(
        source=IMAGE_PATH,
        imgsz=IMGSZ,
        conf=CONF_THRES,
        show=False,
        verbose=False
    )

    polygons = []

    for r in results:
        if r.masks is not None:
            # === LẤY POLYGON TRỰC TIẾP TỪ YOLOv11 ===
            for poly in r.masks.xy:
                if poly is not None and len(poly) >= 3:
                    polygons.append(poly.astype(int))

        # === VẼ CONFIDENCE (OPTIONAL) ===
        if r.boxes is not None:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                label = f"{conf:.2f}"
                (w, h), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                )

                cv2.rectangle(
                    img_draw,
                    (x1, y1 - h - 6),
                    (x1 + w + 6, y1),
                    TEXT_BG_COLOR,
                    -1
                )

                cv2.putText(
                    img_draw,
                    label,
                    (x1 + 3, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    TEXT_COLOR,
                    2,
                    cv2.LINE_AA
                )

    # === VẼ POLYGON ===
    img_draw = draw_polylines_on_image(
        img_draw,
        polygons_list=polygons,
        smooth=True
    )

    # Resize hiển thị
    display_img = cv2.resize(
        img_draw,
        (img_draw.shape[1] // SCALE_SHOW, img_draw.shape[0] // SCALE_SHOW)
    )

    # Save & show
    cv2.imwrite("ketqua_polygon.png", img_draw)
    cv2.imshow("YOLOv11 - Polygon Result", display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
