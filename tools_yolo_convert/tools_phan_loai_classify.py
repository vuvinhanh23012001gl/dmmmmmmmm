import os
import shutil
from ultralytics import YOLO
from pathlib import Path

def classify_and_copy_images(root_folder: str, model_path: str, max_images: int, output_dir: str = "output_classified"):
    """
    Phân loại ảnh từ một cấu trúc thư mục lồng nhau bằng model YOLOv8
    và sao chép chúng vào các thư mục theo class cho đến khi đủ số lượng.

    Args:
        root_folder (str): Đường dẫn đến thư mục gốc (Folder A) chứa ảnh trong các thư mục con.
        model_path (str): Đường dẫn đến tệp model YOLOv8 classification (.pt) đã được training.
        max_images (int): Tổng số ảnh cần phân loại và sao chép trước khi dừng lại.
        output_dir (str): Thư mục nơi các thư mục ảnh đã phân loại sẽ được tạo.
    """
    # 1. Kiểm tra tính hợp lệ của đầu vào
    if not os.path.isdir(root_folder):
        print(f"Lỗi: Thư mục đầu vào '{root_folder}' không tồn tại.")
        return
    if not os.path.isfile(model_path):
        print(f"Lỗi: Tệp model '{model_path}' không tồn tại.")
        return

    # 2. Tải model YOLO
    try:
        model = YOLO(model_path)
        class_names = model.names
        print(f"Đã tải model thành công. Các class: {list(class_names.values())}")
    except Exception as e:
        print(f"Lỗi khi tải model: {e}")
        return

    # 3. Tạo các thư mục đầu ra cho mỗi class
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for class_name in class_names.values():
        Path(os.path.join(output_dir, class_name)).mkdir(parents=True, exist_ok=True)
    print(f"Đã tạo các thư mục đầu ra trong '{output_dir}'.")

    # 4. Xử lý ảnh
    processed_count = 0
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')

    print("Bắt đầu quá trình phân loại và sao chép ảnh...")
    
    # Sử dụng os.walk để duyệt qua tất cả các thư mục con
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            # Nếu đã xử lý đủ số lượng ảnh thì dừng lại
            if processed_count >= max_images:
                print(f"\nĐã xử lý đủ {max_images} ảnh. Dừng lại.")
                return

            if filename.lower().endswith(image_extensions):
                image_path = os.path.join(dirpath, filename)

                try:
                    # Thực hiện dự đoán
                    results = model(image_path, verbose=False) # verbose=False để output gọn gàng

                    # Lấy class có xác suất cao nhất
                    probs = results[0].probs
                    top1_index = probs.top1


                    
                    predicted_class_name = class_names[top1_index]

                    # Xác định đường dẫn đích và sao chép tệp
                    destination_folder = os.path.join(output_dir, predicted_class_name)
                    destination_path = os.path.join(destination_folder, filename)
                    
                    # Xử lý trường hợp tên file bị trùng lặp
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(filename)
                        i = 1
                        while os.path.exists(destination_path):
                            new_filename = f"{base}_{i}{ext}"
                            destination_path = os.path.join(destination_folder, new_filename)
                            i += 1

                    shutil.copy2(image_path, destination_path) # copy2 giữ lại metadata của file

                    processed_count += 1
                    print(f"({processed_count}/{max_images}) Đã sao chép '{filename}' vào thư mục '{predicted_class_name}'")

                except Exception as e:
                    print(f"Lỗi khi xử lý ảnh '{image_path}': {e}")

    print(f"\nHoàn tất! Đã xử lý và sao chép tổng cộng {processed_count} ảnh.")


if __name__ == '__main__':
    # --- CẤU HÌNH ---
    # 1. Đường dẫn đến thư mục A chứa các thư mục con có ảnh
    FOLDER_A_PATH = r"D:\tupn\data_training\AI_BIL\w913_0060\classify\dung_tools_phan_loai_lan_dau\input_check_2"

    # 2. Đường dẫn đến file model .pt đã training (thường là best.pt)
    MODEL_PATH = r"D:\tupn\yolo\runs\classify\BIL_w913_0060_tools_phan_loai_lan_1\weights\best.pt"

    # 3. Số lượng ảnh tối đa cần kiểm tra và sao chép
    NUM_IMAGES_TO_CHECK = 300000

    path_output = r"D:\tupn\data_training\AI_BIL\w913_0060\classify\dung_tools_phan_loai_lan_dau\output_check_2"  # Thư mục đầu ra (mặc định là 'output_classified')

    # --- THỰC THI ---
    classify_and_copy_images(
        root_folder=FOLDER_A_PATH,
        model_path=MODEL_PATH,
        max_images=NUM_IMAGES_TO_CHECK,
        output_dir=path_output
    )
