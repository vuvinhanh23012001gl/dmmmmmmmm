import cv2
import os
import numpy as np
import time
from ultralytics import YOLO
import calculate
import folder
import copy
from enum import Enum 


class Mode(Enum):
    DEFAULT = 0
    CLICK_PEN =  1

mode = Mode.DEFAULT
NAME_FOLDER_MODEL = "model"
NAME_FILE_MODEL = "best.pt"
path_phan_mem = folder.edit_path(os.path.dirname(os.path.realpath(__file__)))
try:
    path_folder_model = folder.create_folder_parent(NAME_FOLDER_MODEL)
    path_file_model = folder.create_file_in_folder(path_folder_model, NAME_FILE_MODEL)
    model = YOLO(path_file_model).cuda()
    model_loaded = True
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Could not load YOLO model: {e}. Auto-segmentation will be unavailable.")
    model_loaded = False

polygons_dirty = False   # ← THAY THẾ HASH
drawing = False
polygons_data_list = [] # Biến mới để lưu trữ danh sách các dictionary

polygons_cv = []
polygons_op = []
start_x, start_y = 0, 0
center = (0, 0)
number_resize = 5
confidence = 0.7
state_file = 'current_state.txt'
label = None # Biến label này sẽ tạm thời cho việc lựa chọn nhãn khi vẽ thủ công, hoặc có thể được dùng khi bạn muốn gán nhãn cho một contour cụ thể
name_label = {"0": ["giot dau 1",[]], "1": ["giot dau 2",[]], "2": ["none",[]], "3": ["none",[]], "4": ["none",[]],
                "5": ["none",[]], "6": ["none",[]], "7": ["none",[]], "8": ["none",[]], "9": ["none",[]]}
mouse_pos = (-1, -1)
eraser_size = 20
is_adding = False
is_erasing = False
is_moving_mask = False
mask_dirty = False   # ← THÊM
selected_polygon_index = -1

# Thêm các biến để di chuyển mask một cách ổn định
original_polygon_for_move = None
initial_click_pos = None
eraser_shape = 'square'
show_help = True
    
# Thêm biến trạng thái hiển thị bounding box và danh sách bounding box YOLO

yolo_bboxes = []  # Lưu bounding box từ YOLO preddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddict


# Thêm biến cho chế độ vẽ bounding box thủ công

manual_bbox_start = None
manual_bbox_end = None
manual_bbox_list = []  # Lưu các bbox thủ công [(x1, y1, x2, y2), ...]



path_setting = path_phan_mem + "/setting/setting_segmentation.txt"
data_setting = folder.read_settings(path_setting)
folder_input = folder.edit_path(data_setting["folder_input"])
if data_setting["forder_output"] == "None":
    forder_output = 'labels_segmentation/output'
else:
    forder_output = folder.edit_path(data_setting["forder_output"])
number_resize = float(data_setting["resize"])
if not os.path.exists(forder_output):
    os.makedirs(forder_output)


def draw_polygon(event, x, y, flags, param):
    global drawing, start_x, start_y, name_label,mask_dirty
    global label, mouse_pos, is_adding, eraser_size, eraser_shape, is_erasing, img_mask, polygons_data_list,polygons_dirty
    global  manual_bbox_start, manual_bbox_end, manual_bbox_list
    global is_moving_mask, selected_polygon_index, original_polygon_for_move, initial_click_pos
    mouse_pos = [x, y]
    
    if mode == Mode.CLICK_PEN and mouse_pos != (-1, -1):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("CLICK_PEN at", x, y)

    if label is not None:
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if mouse_pos is within a contour
            found_contour = False
            for entry_idx, entry in enumerate(polygons_data_list):
                contour_poly = np.array(entry["polygon"], dtype=np.int32)
                if len(contour_poly) > 0 and cv2.pointPolygonTest(contour_poly, (x, y), False) >= 0:
                    polygons_data_list[entry_idx]["label"] = str(label)
                    polygons_dirty = True
                    found_contour = True
                    break

            if not found_contour:
                name_label[str(label)][1].append(mouse_pos)
            label_width = 90
            label_height = (h2 - 110) // 10
            offset_x = 10
            offset_y = 10

            for i in range(10):
                x1 = w2 + offset_x
                y1 = offset_y + i * (label_height + offset_y)
                x2 = w2 + label_width + offset_x
                y2 = offset_y + (i + 1) * (label_height + offset_y)

                if x > x1 and x < x2 and y > y1 and y < y2:
                    if label == i:
                        label = None
                    else:
                        label = i # Gán label bằng số thứ tự của ô vuông
    else:
        if event == cv2.EVENT_MBUTTONDOWN:
            if eraser_shape == 'square':
                eraser_shape = 'circle'
            else:
                eraser_shape = 'square'
            return

        if event == cv2.EVENT_MOUSEWHEEL:
            print(eraser_size)
            if flags > 0:  # Lăn lên để tăng kích thước
                eraser_size += 2
            else:  # Lăn xuống để giảm kích thước
                eraser_size -= 2
            eraser_size = max(1, min(100, eraser_size))  # Giới hạn kích thước trong khoảng 1-100
            return

        if event == cv2.EVENT_RBUTTONDOWN:
            drawing = True
            is_adding = False
            is_erasing = True
            start_x, start_y = x, y
        if event == cv2.EVENT_LBUTTONUP:
            is_adding = False
            drawing = False
        elif event == cv2.EVENT_RBUTTONUP:
            is_erasing = False
            drawing = False
        elif event == cv2.EVENT_LBUTTONDOWN:
            is_erasing = False
            is_adding = True

            label_width = 90
            label_height = (h2 - 110) // 10
            offset_x = 10
            offset_y = 10

            for i in range(10):
                x1 = w2 + offset_x
                y1 = offset_y + i * (label_height + offset_y)
                x2 = w2 + label_width + offset_x
                y2 = offset_y + (i + 1) * (label_height + offset_y)

                if x > x1 and x < x2 and y > y1 and y < y2:
                    if label == i:
                        label = None
                    else:
                        label = i # Gán label bằng số thứ tự của ô vuông
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                # Di chuyển các polygon hiện có trong polygons_data_list
                for pol_data_entry in polygons_data_list:
                    # Check if the mouse is within this polygon before moving it
                    contour_poly = np.array(pol_data_entry["polygon"], dtype=np.int32)
                    if len(contour_poly) > 0 and cv2.pointPolygonTest(contour_poly, (start_x, start_y), False) >= 0:
                        dx = x - start_x
                        dy = y - start_y
                        poly = []
                        for px, py in pol_data_entry["polygon"]:
                            px += dx
                            py += dy
                            poly.append([px, py])
                        pol_data_entry["polygon"] = poly
                        polygons_dirty = True
                        break # Move only the first polygon found under the mouse click
                start_x, start_y = x, y


        if is_adding and img_mask is not None: # them
            x1 = x - eraser_size // 2
            y1 = y - eraser_size // 2
            x2 = x + eraser_size // 2
            y2 = y + eraser_size // 2
            mask_dirty = True
            if eraser_shape == 'square':
                cv2.rectangle(img_mask, (x1, y1), (x2, y2), 255, -1)
            else:
                cv2.circle(img_mask, mouse_pos, eraser_size // 2, 255, -1)

        elif is_erasing and img_mask is not None: # xoa
            print("xóa")
            mask_dirty = True
            x1 = x - eraser_size // 2
            y1 = y - eraser_size // 2
            x2 = x + eraser_size // 2
            y2 = y + eraser_size // 2
            if eraser_shape == 'square':
                cv2.rectangle(img_mask, (x1, y1), (x2, y2), 0, -1)
            else:
                cv2.circle(img_mask, mouse_pos, eraser_size // 2, 0, -1)


list_name_img = os.listdir(folder_input)
if len(list_name_img) == 0:
    print("khong co anh")
stt = 0
name_img_old = ""

last_checked_image = folder.load_current_state(state_file)
if last_checked_image and last_checked_image in list_name_img:
    stt = list_name_img.index(last_checked_image)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_polygon)
cv2.resizeWindow('image', 1920 + 100, 1200 +100)
img_mask = None
img = None
img_new = None
img_resize = None

# Variable to hold a message to be displayed on the image
display_message = ""
message_start_time = 0
MESSAGE_DURATION_MS = 2000 # 2 seconds

# Lấy kích thước màn hình một lần khi bắt đầu
screen_width, screen_height = calculate.get_screen_dimensions()

while True:
    name_img = list_name_img[stt]
    # if name_img_old != name_img or ((stt == 0 or stt == len(list_name_img) - 1) and len(list_name_img) != 0):

    # Mỗi lần sang ảnh → load lại ảnh + mask + polygon đúng của ảnh đó.
    if name_img_old != name_img and len(list_name_img) != 0:
        # Xóa các điểm mẫu của ảnh trước để không ảnh hưởng đến ảnh hiện tại
        for key in name_label:
            name_label[key][1] = []

        output_file = os.path.join(forder_output, name_img.split(".")[0] + ".txt")
        img = cv2.imread(os.path.join(folder_input, name_img))
        if img is None:
            print(f"Could not load image {os.path.join(folder_input, name_img)}. Skipping.")
            stt = (stt + 1) % len(list_name_img) # Move to next image
            continue

        h, w, _ = img.shape
        img_resize = cv2.resize(img.copy(), (int(w * number_resize), int(h * number_resize)))
        # polygons_data_list
        h2, w2, _ = img_resize.shape
        img_mask = np.zeros((h2,w2),dtype=np.uint8)
        print("img_mask 2")
        img_new = np.ones((h2,w2+100,3), dtype=np.uint8) * 255
        img_new[:h2 ,:w2 ,:] = img_resize.copy()
        polygons_data_list = folder.load_polygons_from_txt(output_file, w2, h2)
        polygons_dirty = False
        # Nếu có dữ liệu cũ, vẽ lại mask từ đó
        if polygons_data_list:
            for entry in polygons_data_list:
                poly = np.array(entry["polygon"], dtype=np.int32)
                if len(poly) > 0: # Ensure polygon is not empty
                    cv2.fillPoly(img_mask, [poly], 255) # Vẽ lại các polygon lên mask
        name_img_old = name_img

    # 👉 Đoạn này dùng để tạo ảnh hiển thị mỗi frame: reset canvas, gắn ảnh resize, vẽ bbox (nếu có) và tạo ảnh giả để tránh crash khi chưa có dữ liệu.
    if img_new is not None and img_mask is not None:
        img_new = np.ones((h2,w2+100,3), dtype=np.uint8) * 255
        img_new[:h2 ,:w2 ,:] = img_resize.copy()
    else:
        img_mask = np.zeros((500,500),dtype=np.uint8)
        print("zeros")
        img_resize = np.zeros((500,500,3),dtype=np.uint8)
        img_new = np.zeros((500,500+100,3),dtype=np.uint8) # Ensure it has enough width

    # Chỉ cập nhật danh sách polygon từ mask nếu không ở trong chế độ di chuyển.

    # Đoạn này cập nhật lại danh sách polygon từ mask khi mask thay đổi (không đang move), giữ label cũ bằng cách so overlap lớn nhất, rồi đánh dấu dữ liệu đã thay đổi để lưu.
    # Khi đang di chuyển, polygons_data_list là nguồn dữ liệu chính xác.
    if mask_dirty and not is_moving_mask:
        contours, _ = cv2.findContours(
            img_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        updated_polygons_data_list = []

        for new_contour in contours:
            new_poly = [tuple(pt[0]) for pt in new_contour]

            best_label = "none"
            best_overlap = 0

            for old_entry in polygons_data_list:
                if old_entry["label"] == "none":
                    continue

                overlap = calculate.polygon_overlap_area(
                    new_poly,
                    old_entry["polygon"],
                    h2, w2
                )

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_label = old_entry["label"]

            updated_polygons_data_list.append({
                "label": best_label,
                "polygon": new_poly
            })

        polygons_data_list = updated_polygons_data_list
        mask_dirty = False
        polygons_dirty = True   # ← THÊM
    img_new = img_new[:h2,:w2+100]
    
    # Đoạn này vẽ các polygon lên ảnh dưới dạng lớp phủ bán trong suốt theo label, trộn overlay vào ảnh chính, vẽ tâm mỗi polygon và (nếu bật) vẽ thêm bounding box YOLO.
    # Tạo một lớp phủ (overlay) để vẽ các vùng màu bán trong suốt
    overlay = img_new.copy()
    alpha = 0.2  # Độ trong suốt
    # Màu sắc cho các nhãn, bạn có thể tùy chỉnh
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (128,0,0), (0,128,0), (0,0,128), (128,128,0)]
    # --- Bước 1: Vẽ tất cả các vùng đa giác bán trong suốt lên lớp phủ ---
    for entry in polygons_data_list:
        poly_to_draw = np.array(entry["polygon"], dtype=np.int32)
        if len(poly_to_draw) == 0:
            continue
        
        label_str = entry.get("label", "none")
        
        # Nếu polygon đã có nhãn (là một số)
        if label_str.isdigit():
            label_index = int(label_str)
            if 0 <= label_index < len(colors):
                color = colors[label_index]
                cv2.fillPoly(overlay, [poly_to_draw], color)
        elif label_str == "none":
            # Vẽ các vùng chưa gán nhãn bằng màu vàng để dễ nhận biết
            unlabeled_color = (0, 255, 255)  # Màu vàng (B, G, R)
            cv2.fillPoly(overlay, [poly_to_draw], unlabeled_color)
    # --- Bước 2: Trộn lớp phủ vào ảnh chính ---
    cv2.addWeighted(overlay, alpha, img_new, 1 - alpha, 0, img_new)

    # --- Bước 3: Vẽ các chi tiết không trong suốt (tâm và nhãn) lên ảnh đã trộn ---
    for entry in polygons_data_list:
        center = calculate.calculate_center(entry["polygon"])
        if center:
            # Vẽ điểm trung tâm cho TẤT CẢ các vùng (giống logic cũ)
            cv2.circle(img_new, center, 5, (255, 255, 255), -1) # Chấm trắng
            cv2.circle(img_new, center, 6, (0, 0, 0), 1) # Viền đen cho dễ nhìn


    # Vẽ các khung vuông và label ở bên phải ảnh
    label_width = 90
    label_height = (h2 - 110) // 10
    offset_x = 10
    offset_y = 10
    for i in range(10):
        x1 = w2 + offset_x
        y1 = offset_y + i * (label_height + offset_y)
        x2 = w2 + label_width + offset_x
        y2 = offset_y + (i + 1) * (label_height + offset_y)

        colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (128,0,0), (0,128,0), (0,0,128), (128,128,0)]
        color = colors[i]

        label_text = name_label[str(i)][0]
        text_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = int((x2 + x1 - text_size[0]) / 2)
        text_y = int((y2 + y1 + text_size[1]) / 2)
        cv2.rectangle(img_new, (x1, y1), (x2, y2), color, -1)
        cv2.putText(img_new, label_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if label == i:
            if int(time.time() * 1000) % 500 > 250:
                cv2.rectangle(img_new, (x1, y1), (x2, y2), (0, 0, 0), 3)

    if mouse_pos != (-1, -1):
        color = (255, 255, 255) if not is_adding else (0, 255, 255)
        if eraser_shape == 'square':
            x_start = mouse_pos[0] - eraser_size // 2
            y_start = mouse_pos[1] - eraser_size // 2
            x_end = mouse_pos[0] + eraser_size // 2
            y_end = mouse_pos[1] + eraser_size // 2
            cv2.rectangle(img_new, (x_start, y_start), (x_end, y_end), color, 2)
        else:
            cv2.circle(img_new, mouse_pos, eraser_size // 2, color, 2)

    # Display temporary message if any
    if display_message and (cv2.getTickCount() - message_start_time) / cv2.getTickFrequency() * 1000 < MESSAGE_DURATION_MS:
        cv2.putText(img_new, display_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # showerror(title="error", message=display_message)
    else:
        display_message = "" # Clear message after durationq
    # if show_help:
    #     help_image = calculate.create_help_image(calculate.text, height=h2)
    #     # cv2.imshow('Help', help_image)
    #     # cv2.imshow(name_img, img_new)
    if polygons_dirty:
        if img_mask is not None and np.any(img_mask):
            # 1. Cập nhật mask từ polygon (giữ nguyên logic của bạn)
            calculate.rebuild_mask_from_polygons(img_mask, polygons_data_list)

            # 2. Cấu hình kích thước hiển thị mong muốn (ví dụ: tối đa 800px)
            max_display_size = 640
            h, w = img_mask.shape[:2]

            # Tính toán tỉ lệ để giữ nguyên Aspect Ratio
            scaling_factor = max_display_size / max(h, w)
            new_w = int(w * scaling_factor)
            new_h = int(h * scaling_factor)

            # 3. Thực hiện Resize
            # Sử dụng INTER_NEAREST để giữ nguyên các giá trị pixel của mask (0, 1, 255...) 
            # tránh bị mờ biên (aliasing)
            img_show = cv2.resize(img_mask, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

            # 4. Hiển thị
            cv2.imshow("mask", img_show)
    # --- Căn chỉnh vị trí các cửa sổ ra giữa màn hình ---
    if 'w2' in locals() and 'h2' in locals():
        main_width = img_new.shape[1]
        main_height = img_new.shape[0]

        if show_help:
            help_width = 450  # Chiều rộng cố định từ create_help_image
            total_width = help_width + main_width  # Không còn khoảng cách giữa 2 cửa sổ
            start_x = max(0, (screen_width - total_width) // 2)
            start_y = max(0, (screen_height - main_height) // 2)

            cv2.moveWindow('Help', start_x, start_y) # Cửa sổ hotkeys bên trái
            cv2.moveWindow(name_img, start_x + help_width, start_y) # Cửa sổ ảnh bên phải
        else:
            # Chỉ căn giữa cửa sổ chính nếu không hiển thị trợ giúp
            start_x = max(0, (screen_width - main_width) // 2)
            start_y = max(0, (screen_height - main_height) // 2)
            cv2.moveWindow(name_img, start_x, start_y)

    cv2.setMouseCallback(name_img, draw_polygon)

    k = cv2.waitKey(1) & 0xFF

    # Check for unlabeled polygons before saving or navigating
    unlabeled_polygons_exist = False
    for entry in polygons_data_list:
        if entry["label"] == "none":
            unlabeled_polygons_exist = True
            break

    if k == ord('p'):
        if hasattr(draw_polygon, '_yolo_results'):
            # Lấy bbox từ cache YOLO đã có
            yolo_bboxes.clear()
            results = draw_polygon._yolo_results

            for r in results:
                if hasattr(r, 'boxes') and r.boxes is not None:
                    for box in r.boxes.xyxy.cpu().numpy():
                        x1, y1, x2, y2 = map(int, box)
                        yolo_bboxes.append((x1, y1, x2, y2))

    
            message_start_time = cv2.getTickCount()

        else:
            # Không có YOLO → không làm gì
            display_message = "Chua co ket qua YOLO"
            message_start_time = cv2.getTickCount()

    if k == ord('q') or cv2.getWindowProperty(name_img, cv2.WND_PROP_VISIBLE) < 1:
        if unlabeled_polygons_exist:
            display_message = "Vui lòng gán nhãn cho tất cả các vùng hình bao!"
            message_start_time = cv2.getTickCount()
            continue # Prevent quitting
        output_file = os.path.join(forder_output, name_img.split(".")[0] + ".txt")
        folder.save_polygons_to_txt(img_mask, output_file, polygons_data_list)
        break
    elif k == ord('?'):
        show_help = not show_help
        if not show_help:
            try:
                cv2.destroyWindow('Help')
            except cv2.error:
                pass
    elif k == ord('s'):
        if not model_loaded:
            display_message = "YOLO model not loaded."
            message_start_time = cv2.getTickCount()
            continue

        temp_display = img_new.copy()
        cv2.putText(
            temp_display,
            "Running Auto-Segmentation...",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        cv2.imshow(name_img, temp_display)
        cv2.waitKey(1)

        calculate.auto_segment(img_resize, model, confidence, polygons_data_list, img_mask, yolo_bboxes)

        display_message = "Auto-segmentation complete. Please label new masks."
        message_start_time = cv2.getTickCount()
    elif k == ord('d'):
        if unlabeled_polygons_exist:
            display_message = "Vui lòng gán nhãn cho tất cả các vùng hình bao!"
            message_start_time = cv2.getTickCount()
            continue

        output_file = os.path.join(
            forder_output,
            name_img.split(".")[0] + ".txt"
        )

        if polygons_dirty:
            # if img_mask is not None and np.any(img_mask):
            #     calculate.rebuild_mask_from_polygons(img_mask, polygons_data_list)
            #     cv2.imshow("mask", img_mask)

            folder.save_polygons_to_txt(img_mask, output_file, polygons_data_list)
            print("🔄 Mask changed → saved")
            # cập nhật lại trạng thái gốc
            polygons_dirty = False
        else:
            print("⚡ Mask unchanged → skip save")

        # ===== SANG ẢNH TIẾP THEO =====
        cv2.destroyAllWindows()
        if stt < len(list_name_img) - 1:
            stt += 1
    elif k == ord('a'):
        if unlabeled_polygons_exist:
            display_message = "Vui lòng gán nhãn cho tất cả các vùng hình bao!"
            message_start_time = cv2.getTickCount()
            continue

        output_file = os.path.join(
            forder_output,
            name_img.split(".")[0] + ".txt"
        )

        if polygons_dirty:
            if img_mask is not None and np.any(img_mask):
                calculate.rebuild_mask_from_polygons(img_mask, polygons_data_list)

                mask_path = os.path.join(
                    forder_output,
                    name_img.split(".")[0] + "_mask.png"
                )
                # cv2.imwrite(mask_path, img_mask)



            folder.save_polygons_to_txt(img_mask, output_file, polygons_data_list)
            print("🔄 Mask changed → saved")
            polygons_dirty = False
        else:
            print("⚡ Mask unchanged → skip save")

        # ===== QUAY LẠI ẢNH TRƯỚC =====
        cv2.destroyAllWindows()
        if stt > 0:
            stt -= 1

    elif k == ord('c'): # Copy current polygons to polygons_cv
        polygons_cv = copy.deepcopy(polygons_data_list)
    elif k == ord('v'): # Paste polygons_cv to polygons
        polygons_data_list = copy.deepcopy(polygons_cv)
        polygons_dirty = True
        # Sau khi dán, cần cập nhật lại img_mask
        img_mask.fill(0)
        for entry in polygons_data_list:
            poly = np.array(entry["polygon"], dtype=np.int32)
            if len(poly) > 0: # Ensure polygon is not empty
                cv2.fillPoly(img_mask, [poly], 255)
    elif k == ord('o'): # Copy current polygons to polygons_op
        polygons_op = copy.deepcopy(polygons_data_list)
    elif k == ord('b'): # Paste polygons_op to polygons
        polygons_data_list = copy.deepcopy(polygons_op)
        polygons_dirty = True
        # Sau khi dán, cần cập nhật lại img_mask
        img_mask.fill(0)
        for entry in polygons_data_list:
            poly = np.array(entry["polygon"], dtype=np.int32)
            if len(poly) > 0: # Ensure polygon is not empty
                cv2.fillPoly(img_mask, [poly], 255)
    elif k == ord('r'): # Reset/Remove current image's annotations
        polygons_data_list = []
        img_mask.fill(0)
        polygons_dirty = True
        output_file = os.path.join(forder_output, name_img.split(".")[0] + ".txt")
        if os.path.exists(output_file):
            os.remove(output_file)
            print("removed annotations for current image")
    elif k == ord('u'): # Reset/Remove current image's annotations
        print("Nhận diện cạnh viền vật thể")
        mode = Mode.CLICK_PEN
        display_message = "Vào chế độ điểm"

    if mode ==  Mode.CLICK_PEN:
        x, y = mouse_pos
        size = 15
        color = (0, 0, 255)

        cv2.line(img_new, (x - size, y), (x + size, y), color, 2)
        cv2.line(img_new, (x, y - size), (x, y + size), color, 2)
cv2.destroyAllWindows()