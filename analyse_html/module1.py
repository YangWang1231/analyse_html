import os
import shutil
import zipfile
from os.path import join, getsize

def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:     
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        print('This is not zip')

src_file = 'ultraedit10.zip'
index = src_file.rfind('\\')
path_list = [os.curdir,'extrac_floder']
if index is not -1:
    sub_floder = src_file[index:]
    path_list.append(sub_floder)
dst_path = '\\'.join(path_list)
unzip_file(src_file, dst_path )