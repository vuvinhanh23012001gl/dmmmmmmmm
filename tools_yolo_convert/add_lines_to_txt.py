import os

def append_lines_to_txt_files(folder_path: str, lines_to_add: list):
    """
    Duyệt qua một thư mục và thêm các dòng văn bản được chỉ định vào cuối mỗi tệp .txt.

    Args:
        folder_path (str): Đường dẫn đến thư mục chứa các tệp .txt.
        lines_to_add (list): Một danh sách các chuỗi, mỗi chuỗi là một dòng để thêm vào tệp.
    """
    # 1. Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(folder_path):
        print(f"Lỗi: Thư mục '{folder_path}' không tồn tại.")
        return

    # 2. Chuẩn bị nội dung cần thêm
    # Thêm ký tự xuống dòng (\n) vào trước và giữa các dòng để đảm bảo chúng nằm trên các dòng riêng biệt
    content_to_append = "\n" + "\n".join(lines_to_add)

    print(f"Bắt đầu xử lý các tệp trong thư mục: {folder_path}")
    file_count = 0

    # 3. Duyệt qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        # Chỉ xử lý các tệp có đuôi .txt
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Mở tệp ở chế độ 'a' (append - ghi tiếp vào cuối)
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(content_to_append)
                print(f"Đã thêm 2 dòng vào tệp: {filename}")
                file_count += 1
            except Exception as e:
                print(f"Lỗi khi xử lý tệp '{filename}': {e}")

    print(f"\nHoàn tất! Đã cập nhật thành công {file_count} tệp .txt.")

if __name__ == '__main__':
    # --- CẤU HÌNH ---
    # Vui lòng thay đổi đường dẫn này đến thư mục chứa các tệp .txt của bạn
    TARGET_FOLDER = r"D:\tupn\data_training\agv_shipping\nhan_dien_cang_pallet\data_all\label"

    LINES = [
        "1 0.619271 0.462269 0.122396 0.070833",
        "1 0.797656 0.455324 0.122396 0.070833"
    ]

    # --- THỰC THI ---
    append_lines_to_txt_files(TARGET_FOLDER, LINES)
