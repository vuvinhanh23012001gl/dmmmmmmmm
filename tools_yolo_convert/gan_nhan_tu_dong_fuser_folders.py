import os
from ultralytics import YOLO
import numpy as np
import path
import cv2
import support_main.edit_file_txt as edit_file_txt
import pybboxes as pbx
import shutil
from support_main.lib_main import remove, load_data_csv, edit_csv_tab

path_phan_mem = path.path_phan_mem
path_setting = path_phan_mem + "/setting/setting_gan_nhan_tu_dong.csv"

data_setting = load_data_csv.ds_data(path_setting)[0]
for i in range(0,len(data_setting)):
    if len(data_setting[i]) != 0:
        if data_setting[i][0] == "path_weights":
            path_weights = data_setting[i][1]
        if data_setting[i][0] == "path_folder_input":
            path_folder_input = data_setting[i][1]
        if data_setting[i][0] == "path_label_output":
            path_label_output = data_setting[i][1]
        if data_setting[i][0] == "path_img_output":
            path_img_output = data_setting[i][1]

model = YOLO(path_weights)
model.to("cuda") # Move the model to the GPU
def convert_yolo(w=int(640),h=int(480),data=[]):
    return pbx.convert_bbox(data, from_type="voc", to_type="yolo", image_size=(w,h))
     
def convert_box(w=640,h=480,data=[]):
    return pbx.convert_bbox(data, from_type="yolo", to_type="voc", image_size=(w,h))

def convert_bbox_to_yolo(data_input, w, h):
    list_output = []
    list_append = []
    for i in range(0,len(data_input)):
        data = [float(data_input[i][0]),float(data_input[i][1]),float(data_input[i][2]),float(data_input[i][3])]
        label = int(float(data_input[i][5]))
        dt = convert_yolo(w, h, data = data)
        list_append = [str(label),str(dt[0]),str(dt[1]),str(dt[2]),str(dt[3])]
        list_output.append(list_append)
    return list_output

def convert_data(path_img):
    det = []
    img = cv2.imread(path_img)
    result = model(img,verbose=False)
    xyxy = result[0].boxes.xyxy.tolist()
    labels = result[0].boxes.cls.tolist()
    conf = result[0].boxes.conf.tolist()
    for i in range(0,len(conf)):
        det.append([int(xyxy[i][0]),int(xyxy[i][1]),int(xyxy[i][2]),int(xyxy[i][3]),conf[i],int(float(labels[i]))])
    det = np.array(det)
    return det

def convert_data_yolo(path_folder):
    list_folder = os.listdir(path_folder)
    for folder_name in list_folder:
        path_folder_input = os.path.join(path_folder, folder_name)
        if not os.path.isdir(path_folder_input):
            continue
        list_img = os.listdir(path_folder_input)
        for j, img_name in enumerate(list_img):
            print(f"Processing folder '{folder_name}', image {j+1}/{len(list_img)}")
            path_img = os.path.join(path_folder_input, img_name)
            img = cv2.imread(path_img)
            if img is None:
                print(f"Warning: Could not read image {path_img}. Skipping.")
                continue
            h, w, _ = img.shape
            name_img = os.path.splitext(os.path.basename(path_img))[0]
            det = convert_data(path_img)
            if len(det) == 0:
                continue
            shutil.copy(path_img, path_img_output + "/" + name_img + ".png")
            edit_file_txt.creat_file_txt(path_file = path_label_output + "/" + name_img + ".txt",data = convert_bbox_to_yolo(det, w = w, h = h))
    




convert_data_yolo(path_folder_input)