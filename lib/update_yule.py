import os
from lib import dbConnecter
import time

'''
CREATE TABLE yule (
           name VARCHAR(128),
           hot INT,
           path VARCHAR(256),
           intro VARCHAR(256),
           timef VARCHAR(64),
           creator VARCHAR(128)
        );
'''


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

def get_game_name(directory_path):
    file_list = []
    if not os.path.exists(directory_path):
        print(f"目录 {directory_path} 不存在！")
        return file_list

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # file_list.append(os.path.join(root, file))  # 完整路径
            file_list.append(file)

    return file_list


if __name__ == "__main__":
    folder_path_intro = '../static/md/yule'
    folder_path_source = '../templates/yule/source'
    intro_files = get_all_files_in_directory(folder_path_intro)
    source_files = get_all_files_in_directory(folder_path_source)
    gamename = get_game_name(folder_path_source)
    now = time.localtime()
    now_temp = time.strftime("%Y-%m-%d %H:%M", now)
    intro_files.sort()
    source_files.sort()
    gamename.sort()
    for i in range(0, len(intro_files)):
        if dbConnecter.read_data('yule', 'name', gamename[i]) == []:
            if gamename[i] != '.DS_Store':
                dbConnecter.insert_data('yule',
                                    '(name, hot, path, intro, timef, creator)',
                                        (gamename[i][:-5], 0, source_files[i][10:], intro_files[i], now_temp, 'ycy'))

