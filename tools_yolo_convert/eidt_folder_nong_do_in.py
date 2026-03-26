import os
 
def delete_duplicates(source_folder: str, target_folder: str):
    """
    Kiểm tra các tệp trong target_folder và xóa những tệp có tên trùng
    với các tệp trong source_folder.
 
    Args:
        source_folder (str): Đường dẫn đến thư mục nguồn.
        target_folder (str): Đường dẫn đến thư mục đích để kiểm tra và xóa.
    """
    # 1. Kiểm tra xem các đường dẫn thư mục có hợp lệ không
    if not os.path.isdir(source_folder):
        print(f"Lỗi: Thư mục nguồn '{source_folder}' không tồn tại hoặc không phải là một thư mục.")
        return
    if not os.path.isdir(target_folder):
        print(f"Lỗi: Thư mục đích '{target_folder}' không tồn tại hoặc không phải là một thư mục.")
        return
 
    print(f"Bắt đầu quá trình kiểm tra và xóa tệp trùng lặp...")
    print(f" - Thư mục nguồn: {source_folder}")
    print(f" - Thư mục đích:  {target_folder}\n")
 
    try:
        # 2. Lấy danh sách tên tệp từ cả hai thư mục
        # Sử dụng set cho thư mục đích để tăng tốc độ tìm kiếm
        source_files = os.listdir(source_folder)
        target_files_set = set(os.listdir(target_folder))
       
        deleted_count = 0
 
        # 3. Lặp qua các tệp trong thư mục nguồn
        for filename in source_files:
            # 4. Nếu tệp tồn tại trong thư mục đích, hãy xóa nó
            if filename in target_files_set:
                file_to_delete = os.path.join(target_folder, filename)
               
                try:
                    # Đảm bảo rằng đó là một tệp trước khi xóa
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)
                        print(f"Đã xóa: {file_to_delete}")
                        deleted_count += 1
                except OSError as e:
                    print(f"Lỗi khi xóa tệp '{file_to_delete}': {e}")
 
        if deleted_count == 0:
            print("Không tìm thấy tệp nào trùng lặp để xóa.")
        else:
            print(f"\nHoàn tất. Tổng cộng đã xóa {deleted_count} tệp.")
 
    except OSError as e:
        print(f"Lỗi khi truy cập thư mục: {e}")
 
 
# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # Vui lòng thay đổi các đường dẫn này thành đường dẫn thực tế trên máy của bạn
    # Ví dụ trên Windows: "C:\\Users\\YourUser\\Desktop\\Folder1"
    # Ví dụ trên macOS/Linux: "/home/youruser/Desktop/Folder1"
    folder1 = r"D:\tupn\data_training\kiem_tra_trang_in\classifi\truong_hop_3_label\data_all\edit_NG"
    folder2 = r"D:\tupn\data_training\kiem_tra_trang_in\classifi\truong_hop_3_label\data_all\NG"
 
    delete_duplicates(folder1, folder2)
 
 