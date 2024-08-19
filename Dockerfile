# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9.9-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 安装必要的工具
RUN apt-get update && apt-get install -y git && apt-get clean

# 克隆指定的 GitHub 仓库到当前目录，而不是创建子目录
RUN git clone --depth 1 https://github.com/bassce/IPTV-M3U-Checker2-IPServer.git .

# 安装所需的 Python 包
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# 定义容器启动时的命令，重新拉取最新代码并运行
CMD git pull origin main && python /app/main.py