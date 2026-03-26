import os
import shutil

def copy_and_rename_images(source_folder: str, destination_folder: str):
    """
    Sao chép tất cả các tệp ảnh từ một thư mục nguồn (bao gồm các thư mục con)
    vào một thư mục đích và đổi tên chúng theo định dạng 'img<số thứ tự>.png'.

    Args:
        source_folder (str): Đường dẫn đến thư mục nguồn chứa các thư mục con có ảnh.
        destination_folder (str): Đường dẫn đến thư mục đích để lưu các ảnh đã sao chép.
    """
    # Tạo thư mục đích nếu nó chưa tồn tại
    os.makedirs(destination_folder, exist_ok=True)
    print(f"Thư mục đích '{destination_folder}' đã được chuẩn bị.")

    # Biến đếm để đánh số thứ tự cho ảnh
    counter = 1
    
    # Các định dạng ảnh được hỗ trợ
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    # Duyệt qua tất cả các thư mục và tệp trong thư mục nguồn
    print(f"Bắt đầu quét thư mục nguồn '{source_folder}'...")
    for root, _, files in os.walk(source_folder):
        for filename in files:
            # Kiểm tra nếu tệp là một ảnh
            if filename.lower().endswith(image_extensions):
                # Tạo đường dẫn đầy đủ cho tệp nguồn
                source_path = os.path.join(root, filename)
                
                # Tạo tên tệp mới
                new_filename = f"img{counter}.png"
                
                # Tạo đường dẫn đầy đủ cho tệp đích
                dest_path = os.path.join(destination_folder, new_filename)
                
                try:
                    # Sao chép và đổi tên tệp
                    shutil.copy2(source_path, dest_path)
                    print(f"Đã sao chép: '{source_path}' -> '{dest_path}'")
                    
                    # Tăng biến đếm
                    counter += 1
                except Exception as e:
                    print(f"Lỗi khi sao chép tệp '{source_path}': {e}")

    print(f"\nHoàn tất! Tổng cộng đã sao chép {counter - 1} ảnh vào '{destination_folder}'.")


# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # Thay đổi các đường dẫn này cho phù hợp với cấu trúc thư mục của bạn
    # Ví dụ trên Windows: "C:\\Users\\YourUser\\Desktop\\FolderTong"
    # Ví dụ trên macOS/Linux: "/home/YourUser/Desktop/FolderTong"
    
    source_directory = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\w913_15_1_2026\gan_nhan_training_lan_dau\vv"  # Thư mục chứa các folder con có ảnh
    destination_directory = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\w913_15_1_2026\gan_nhan_training_lan_dau\cc" # Thư mục để chứa tất cả ảnh

    # # Tạo một vài thư mục và tệp giả để chạy ví dụ
    # # Bạn có thể xóa phần này nếu đã có sẵn thư mục
    # print("--- Đang tạo dữ liệu ví dụ ---")
    # if not os.path.exists(source_directory):
    #     os.makedirs(os.path.join(source_directory, "album_1"))
    #     os.makedirs(os.path.join(source_directory, "album_2"))
    #     # Tạo các tệp ảnh giả
    #     open(os.path.join(source_directory, "album_1", "anh_1.jpg"), 'a').close()
    #     open(os.path.join(source_directory, "album_1", "anh_2.png"), 'a').close()
    #     open(os.path.join(source_directory, "album_2", "photo_A.jpeg"), 'a').close()
    #     open(os.path.join(source_directory, "album_2", "photo_B.gif"), 'a').close()
    #     open(os.path.join(source_directory, "file_van_ban.txt"), 'a').close() # Tệp này sẽ bị bỏ qua
    # print("--- Dữ liệu ví dụ đã sẵn sàng ---\n")

    # Gọi hàm để thực hiện công việc
    copy_and_rename_images(source_directory, destination_directory)
