import os
import shutil
import random
 
def split_data(image_folder, label_folder, train_img_folder, train_label_folder, val_img_folder, val_label_folder, train_ratio=0.8):
    """
    Split images and corresponding label files into training and validation sets.
 
    :param image_folder: Path to the folder containing image files.
    :param label_folder: Path to the folder containing label (.txt) files.
    :param train_img_folder: Path to the output folder for training images.
    :param train_label_folder: Path to the output folder for training labels.
    :param val_img_folder: Path to the output folder for validation images.
    :param val_label_folder: Path to the output folder for validation labels.
    :param train_ratio: Ratio of data to be used for training (default is 0.8).
    """
    # Ensure output folders exist
    os.makedirs(train_img_folder, exist_ok=True)
    os.makedirs(train_label_folder, exist_ok=True)
    os.makedirs(val_img_folder, exist_ok=True)
    os.makedirs(val_label_folder, exist_ok=True)
 
    # Get the list of all image files
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
   
    # Shuffle the image files
    random.shuffle(image_files)
 
    # Split the image files into training and validation sets
    split_index = int(len(image_files) * train_ratio)
    train_files = image_files[:split_index]
    val_files = image_files[split_index:]
 
    # Process training files
    for image_file in train_files:
        image_name, image_ext = os.path.splitext(image_file)
        # Copy image to training folder
        shutil.copy(os.path.join(image_folder, image_file), os.path.join(train_img_folder, image_file))
        # Copy corresponding label file if it exists
        label_file = f"{image_name}.txt"
        if os.path.exists(os.path.join(label_folder, label_file)):
            shutil.copy(os.path.join(label_folder, label_file), os.path.join(train_label_folder, label_file))
 
    # Process validation files
    for image_file in val_files:
        image_name, image_ext = os.path.splitext(image_file)
        # Copy image to validation folder
        shutil.copy(os.path.join(image_folder, image_file), os.path.join(val_img_folder, image_file))
        # Copy corresponding label file if it exists
        label_file = f"{image_name}.txt"
        if os.path.exists(os.path.join(label_folder, label_file)):
            shutil.copy(os.path.join(label_folder, label_file), os.path.join(val_label_folder, label_file))
 
    print(f"Data split completed: {len(train_files)} training files, {len(val_files)} validation files.")
 
# Example usage
# split_data(
#     r"C:\tupn\tools\labels_segmentation_exe\crop_img",
#     r"C:\tupn\tools\labels_segmentation_exe\output_crop_img",
#     r"C:\tupn\phan_mem\l_fuser_ELL_ELLe\data_training\lay_seg\training\images",
#     r"C:\tupn\phan_mem\l_fuser_ELL_ELLe\data_training\lay_seg\training\labels",
#     r"C:\tupn\phan_mem\l_fuser_ELL_ELLe\data_training\lay_seg\val\images",
#     r"C:\tupn\phan_mem\l_fuser_ELL_ELLe\data_training\lay_seg\val\labels",
# )

# split_data(
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\mix_data_trai_phai",
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\out_mix_data_trai_phai",
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\data_set\training\images",
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\data_set\training\labels",
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\data_set\val\images",
#     r"D:\tupn\data_training\kiem_tra_trang_in\oject\data_set\val\labels",
# )
 
# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\giac_to",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\labels\giac_nhua_trang",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\dataset\giac_nhua_trang\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\dataset\giac_nhua_trang\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\dataset\giac_nhua_trang\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\dataset\giac_nhua_trang\val\labels",
# )
 
# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\giac_to",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\labels\giac_to_circle",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\val\labels",
# )

# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\giac_to",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\labels\giac_to_lay",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_to_lay\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_to_lay\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_to_lay\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_to_lay\val\labels",
# )
# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_2\giac_nho",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_2\labels\giac_nho_lay",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_lay\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_lay\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_lay\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_lay\val\labels",
# )

# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_2\giac_nho",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_2\labels\giac_nho_circle",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_circle\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_circle\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_circle\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\dataset\giac_nho_circle\val\labels",
# )

# split_data(
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\giac_nhua",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\data_lan_1\labels\giac_nhua_xam",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_nhua_xam\training\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_nhua_xam\training\labels",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_nhua_xam\val\images",
#     r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\labels\labelss\dataset\giac_nhua_xam\val\labels",
# )

# split_data(
#     r'D:\tupn\data_training\check fuser\data\mix_data\lay_seg\images_seg',
#     r"D:\tupn\data_training\check fuser\data\mix_data\lay_seg\labels_seg_lay",
#     r'D:\tupn\data_training\check fuser\data\mix_data\lay_seg\chia_80_20\training\images',
#     r'D:\tupn\data_training\check fuser\data\mix_data\lay_seg\chia_80_20\training\labels',
#     r'D:\tupn\data_training\check fuser\data\mix_data\lay_seg\chia_80_20\val\images',
#     r'D:\tupn\data_training\check fuser\data\mix_data\lay_seg\chia_80_20\val\labels',
# )
 

split_data(
    r'D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\images\giac_nhua',
    r"D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\labels\giac_nhua_xam",
    r'D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\chia_80_20\giac_nhua_xam\train\images',
    r'D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\chia_80_20\giac_nhua_xam\train\labels',
    r'D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\chia_80_20\giac_nhua_xam\val\images',
    r'D:\tupn\data_training\fuser_dll_a_Thai_Cuong_new\segment\gan_nhan_lan_3\chia_80_20\giac_nhua_xam\val\labels',
)
 
