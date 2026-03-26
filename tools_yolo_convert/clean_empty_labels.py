import os
import path
from support_main.lib_main import load_data_csv

path_phan_mem = path.path_phan_mem
path_setting = path_phan_mem + "/setting/setting_check_folder.csv"

def main():
    # Cau hinh duong dan thu muc truc tiep
    image_folder = r"D:\tupn\data_training\FC_fuser\kiem_tra_gan_nhan\data_all"
    txt_folder = r"D:\tupn\data_training\FC_fuser\kiem_tra_gan_nhan\output_oject"

    if not image_folder or not txt_folder:
        print("Chua cau hinh image_folder hoac txt_folder.")
        return

    print(f"Dang kiem tra thu muc anh: {image_folder}")
    print(f"Dang kiem tra thu muc nhan: {txt_folder}")

    list_img = os.listdir(image_folder)
    valid_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    count_deleted = 0

    for img_name in list_img:
        name, ext = os.path.splitext(img_name)
        if ext.lower() not in valid_exts:
            continue

        img_path = os.path.join(image_folder, img_name)
        txt_path = os.path.join(txt_folder, name + ".txt")

        should_delete = False
        
        if not os.path.exists(txt_path):
            print(f"Khong co file txt: {img_name} -> Xoa.")
            should_delete = True
        elif os.path.getsize(txt_path) == 0:
            print(f"File txt rong: {img_name} -> Xoa.")
            should_delete = True
            
        if should_delete:
            # os.remove(img_path)
            if os.path.exists(txt_path):
                os.remove(txt_path)
            count_deleted += 1
            
    print(f"Hoan thanh. Da xoa {count_deleted} anh/cap file.")

if __name__ == "__main__":
    main()