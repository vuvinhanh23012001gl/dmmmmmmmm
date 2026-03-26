import cv2
import os
import time
from datetime import datetime
from support_main.lib_main import load_data_csv, edit_csv_tab
import os
import path

path_phan_mem = path.path_phan_mem


path_setting = path_phan_mem + "/setting/setting_convert_video_to_img.csv"



data_setting = load_data_csv.ds_data(path_setting)[0]
for i in range(0,len(data_setting)):
    if len(data_setting[i]) != 0:
        if data_setting[i][0] == "dinh_dang":
            dinh_dang = data_setting[i][1]
        if data_setting[i][0] == "path_video":
            path_video = data_setting[i][1]
        if data_setting[i][0] == "folder_output":
            folder_output = data_setting[i][1]
        if data_setting[i][0] == "time":
            time = int(float(data_setting[i][1]))



def time_now():
    dt = datetime.now()
    time_0 = str(dt.year) +'/'+ str(dt.month) + '/' + str(dt.day) + ' ' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
    time_1 = str(dt.year) +'_'+ str(dt.month) + '_' + str(dt.day) + '_' + str(dt.hour) + '_' + str(dt.minute) + '_' + str(dt.second)
    return time_0,time_1

def read_settings(file_path):
    settings = {}
    with open(file_path, 'r') as file:
        for line in file:
            print(line)
            name, value = line.strip().split(' ')
            settings[str(name)] = str(value)
            print(settings[str(name)])
    return settings

def video_to_images(video_path, output_folder, time_detect = 0.5, dinh_dang = "png"):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Mở video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    t = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if time.time() - t > time_detect:
            t = time.time()
            time_0,time_1 = time_now()
            cv2.imwrite(output_folder + "/img_" + time_1 + "." +dinh_dang, frame)

    cap.release()
    print(f"Đã lưu {frame_count} ảnh vào thư mục {output_folder}")


if os.path.exists(path_video) == True:
    video_to_images(path_video, folder_output, float(data_setting["time"]), data_setting["dinh_dang"])