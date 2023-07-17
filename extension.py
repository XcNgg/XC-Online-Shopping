"""
extension.py
    项目扩展文件
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_mail import Mail

mail = Mail()



import os
import shutil
def move_file(imgfile, dstpath):
    """
    :param imgfile: 需要复制、移动的文件
    :param dstpath: 目的地址
    :return:
    """
    if not os.path.isfile(imgfile):
        print(f"{imgfile} not exist!" )
    else:
        fpath, fname = os.path.split(imgfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(imgfile, dstpath + fname)  # 复制文件
        print(f"MOVE {imgfile} --> {dstpath + fname}")