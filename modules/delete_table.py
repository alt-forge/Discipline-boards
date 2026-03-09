import os

def delete_table(file_path_txt, file_path_png):
    if os.path.exists(file_path_txt):
        os.remove(file_path_txt)
    if os.path.exists(file_path_png):
        os.remove(file_path_png)