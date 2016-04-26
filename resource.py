# _*_ coding: utf-8 _*_

import sys
import os

def resource_path(resource):
    """
    """
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, resource)
    else:
        dir_name = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(dir_name, resource)

img_poster = resource_path("poster.jpg")
ico_dgut = resource_path("dgut_video_yellow.ico")
img_wechat200 = resource_path("wechat200.jpg")