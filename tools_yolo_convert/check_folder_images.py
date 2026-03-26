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


list_img = os.listdir(image_folder)
list_txt = os.listdir(txt_folder)

list_name_img = []
for i in range(0,len(list_img)):
    name_img = list_img[i].split(".")[0]
    list_name_img.append(name_img)
list_name_txt = []
for i in range(0,len(list_txt)):
    name_txt = list_txt[i].split(".")[0]
    list_name_txt.append(name_txt)

unlisted_images = [img for img in list_name_img if img not in list_name_txt]
for i in range(0,len(unlisted_images)):
    print(f"Image {unlisted_images[i]} is not labeled yet.")
    # img = cv2.imread(os.path.join(image_folder, unlisted_images[i] + '.png'))
    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    