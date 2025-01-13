import os


def get_all_files_in_directory(directory_path):
    file_list = []
    if not os.path.exists(directory_path):
        print(f"目录 {directory_path} 不存在！")
        return file_list

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_list.append(os.path.join(root, file))  # 完整路径
            # 如果只想存文件名而不带路径，可以改为：file_list.append(file)

    return file_list


if __name__ == "__main__":
    folder_path_intro = 'templates/yule/intro'
    folder_path_source = 'templates/yule/source'
    intro_files = get_all_files_in_directory(folder_path_intro)
    source_files = get_all_files_in_directory(folder_path_source)
    for i in range(0, len(intro_files)):
        intro_files[i] = intro_files[i][10:]
        print(intro_files[i])
    for i in range(0, len(source_files)):
        source_files[i] = source_files[i][10:]
        print(source_files[i])
