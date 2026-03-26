import os
import shutil

def sao_chep_txt_cho_anh(thu_muc_anh, thu_muc_txt, duong_dan_file_txt_nguon):
    """
    Sao chép một file txt nguồn vào một thư mục khác cho mỗi ảnh trong thư mục ảnh.

    Tên của file txt mới sẽ trùng với tên của file ảnh tương ứng (không có phần mở rộng).

    Args:
        thu_muc_anh (str): Đường dẫn đến thư mục chứa các file ảnh.
        thu_muc_txt (str): Đường dẫn đến thư mục để lưu các file txt được sao chép.
        duong_dan_file_txt_nguon (str): Đường dẫn đến file txt nguồn cần sao chép.
    """
    # Các phần mở rộng file ảnh hợp lệ
    cac_duoi_file_anh = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # 1. Kiểm tra xem thư mục ảnh và file txt nguồn có tồn tại không
    if not os.path.isdir(thu_muc_anh):
        print(f"Lỗi: Thư mục ảnh '{thu_muc_anh}' không tồn tại.")
        return
    if not os.path.isfile(duong_dan_file_txt_nguon):
        print(f"Lỗi: File txt nguồn '{duong_dan_file_txt_nguon}' không tồn tại.")
        return

    # 2. Tạo thư mục txt đích nếu nó chưa tồn tại
    os.makedirs(thu_muc_txt, exist_ok=True)

    # 3. Lặp qua tất cả các file trong thư mục ảnh
    so_luong_file_da_tao = 0
    for ten_file_anh in os.listdir(thu_muc_anh):
        # Tách tên file và phần mở rộng
        ten_goc, phan_mo_rong = os.path.splitext(ten_file_anh)
        
        # 4. Kiểm tra xem file có phải là ảnh không
        if phan_mo_rong.lower() in cac_duoi_file_anh:
            # 5. Tạo đường dẫn đích cho file txt mới
            duong_dan_file_txt_dich = os.path.join(thu_muc_txt, f"{ten_goc}.txt")

            # 6. Sao chép file txt nguồn vào đích với tên mới
            try:
                shutil.copy(duong_dan_file_txt_nguon, duong_dan_file_txt_dich)
                so_luong_file_da_tao += 1
            except Exception as e:
                print(f"Không thể sao chép file cho ảnh '{ten_file_anh}': {e}")

    print(f"Hoàn tất! Đã tạo thành công {so_luong_file_da_tao} file .txt trong thư mục '{thu_muc_txt}'.")


# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # Giả sử cấu trúc thư mục của bạn như sau:
    # /path/to/your/project/
    # │
    # ├── images/
    # │   ├── cat.jpg
    # │   ├── dog.png
    # │   └── bird.jpeg
    # │
    # ├── labels/  (thư mục này sẽ được tạo nếu chưa có)
    # │
    # └── template.txt (file này chứa nội dung bạn muốn sao chép)

    # --- Bạn cần thay đổi các đường dẫn này cho phù hợp với máy của bạn ---
    

    # Tạo các đường dẫn tương đối
    thu_muc_chua_anh = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\kote_4_diem"
    thu_muc_chua_txt = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\kote_4_diem_output"
    file_txt_nguon = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\0104.txt"

    # thu_muc_chua_anh = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\kote_5_diem"
    # thu_muc_chua_txt = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\kote_5_diem_output"
    # file_txt_nguon = r"D:\tupn\AI BIL\data_training\data_LV_EL\0060\ojectdetect\2B (137).txt"


    # --- Chuẩn bị các file và thư mục mẫu để chạy ví dụ ---
    print("Đang tạo các file và thư mục mẫu cho ví dụ...")
    os.makedirs(thu_muc_chua_anh, exist_ok=True)
    # # Tạo các file ảnh giả
    # for img in ["cat.jpg", "dog.png", "bird.jpeg", "document.pdf"]:
    #     with open(os.path.join(thu_muc_chua_anh, img), "w") as f:
    #         f.write("dummy image data")
    # # Tạo file txt nguồn giả
    # with open(file_txt_nguon, "w") as f:
    #     f.write("Đây là nội dung mẫu.")
    # print("Đã tạo xong file mẫu.\n")
    # --- Kết thúc phần chuẩn bị ---

    # Gọi hàm để thực hiện công việc
    print("Bắt đầu quá trình sao chép...")
    sao_chep_txt_cho_anh(
        thu_muc_anh=thu_muc_chua_anh,
        thu_muc_txt=thu_muc_chua_txt,
        duong_dan_file_txt_nguon=file_txt_nguon
    )

    # Kết quả mong đợi:
    # Thư mục 'labels' sẽ được tạo (nếu chưa có).
    # Bên trong thư mục 'labels' sẽ có các file:
    # - cat.txt
    # - dog.txt
    # - bird.txt
    # Mỗi file này sẽ có nội dung giống hệt file 'template.txt'.
    # File 'document.pdf' trong thư mục 'images' sẽ được bỏ qua.
