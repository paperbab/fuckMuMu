import os
import shutil


def get_input_path(prompt):
    path = input(prompt)
    while not os.path.exists(path):
        print("路径不存在，请重新输入。")
        path = input(prompt)
    return path


def main():
    # 1. 输入 MuMu 用户目录
    mumu_user_dir = get_input_path("请输入 MuMu 模拟器 用户目录路径：")
    startup_image_dir = os.path.join(mumu_user_dir, "startupImage")
    if not os.path.exists(startup_image_dir):
        print("未找到 startupImage 文件夹。")
        return

    # 2. 输入照片目录
    photo_dir = get_input_path("请输入照片目录路径（包含 jpeg 图片）：")
    photos = [
        f for f in os.listdir(photo_dir)
        if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')
    ]
    if not photos:
        print("照片目录下没有 jpeg 图片。")
        return

    # 3. 遍历 startupImage 下的所有子文件夹
    subfolders = [
        os.path.join(startup_image_dir, d)
        for d in os.listdir(startup_image_dir)
        if os.path.isdir(os.path.join(startup_image_dir, d))
    ]
    rename_list = ["Normal.jpeg", "Pressed.jpeg", "Hover.jpeg"]
    for folder in subfolders:
        # 清空原有图片
        for file in os.listdir(folder):
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                os.remove(os.path.join(folder, file))
        # 复制三张图片并重命名
        for i, new_name in enumerate(rename_list):
            photo_file = photos[i % len(photos)]
            shutil.copy(os.path.join(photo_dir, photo_file),
                        os.path.join(folder, new_name))
            print(f"已覆盖 {folder} 下的图片为 {new_name}")

    print("全部覆盖完成。")


if __name__ == "__main__":
    main()
