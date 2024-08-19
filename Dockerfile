# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9.9-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 安装必要的工具
RUN apt-get update && apt-get install -y git && apt-get clean

# 克隆项目代码（如果不希望在/app下创建子目录，可以使用以下方法）
RUN git clone --depth 1 https://github.com/bassce/IPTV-M3U-Checker2-IPServer.git /app

# 安装所需的 Python 包
RUN pip install --no-cache-dir -r /app/requirements.txt

# 映射宿主机文件夹到容器
VOLUME /app/output
VOLUME /app/playlists

# 设定启动时的命令，先拉取最新代码再运行
CMD git -C /app pull origin main && python /app/main.py