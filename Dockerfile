# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9.9-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 添加 Docker 参数作为环境变量
ENV TESTSPEED=720
ENV CTYPE=1
ENV OTYPE=4
ENV IPTV_SERVER_MODE="no"
ENV CHECKFILE_LIST=""
ENV SENDFILE_LIST=""
ENV MAX_CHECK_COUNT=2000
ENV WEBHOOK=""
ENV SECRET=""
ENV YOUR_DOMAIN=""
ENV DELAY_THRESHOLD=2000
ENV KEYWORDS=""
ENV GITHUB_TOKEN=your_default_token
ENV SEARCH_QUERIES=直播源,iptv
ENV DAYS_AGO=20

# 设置工作目录
WORKDIR /app

# 将项目的所有文件复制到容器中
COPY main.py .
COPY iptv.py .
COPY zyrobot.py .
COPY db_import.py .
COPY myconfig.json .
COPY requirements.txt .
COPY get_down_list.py .
COPY playlists/sortlist.xlsx /app/defaults/sortlist.xlsx
COPY utils ./utils

# 安装所需的 Python 包
RUN pip install --no-cache-dir -r ./requirements.txt

# 创建播放列表目录并复制默认文件
RUN mkdir -p /app/playlists

# 复制启动脚本
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 设置宿主机与容器的共享目录
VOLUME /app/output
VOLUME /app/playlists

# 使用启动脚本作为入口点
ENTRYPOINT ["/app/entrypoint.sh"]