import os

def cleanup_empty_pairs(folder_path: str):
    """
    Quét một thư mục, tìm các tệp .txt rỗng và xóa chúng cùng với
    các tệp ảnh có cùng tên cơ sở.

    Args:
        folder_path (str): Đường dẫn đến thư mục chứa các cặp tệp ảnh và txt.
    """
    if not os.path.isdir(folder_path):
        print(f"Lỗi: Thư mục '{folder_path}' không tồn tại.")
        return

    print(f"Bắt đầu quét thư mục: '{folder_path}'")
    
    # Các định dạng ảnh phổ biến để tìm kiếm
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    files_deleted_count = 0

    # Lấy danh sách tất cả các tệp trong thư mục
    try:
        all_files = os.listdir(folder_path)
    except OSError as e:
        print(f"Lỗi khi truy cập thư mục: {e}")
        return

    # Lọc ra các tệp .txt để xử lý trước
    txt_files = [f for f in all_files if f.lower().endswith('.txt')]

    for txt_filename in txt_files:
        txt_path = os.path.join(folder_path, txt_filename)

        # Kiểm tra xem tệp txt có rỗng không
        try:
            if os.path.getsize(txt_path) == 0:
                print(f"Tìm thấy tệp văn bản rỗng: '{txt_filename}'")
                
                # Lấy tên cơ sở (không có phần mở rộng)
                base_name = os.path.splitext(txt_filename)[0]
                
                # Tìm và xóa tệp ảnh tương ứng
                image_found_and_deleted = False
                for ext in image_extensions:
                    image_filename = base_name + ext
                    image_path = os.path.join(folder_path, image_filename)
                    
                    if os.path.exists(image_path):
                        try:
                            os.remove(image_path)
                            print(f"  -> Đã xóa tệp ảnh tương ứng: '{image_filename}'")
                            image_found_and_deleted = True
                            break # Dừng lại sau khi tìm thấy và xóa một ảnh
                        except OSError as e:
                            print(f"  -> Lỗi khi xóa tệp ảnh '{image_filename}': {e}")

                # Xóa tệp txt rỗng
                try:
                    os.remove(txt_path)
                    print(f"  -> Đã xóa tệp văn bản rỗng: '{txt_filename}'")
                    files_deleted_count += 1
                    if image_found_and_deleted:
                        files_deleted_count += 1
                except OSError as e:
                    print(f"  -> Lỗi khi xóa tệp văn bản '{txt_filename}': {e}")

        except FileNotFoundError:
            # Tệp có thể đã bị xóa trong một vòng lặp khác, bỏ qua
            continue
        except OSError as e:
            print(f"Lỗi khi kiểm tra tệp '{txt_filename}': {e}")

    print(f"\nHoàn tất! Đã xóa tổng cộng {files_deleted_count} tệp.")


# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # Thay đổi đường dẫn này cho phù hợp với thư mục của bạn
    target_folder = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\New folder\objectdetect_land\dataset\mixdata"

    # # --- Tạo dữ liệu ví dụ để kiểm tra (bạn có thể xóa phần này) ---
    # print("--- Đang tạo dữ liệu ví dụ ---")
    # os.makedirs(target_folder, exist_ok=True)
    # # Cặp 1: Tệp txt có nội dung -> Sẽ được giữ lại
    # with open(os.path.join(target_folder, "anh_co_chu_thich.txt"), "w") as f:
    #     f.write("Đây là con mèo.")
    # open(os.path.join(target_folder, "anh_co_chu_thich.jpg"), "a").close()

    # # Cặp 2: Tệp txt rỗng -> Sẽ bị xóa
    # open(os.path.join(target_folder, "anh_can_xoa.txt"), "a").close()
    # open(os.path.join(target_folder, "anh_can_xoa.png"), "a").close()

    # # Cặp 3: Tệp txt rỗng khác -> Sẽ bị xóa
    # open(os.path.join(target_folder, "hinh_bo_di.txt"), "a").close()
    # open(os.path.join(target_folder, "hinh_bo_di.jpeg"), "a").close()
    
    # # Tệp không liên quan -> Sẽ được giữ lại
    # open(os.path.join(target_folder, "tai_lieu_quan_trong.pdf"), "a").close()
    # print("--- Dữ liệu ví dụ đã sẵn sàng ---\n")

    # Gọi hàm để dọn dẹp
    cleanup_empty_pairs(target_folder)
