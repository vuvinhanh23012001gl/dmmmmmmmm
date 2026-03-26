import os, cv2
import path
from support_main.lib_main import edit_csv_tab, load_data_csv, remove
 

path_phan_mem = path.path_phan_mem


path_setting = path_phan_mem + "/setting/setting_check_folder.csv"



data_setting = load_data_csv.ds_data(path_setting)[0]
for i in range(0,len(data_setting)):
    if len(data_setting[i]) != 0:
        if data_setting[i][0] == "image_folder":
            image_folder = data_setting[i][1]
        if data_setting[i][0] == "txt_folder":
            txt_folder = data_setting[i][1]


list_img = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'))]
list_txt = [f for f in os.listdir(txt_folder) if f.lower().endswith('.txt')]

list_name_img = []
for i in range(0,len(list_img)):
    name_img = list_img[i].split(".")[0]
    list_name_img.append(name_img)
list_name_txt = []
for i in range(0,len(list_txt)):
    name_txt = list_txt[i].split(".")[0]
    list_name_txt.append(name_txt)

result = [item for item in list_name_txt if item not in list_name_img]
print(result)
