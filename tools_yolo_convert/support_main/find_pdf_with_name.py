import os



def get_pdf_files_from_folders(folder_paths, name_file, stt = None):
    """
    Hàm nhận danh sách đường dẫn thư mục, tạo danh sách các file PDF,
    sau đó kiểm tra file PDF nào có tên bắt đầu với name_file (phân biệt chữ hoa và chữ thường).
    Nếu tìm thấy, trả về index và đường dẫn file PDF. Nếu không, trả về None.
    
    Args:
        folder_paths (list): Danh sách các đường dẫn thư mục.
        name_file (str): Tên file cần tìm (ký tự đầu của file PDF).
    
    Returns:
        tuple or None: Tuple (index, đường dẫn file PDF) nếu tìm thấy, hoặc None nếu không tìm thấy.
    """
    pdf_files = []  # Danh sách chứa tất cả các file PDF

    # Tạo danh sách các file PDF từ các thư mục
    for folder in folder_paths:
        if os.path.isdir(folder):  # Kiểm tra xem đường dẫn có phải là thư mục không
            for root, _, files in os.walk(folder):  # Duyệt qua các file trong thư mục
                for file in files:
                    if file.endswith('.pdf'):  # Kiểm tra file có đuôi .pdf
                        pdf_files.append(os.path.join(root, file))  # Thêm đường dẫn đầy đủ vào danh sách
    # Kiểm tra file nào bắt đầu với name_file
    for index, pdf_file in enumerate(pdf_files):
        if stt is not None:  # Nếu có chỉ số stt được cung cấp
            if os.path.basename(pdf_file).startswith(name_file) and index != stt:  # Kiểm tra tên file (phân biệt chữ hoa/thường)
                return index, pdf_file  # Trả về index và đường dẫn file PDF
        else:
            if os.path.basename(pdf_file).startswith(name_file):  # Kiểm tra tên file (phân biệt chữ hoa/thường)
                return index, pdf_file  # Trả về index và đường dẫn file PDF

    return None  # Không tìm thấy file phù hợp