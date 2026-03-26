import os
from ultralytics import YOLO
import numpy as np
import path
import cv2
import support_main.edit_file_txt as edit_file_txt
import shutil
# Import pybboxes and related conversion functions are removed as they are for bounding boxes (VOC/YOLO), not segmentation masks.
from support_main.lib_main import remove, load_data_csv, edit_csv_tab
import os

# --- Thiết lập Đường dẫn và Cấu hình ---
# Giả định 'path' module và các hàm support_main là có sẵn và hoạt động
path_phan_mem = path.path_phan_mem
path_setting = path_phan_mem + "/setting/setting_gan_nhan_tu_dong_segment.csv"

# Load cấu hình
data_setting = load_data_csv.ds_data(path_setting)[0]
for item in data_setting:
    if len(item) == 2:
        if item[0] == "path_weights":
            path_weights = item[1]
        if item[0] == "path_folder_input":
            path_folder_input = item[1]
        if item[0] == "path_label_output":
            path_label_output = item[1]

# Khởi tạo mô hình trên GPU (nếu có)
model = YOLO(path_weights)

# --- Hàm Chuyển đổi và Xử lý Dữ liệu ---

def convert_mask_to_yolo_segmentation(mask, class_id, w, h):
    """
    Chuyển đổi mặt nạ (mask) thành định dạng polygon chuẩn hóa YOLO segmentation,
    kết hợp tất cả các đường bao tìm được.
    """
    # Tìm các đường bao (contours) từ mặt nạ.
    # Sử dụng cv2.RETR_LIST hoặc cv2.RETR_EXTERNAL để đảm bảo lấy hết các phần
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None

    # Danh sách để chứa tất cả các điểm đã chuẩn hóa
    all_normalized_points = []
    
    # ⚠️ Xử lý TẤT CẢ các đường bao (contour), không chỉ cái lớn nhất
    for contour in contours:
        # Làm phẳng (flatten) và chuẩn hóa (normalize) các điểm
        points = contour.flatten().astype(float)
        
        # Chỉ xử lý các đường bao có ít nhất 3 điểm (là một polygon)
        if len(points) >= 6: 
            for i in range(0, len(points), 2):
                x_norm = points[i] / w
                y_norm = points[i+1] / h
                
                # Giới hạn giá trị trong khoảng [0, 1] và định dạng 6 chữ số thập phân
                x_norm = max(0.0, min(1.0, x_norm))
                y_norm = max(0.0, min(1.0, y_norm))
                
                all_normalized_points.extend([f"{x_norm:.6f}", f"{y_norm:.6f}"]) 

    if not all_normalized_points:
        return None
        
    # Ghép class_id và tất cả các điểm lại thành một dòng
    return [str(class_id)] + all_normalized_points


def process_image_segmentation(path_img):
    """
    Chạy mô hình segmentation trên ảnh và trích xuất dữ liệu nhãn YOLO.
    
    Returns:
        list: Danh sách các chuỗi nhãn YOLO segmentation.
    """
    yolo_labels = []
    
    img = cv2.imread(path_img)
    if img is None:
        print(f"Lỗi: Không thể đọc ảnh tại {path_img}")
        return []
        
    h, w, _ = img.shape # Kích thước GỐC (510, 984)
    
    # Chạy mô hình
    result = model(img)[0]
    
    labels = result.boxes.cls.tolist()
    
    if result.masks is None:
        print("Cảnh báo: Không tìm thấy mặt nạ (masks) trong kết quả.")
        return []
        
    masks = result.masks.data.cpu().numpy() # Lấy dữ liệu mặt nạ từ tensor
    
    # LƯU Ý QUAN TRỌNG: YOLOv8 cung cấp một hàm masks.xyxy, nhưng khi làm việc 
    # với numpy array, bạn cần tự resize mask về kích thước ảnh gốc.
    
    # Xử lý từng mặt nạ
    for i in range(len(labels)):
        class_id = int(labels[i])
        mask_np = masks[i] # Mặt nạ dự đoán (ví dụ: 352 x 640)
        
        # ⚠️ BƯỚC SỬA LỖI: RESIZE mặt nạ về kích thước ảnh GỐC (w, h)
        # Sử dụng nội suy NEAREST vì đây là mặt nạ nhị phân (0 hoặc 1)
        resized_mask = cv2.resize(
            mask_np, 
            (w, h), # Kích thước đích là (w, h) của ảnh gốc
            interpolation=cv2.INTER_NEAREST 
        )
        
        # Chuyển đổi mặt nạ đã resize sang chuỗi nhãn YOLO segmentation
        yolo_segmentation_line = convert_mask_to_yolo_segmentation(resized_mask, class_id, w, h)
        
        if yolo_segmentation_line:
            yolo_labels.append(yolo_segmentation_line) 
            
    return yolo_labels


def save_yolo_segmentation_labels(path_file, data):
    """
    Tạo và ghi nội dung nhãn YOLO segmentation vào một tệp .txt.

    Args:
        path_file (str): Đường dẫn đầy đủ đến tệp nhãn (.txt) sẽ được ghi.
        data (list): Danh sách các nhãn, trong đó mỗi nhãn là một danh sách
                     chứa [class_id, x1_norm, y1_norm, x2_norm, y2_norm, ...].
                     Ví dụ: [['0', '0.500', '0.500', ...], [...]]
    """
    # Chuyển đổi mỗi danh sách nhãn thành một chuỗi duy nhất
    # Dùng ' ' để nối class_id và các tọa độ lại
    lines = []
    for label_data in data:
        # Đảm bảo tất cả các phần tử trong label_data đều là chuỗi
        line = " ".join(map(str, label_data))
        lines.append(line)
        
    # Nối tất cả các chuỗi nhãn lại bằng ký tự xuống dòng
    content = "\n".join(lines)

    # Ghi nội dung vào tệp
    try:
        with open(path_file, 'w') as f:
            f.write(content)
        # print(f"Đã lưu thành công nhãn segmentation vào: {path_file}")
    except Exception as e:
        print(f"Lỗi khi ghi file nhãn {path_file}: {e}")
def segment_and_save_yolo_labels(path_folder):
    """
    Duyệt qua thư mục ảnh, thực hiện segmentation và lưu nhãn YOLO.
    """
    list_img = os.listdir(path_folder)
    print(f"Tìm thấy {len(list_img)} ảnh để xử lý.")
    
    for i, file_name in enumerate(list_img):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', ".bmp")):
            path_img = os.path.join(path_folder, file_name)
            name_img = os.path.splitext(os.path.basename(path_img))[0]
            
            print(f"[{i+1}/{len(list_img)}] Xử lý ảnh: {file_name}")
            
            # Lấy dữ liệu nhãn segmentation
            det_yolo_segmentation = process_image_segmentation(path_img)

            # Lưu nhãn vào file .txt
            # data cần là list of list [['class_id', 'x1', 'y1', ...], [...]]
            # CODE MỚI:
            save_yolo_segmentation_labels(
                path_file = os.path.join(path_label_output, f"{name_img}.txt"),
                data = det_yolo_segmentation
            )
            print(f"  -> Đã lưu {len(det_yolo_segmentation)} nhãn phân đoạn.")
        else:
            print(f"[{i+1}/{len(list_img)}] Bỏ qua file: {file_name} (Không phải ảnh)")
    
# --- Chạy Chương trình Chính ---       
if __name__ == "__main__":
    # Đảm bảo thư mục đầu ra tồn tại
    if not os.path.exists(path_label_output):
        os.makedirs(path_label_output)
        
    segment_and_save_yolo_labels(path_folder_input)
    print("Hoàn thành quá trình gắn nhãn tự động cho segmentation.")