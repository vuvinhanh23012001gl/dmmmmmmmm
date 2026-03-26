import os

def remove_blank_lines_in_folder(folder_path: str):
    """
    Duyệt qua một thư mục, đọc từng tệp .txt, xóa các dòng trống
    và ghi lại nội dung đã được làm sạch.

    Args:
        folder_path (str): Đường dẫn đến thư mục chứa các tệp .txt.
    """
    # 1. Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(folder_path):
        print(f"Lỗi: Thư mục '{folder_path}' không tồn tại.")
        return

    print(f"Bắt đầu xóa dòng trống trong các tệp .txt tại: {folder_path}")
    processed_count = 0
    
    # 2. Duyệt qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Đọc tất cả các dòng từ tệp
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Lọc ra những dòng không trống
                # line.strip() sẽ xóa khoảng trắng ở đầu và cuối dòng. Nếu kết quả là một chuỗi rỗng, đó là dòng trống.
                non_blank_lines = [line for line in lines if line.strip()]

                # Chỉ ghi lại tệp nếu nội dung có thay đổi (số dòng giảm)
                if len(non_blank_lines) < len(lines):
                    # Ghi lại các dòng không trống vào tệp (ghi đè)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(non_blank_lines)
                    print(f"Đã xóa các dòng trống trong tệp: {filename}")
                    processed_count += 1

            except Exception as e:
                print(f"Lỗi khi xử lý tệp '{filename}': {e}")

    print(f"\nHoàn tất! Đã xử lý và làm sạch {processed_count} tệp.")

if __name__ == '__main__':
    # --- CẤU HÌNH ---
    # Vui lòng thay đổi đường dẫn này đến thư mục chứa các tệp .txt của bạn
    TARGET_FOLDER = r"D:\tupn\data_training\agv_shipping\nhan_dien_cang_pallet\data_all\label"

    # --- THỰC THI ---
    remove_blank_lines_in_folder(TARGET_FOLDER)
