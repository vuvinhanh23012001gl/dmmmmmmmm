import cv2
import os
from ultralytics import YOLO

 
path_weight_giac = r"D:\tupn\yolo\runs\detect\fuser_dll_3_label_ver2\weights\best.pt"
load_model = 0
model = ""    
 
def xu_ly_anh(img,weights = path_weight_giac):
    global load_model, model
    error = ""
    if load_model == 0:
        model = YOLO(weights)
    result = model(img)
    print(result)
    xyxy = result[0].boxes.xyxy.tolist()
    labels = result[0].boxes.cls.tolist()
    conf = result[0].boxes.conf.tolist()
    # NG1 - khong co giac cam, NG2 - nhan dien giac cam kem
    if len(conf) == 0:
        error = "NG1"
    else:
        for i in range(0,len(conf)):
            if conf[i] < 0.5:
                error = "NG2"
    # Chuyển đổi các giá trị trong danh sách xyxy từ float sang int
    xyxy_int = [[int(coord) for coord in box] for box in xyxy]
    labels = [str(int(box)) for box in labels]
    return xyxy_int,labels,conf,error
 
def crop_images_with_detection_from_folder(input_folder_path, output_folder_path, delta=20):
    """
    Tải ảnh từ thư mục input_folder_path, sử dụng convert_circle.xu_ly_anh để phát hiện đối tượng,
    cắt các vùng được phát hiện với một khoảng delta cho trước, và lưu chúng vào output_folder_path.
 
    Args:
        input_folder_path (str): Đường dẫn đến thư mục chứa ảnh đầu vào.
        output_folder_path (str): Đường dẫn đến thư mục lưu ảnh đã cắt.
        delta (int): Khoảng pixel để mở rộng/thu hẹp vùng cắt. Tọa độ cắt sẽ dựa trên
                     [x1-delta, y1-delta, x2+delta, y2+delta].
                     Ảnh thực tế sẽ được cắt theo: img[y1-delta:y2+delta, x1-delta:x2+delta].
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Đã tạo thư mục đầu ra: {output_folder_path}")
 
    # Hàm xu_ly_anh trong convert_circle.py sẽ tự quản lý việc tải model.
    # Cần đảm bảo rằng convert_circle.path_weight_giac được thiết lập đúng
    # và tệp model tồn tại. Điều này được xử lý bên trong convert_circle.py.
 
    for image_filename in os.listdir(input_folder_path):
        image_path = os.path.join(input_folder_path, image_filename)
       
        # Kiểm tra nếu là tệp và có định dạng ảnh phổ biến
        if not os.path.isfile(image_path) or not image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            print(f"Bỏ qua tệp không phải ảnh hoặc định dạng không hỗ trợ: {image_filename}")
            continue
 
        print(f"Đang xử lý ảnh: {image_path}")
        img = cv2.imread(image_path)
 
        if img is None:
            print(f"Không thể tải ảnh: {image_path}. Bỏ qua.")
            continue
 
        # Lấy các phát hiện bằng xu_ly_anh
        # xu_ly_anh trả về: xyxy_int, labels, conf, error
        xyxy_list, _, _, error_msg = xu_ly_anh(img)
 
        if error_msg:
            print(f"Lỗi khi phát hiện đối tượng trong {image_filename}: {error_msg}. Bỏ qua việc cắt ảnh này.")
            continue
       
        if not xyxy_list:
            print(f"Không phát hiện đối tượng nào trong {image_filename}. Bỏ qua việc cắt ảnh này.")
            continue
 
        img_height, img_width = img.shape[:2]
 
        for i, box_coords in enumerate(xyxy_list):
            x1, y1, x2, y2 = box_coords
 
            # Áp dụng delta vào tọa độ và đảm bảo nằm trong giới hạn ảnh
            crop_x1 = max(0, x1 - delta)
            crop_y1 = max(0, y1 - delta)
            crop_x2 = min(img_width, x2 + delta)
            crop_y2 = min(img_height, y2 + delta)
 
            if crop_x1 >= crop_x2 or crop_y1 >= crop_y2:
                print(f"Kích thước cắt không hợp lệ cho hộp {i} trong {image_filename} sau khi áp dụng delta. Bỏ qua hộp này.")
                continue
           
            cropped_image = img[crop_y1:crop_y2, crop_x1:crop_x2]
 
            base_name, ext = os.path.splitext(image_filename)
            cropped_filename = f"{base_name}_crop_{i}{ext}"
            output_path = os.path.join(output_folder_path, cropped_filename)
           
            try:
                cv2.imwrite(output_path, cropped_image)
                print(f"Đã lưu ảnh đã cắt: {output_path}")
            except Exception as e:
                print(f"Lỗi khi lưu ảnh đã cắt {output_path}: {e}")
 
if __name__ == '__main__':
    path_input_folder = r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\oject\cut_anh\images_goc"
    path_output_folder = r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\oject\cut_anh\images"
    crop_images_with_detection_from_folder(path_input_folder, path_output_folder)
 
 