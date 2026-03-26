import os
import shutil
import random

def split_classification_data(source_folders, output_folder, train_ratio=0.8):
    """
    Chia dữ liệu từ các thư mục lớp nguồn vào cấu trúc train/val cho bài toán classification.

    Args:
        source_folders (list): Danh sách các đường dẫn đến thư mục nguồn, mỗi thư mục chứa ảnh của một lớp.
        output_folder (str): Đường dẫn đến thư mục đầu ra để chứa các tập train/val.
        train_ratio (float): Tỷ lệ dữ liệu cho tập huấn luyện (mặc định là 0.8).
    """
    # Tạo các thư mục train và val chính
    train_dir = os.path.join(output_folder, 'train')
    val_dir = os.path.join(output_folder, 'val')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    print(f"Đang xử lý {len(source_folders)} lớp...")

    for source_folder in source_folders:
        if not os.path.isdir(source_folder):
            print(f"Cảnh báo: Bỏ qua '{source_folder}' vì không phải là thư mục.")
            continue

        # Lấy tên lớp từ tên thư mục nguồn
        class_name = os.path.basename(source_folder)
        print(f"\n--- Đang xử lý lớp: {class_name} ---")

        # Tạo thư mục con cho lớp trong train và val
        train_class_dir = os.path.join(train_dir, class_name)
        val_class_dir = os.path.join(val_dir, class_name)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(val_class_dir, exist_ok=True)

        # Lấy danh sách tất cả các file ảnh
        images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        random.shuffle(images)

        # Chia danh sách ảnh
        split_index = int(len(images) * train_ratio)
        train_images = images[:split_index]
        val_images = images[split_index:]

        # Sao chép file vào thư mục train
        for image_name in train_images:
            shutil.copy(os.path.join(source_folder, image_name), os.path.join(train_class_dir, image_name))

        # Sao chép file vào thư mục val
        for image_name in val_images:
            shutil.copy(os.path.join(source_folder, image_name), os.path.join(val_class_dir, image_name))

        print(f"Đã chia lớp '{class_name}': {len(train_images)} ảnh train, {len(val_images)} ảnh val.")

    print("\nHoàn tất việc chia dữ liệu!")


if __name__ == "__main__":
    # --- THAY ĐỔI CÁC ĐƯỜNG DẪN BÊN DƯỚI ---

    # # 1. Danh sách các thư mục chứa ảnh gốc của bạn (mỗi thư mục là một lớp)
    # source_class_folders = [
    #     r"D:\tupn\data_training\AI_BIL\w001_0061\data_all\00_no_kote",  # Ví dụ: thư mục chứa ảnh chó
    #     r"D:\tupn\data_training\AI_BIL\w001_0061\data_all\01_kote_touch",  # Ví dụ: thư mục chứa ảnh mèo
    #     r"D:\tupn\data_training\AI_BIL\w001_0061\data_all\02_solder_touch"   # Ví dụ: thư mục chứa ảnh mèo
    # ]

    # # 2. Thư mục đầu ra để chứa bộ dữ liệu đã chia
    # output_dataset_folder = r'D:\tupn\data_training\AI_BIL\w001_0061\chia_80_20'

    # 1. Danh sách các thư mục chứa ảnh gốc của bạn (mỗi thư mục là một lớp)
    # source_class_folders = [
    #     r"D:\tupn\AI BIL\data_training\data_LV_EL\0061\phan_loai_30_10\20251025\loai_27_da_phan_loai_lan2\loai_27_da_phan_loai_lan2\loai_27\output_1\00_no_kote",  # Ví dụ: thư mục chứa ảnh chó
    #     r"D:\tupn\AI BIL\data_training\data_LV_EL\0061\phan_loai_30_10\20251025\loai_27_da_phan_loai_lan2\loai_27_da_phan_loai_lan2\loai_27\output_1\01_kote_touch",  # Ví dụ: thư mục chứa ảnh mèo
    #     r"D:\tupn\AI BIL\data_training\data_LV_EL\0061\phan_loai_30_10\20251025\loai_27_da_phan_loai_lan2\loai_27_da_phan_loai_lan2\loai_27\output_1\02_solder_touch",  # Ví dụ: thư mục chứa ảnh mèo
    # ]

    source_class_folders = [
        r"D:\tupn\data_training\AI_BIL\w913_0060\classify\tao_tools_phan_loai\phan_loai\00_no_kote",  # Ví dụ: thư mục chứa ảnh chó
        r"D:\tupn\data_training\AI_BIL\w913_0060\classify\tao_tools_phan_loai\phan_loai\00_no_solder",
        r"D:\tupn\data_training\AI_BIL\w913_0060\classify\tao_tools_phan_loai\phan_loai\01_solder_touch"
    ]

    # 2. Thư mục đầu ra để chứa bộ dữ liệu đã chia
    output_dataset_folder = r'D:\tupn\data_training\AI_BIL\w913_0060\classify\tao_tools_phan_loai\chia_80_20'

    # Chạy hàm chia dữ liệu
    split_classification_data(source_class_folders, output_dataset_folder, train_ratio=0.8)