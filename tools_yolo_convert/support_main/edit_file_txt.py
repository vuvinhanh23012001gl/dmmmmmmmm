import pybboxes as pbx
from support_main.lib_main import remove
import os
import shutil
def edit_path(input):
    output = ""
    for i in input:
        if i == "\\":
            output = output + "/"
        else:
            output = output + i
    return output
path_phan_mem = edit_path(os.path.dirname(os.path.realpath(__file__)))

def read_txt_float(path_file = "1.txt"):
    list0 = []
    list1 = []
    text = ""
    with open(path_file) as f:
        contents = f.read()
        for i in range(0,len(contents)):
            if contents[i] == "\n":
                list1.append(float(text))
                list0.append(list1)
                list1 = []
                text = ""
            else:
                if contents[i] == " ":
                    list1.append(float(text))
                    text = ""
                else:
                    text = text + str(contents[i])
    return list0
                

def read_txt_str(path_file = "1.txt"):
    list0 = []
    list1 = []
    text = ""
    with open(path_file) as f:
        contents = f.read()
        for i in range(0,len(contents)):
            if contents[i] == "\n":
                list1.append((text))
                list0.append(list1)
                list1 = []
                text = ""
            else:
                if contents[i] == " ":
                    list1.append((text))
                    text = ""
                else:
                    text = text + str(contents[i])
    return list0
# print(read_txt_str())
def creat_file_txt(path_file = "D:/4_tools/yolov5_v1_0/test_convert_yolo.txt",data=[["new_data1","new_data2"]]):
    with open((path_file), 'w') as f:
        for i in range(0,len(data)):
            data[i][0] = data[i][0] + " "
            data[i][1] = data[i][1] + " "
            data[i][2] = data[i][2] + " "
            data[i][3] = data[i][3] + " "
            data[i][4] = data[i][4] + "\n"
            for i2 in range(0,len(data[i])):
                f.writelines(data[i][i2])
        f.close()

# creat_file_txt()



# import os
# path_folder = "./label_img_chua_gan_nhan"
# list_data = os.listdir(path_folder)
# for ii in range(0,len(list_data)):
#     a = list(list_data[ii])
#     del a[-1]
#     del a[-1]
#     del a[-1]
#     name = ""
#     for i in range(0,len(a)):
#         name = name + a[i]
#     os.rename(path_folder + "/" +list_data[ii], "./test1/"+name + ".txt")




