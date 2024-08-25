import os
import time
import sys
from iptv import Iptv
from zyrobot import DingtalkChatbot

def get_env_or_default(env_var, default_value):
    return os.getenv(env_var, default_value)

if __name__ == '__main__':
    # 从环境变量中获取参数
    testspeed = int(get_env_or_default('TESTSPEED', 720))
    ctype = int(get_env_or_default('CTYPE', 1))
    otype = int(get_env_or_default('OTYPE', 4))
    iptv_server_mode = get_env_or_default('IPTV_SERVER_MODE', 'no').lower()
    checkfile_list = get_env_or_default('CHECKFILE_LIST', '').split(',')
    sendfile_list = get_env_or_default('SENDFILE_LIST', '').split(',')
    max_check_count = int(get_env_or_default('MAX_CHECK_COUNT', 2000))
    webhook = get_env_or_default('WEBHOOK', '')
    secret = get_env_or_default('SECRET', '')
    your_domain = get_env_or_default('YOUR_DOMAIN', '')
    delay_threshold = int(get_env_or_default('DELAY_THRESHOLD', 2000))
    keywords = get_env_or_default('KEYWORDS', '').split(',')

    # 初始化钉钉机器人，如果提供了 webhook 和 secret
    xiaoding = None
    if webhook and secret:
        xiaoding = DingtalkChatbot(webhook, secret=secret)

    print('开始......')
    time1 = time.time()

    iptv = Iptv(bReNew=False, logger=None)
        
    # 设置最大检查数量和延迟阈值
    iptv.MaxSourceCount = max_check_count
    iptv.delay_threshold = delay_threshold

    # 获取节目列表
    myList = iptv.getPlaylist(ctype=ctype, checkfile_list=checkfile_list)

    # 运行检测，基于分辨率（testspeed）进行筛选
    iptv.runcheck(myList, bSavedb=(ctype & 0x08 == 0), bTestSpeed=testspeed)

    # 输出结果文件
    fnames = iptv.output(otype, iptv_server_mode=iptv_server_mode)

    # 发送结果文件
    iptv.sendit(fnames, sendfile_list)

    print(f'结束.....{time.time() - time1}秒')
