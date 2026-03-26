import os

def convert_yolo_labels(input_folder, output_folder, new_class_id=0):
    # Tạo folder đầu ra nếu chưa có
    os.makedirs(output_folder, exist_ok=True)

    # Duyệt tất cả file txt trong folder đầu vào
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    parts[0] = str(new_class_id)  # đổi class id
                new_lines.append(" ".join(parts) + "\n")

            with open(output_path, "w") as f:
                f.writelines(new_lines)

    print("✅ Hoàn thành chuyển đổi class ID!")


convert_yolo_labels(r"D:\tupn\data_training\yolo_input\segment\img_200\labels", r"D:\tupn\data_training\yolo_input\segment\img_200\label")
