import os
import shutil
import zipfile
import rarfile
from os.path import join, getsize, splitext

file_extensions = ['.rar', '.zip']

def unzip_file(zip_src, dst_dir):
    '''
    zip_src: zip file path
    dst_dir: extract to this floder
    etc:
    zip_src = 'somefloder/hello.zip'
    dst_dir = './extract_zip'
    after call unzip_function, will extract hello.zip to './extract_zip/hello/'
    '''
    unrar_file_path = r'C:\Program Files\WinRAR\Unrar'

    filename, ext = splitext(zip_src)
    if ext not in file_extensions:
        return None

    index = filename.rfind('\\')
    if(index != -1):
        sub_floder = filename[index+1:]
    else:
        sub_floder = filename
    dst_dir = '\\'.join((dst_dir, sub_floder))

    if zipfile.is_zipfile(zip_src):
        with zipfile.ZipFile(zip_src,"r") as fz:
            fz.extractall(dst_dir)
    elif rarfile.is_rarfile(zip_src):
        rarfile.UNRAR_TOOL = unrar_file_path 

        with rarfile.RarFile(zip_src,'r') as fz:
            fz.extractall(dst_dir)



if __name__ == '__main__':
    src_file = r'C:\Download\ultraedit10.rar'
    path_list = [os.curdir,'extrac_floder']
    dst_path = '\\'.join(path_list)
    unzip_file(src_file, dst_path )