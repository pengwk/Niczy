# _*_ coding:utf-8 _*_

from __future__ import division

import os
import subprocess
import sys



def open_in_folder(path):
    u"""path 文件"""

    file_dir = os.path.dirname(path)
    path = path.encode(sys.getfilesystemencoding())
    if sys.platform.startswith("win32"):
        subprocess.Popen(["explorer", "/select,", path])

    elif sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", "--", path])

    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", "--", path])
    return None

def readable_size(byte):
    u"""
    :params :byte type int 
    """

    B = 1024
    KB = 1048576
    MB = 1073741824
    GB = 1099511627776L

    if byte <= B:
        size_str = "{}B".format(byte)

    elif byte <= KB: 
        size = round(byte/B)
        size_str = "{}KB".format(size)

    elif byte <= MB: 
        size = round(byte/KB)
        size_str = "{}MB".format(size)

    elif byte <= GB:
        size = round(byte/MB)
        size_str = "{}GB".format(size)

    return size_str

def file_dir(path):
    u"""获取文件所在的文件夹
    
    """

    import os
    # path = os.path.normpath(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    print dirname
    parts = os.path.split(dirname)
    print parts
    if parts[-1]:
        parent = parts[-1]

    else:
        parent = parts[-2]
    return parent

if __name__ == "__main__":
    open_in_folder(ur"E:\temp\Niczy\06美女的烦恼你们根本就不懂之第二弹 _超清.mp4")