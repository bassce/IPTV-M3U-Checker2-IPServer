#!/bin/bash

# 如果宿主机挂载的目录为空，则复制默认的 sortlist.xlsx
if [ ! -f /app/playlists/sortlist.xlsx ]; then
    cp /app/defaults/sortlist.xlsx /app/playlists/sortlist.xlsx
fi

# 先执行 get_down_list.py 脚本
python get_down_list.py

# 待 get_down_list.py 脚本执行完毕后再执行 main.py 脚本
exec python main.py