import os
import shutil

def split_data(img_dir, label_dir, output_dir, train_ratio=0.8):

    # Xóa output cũ
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Đã xóa thư mục output cũ: {output_dir}")

    # Tạo thư mục train/images, train/labels, val/images, val/labels
    train_img_dir = os.path.join(output_dir, 'train', 'images')
    train_label_dir = os.path.join(output_dir, 'train', 'labels')
    val_img_dir = os.path.join(output_dir, 'val', 'images')
    val_label_dir = os.path.join(output_dir, 'val', 'labels')

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    # Lấy danh sách ảnh
    img_files = [f for f in os.listdir(img_dir)
                 if os.path.isfile(os.path.join(img_dir, f))]

    # Không shuffle – giữ nguyên thứ tự
    train_size = int(len(img_files) * train_ratio)
    train_files = img_files[:train_size]
    val_files = img_files[train_size:]

    def copy_files(files, img_src, label_src, img_dst, label_dst):
        for img_file in files:
            base, _ = os.path.splitext(img_file)
            label_file = base + ".txt"

            src_img_path = os.path.join(img_src, img_file)
            src_label_path = os.path.join(label_src, label_file)

            dst_img_path = os.path.join(img_dst, img_file)
            dst_label_path = os.path.join(label_dst, label_file)

            if os.path.exists(src_label_path):
                shutil.copy2(src_img_path, dst_img_path)
                shutil.copy2(src_label_path, dst_label_path)
            else:
                print(f"⚠️ Không tìm thấy nhãn cho ảnh: {img_file}")

    # Copy dữ liệu
    copy_files(train_files, img_dir, label_dir, train_img_dir, train_label_dir)
    copy_files(val_files,   img_dir, label_dir, val_img_dir,   val_label_dir)

    print("🎉 Hoàn thành tách dữ liệu theo cấu trúc train/val!")

# Ví dụ sử dụngd
img_dir = r"C:\Users\anhuv\Desktop\Train\Lay"
label_dir = r"C:\Users\anhuv\Desktop\Train\out_put"
output_dir = r"C:\Users\anhuv\Desktop\Train\out1"

split_data(img_dir, label_dir, output_dir)
