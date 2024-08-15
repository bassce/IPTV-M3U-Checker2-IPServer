#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2024/04/16 17:20
# @Author  : Allen zh
# @Email   : allenzh77@gmail.com
# @File    : main.py

import time
import sys
import json
from iptv import Iptv
from zyrobot import DingtalkChatbot

# 在线预览文件域名 http / https
your_domain = False#'https://list.domain.com'

def load_config():
    '''获取运行配置信息'''
    try:
        with open(r"myconfig.json",encoding='utf-8') as json_file:
            parms = json.load(json_file)
            parms.setdefault('ctype', 0x01)
            parms.setdefault('checkfile_list', [])
            parms.setdefault('keywords', [])
            parms.setdefault('otype', 0x01 | 0x02 | 0x10)
            parms.setdefault('sendfile_list', [])
            parms.setdefault('newDb', False)
            parms.setdefault('webhook', '')
            parms.setdefault('secret', '')
            parms.setdefault('max_check_count', 2000)
            parms.setdefault('iptv_server_mode', 'no')
            
    except Exception as e:
        print(f"未发现myconfig.json配置文件，或配置文件格式有误: {e}")
        return {}
    return parms

if __name__ == '__main__':
    '''
    if (len(sys.argv) >= 1 ):
        for parm in sys.argv[1:]:
            checkfile_list.append (parm)
    '''
    
    parms=load_config()

    if not parms:
        sys.exit("配置加载失败，程序退出。")

    xiaoding = DingtalkChatbot(parms['webhook'], secret=parms['secret'])

    print('开始......')
    time1=time.time()

    iptv = Iptv(bReNew=parms['newDb'],logger=None)
        
    #设置最大解析节目源数量(可选,默认2000)
    iptv.MaxSourceCount=parms['max_check_count']

    # 获取节目列表
    myList=iptv.getPlaylist(ctype=parms['ctype'],checkfile_list=parms['checkfile_list'],keywords=parms['keywords'])
    # 运行检测
    iptv.runcheck(myList, bSavedb=(parms['ctype'] & 0x08 == 0), bTestSpeed=parms.get('testspeed', True))

    # 输出结果文件
    fnames=iptv.output(parms['otype'], iptv_server_mode=parms.get('iptv_server_mode', 'no'))   #diyp 0x01|m3u 0x02|标准txt 0x04 |测试 0x08

     # 发送结果文件
    iptv.sendit(fnames,parms['sendfile_list'])

    print('结束.....%s秒'%str(time.time()-time1))