#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2024/04/16 17:20
# @Author  : Allen zh
# @Email   : allenzh@outlook.com
# @File    : tools.py


import urllib.request
import urllib.parse
import urllib.error
import socket
import time
import os
from urllib.parse import urlparse

socket.setdefaulttimeout(5.0)

class Tools (object) :

    def __init__ (self) :
        pass

    def del_file(self,path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)

    def mkdir(self,path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return True

    def chkPlayable (self, url) :
        try:
            # 处理 IPv6 地址
            parsed_url = urlparse(url)
            if ':' in parsed_url.netloc and not parsed_url.netloc.startswith('['):
                parsed_url = parsed_url._replace(netloc=f"[{parsed_url.netloc}]")
            url = parsed_url.geturl()

            startTime = int(round(time.time() * 1000))
            code = urllib.request.urlopen(url).getcode()
            if code == 200 :
                endTime = int(round(time.time() * 1000))
                useTime = endTime - startTime
                return int(useTime)
            else:
                return 0
        except:
            return 0
