FROM python:3.10-slim

# 安装系统工具
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 拷贝源码
COPY . /app

# 安装依赖
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    git clone https://github.com/enarjord/passivbot.git && \
    pip install -r passivbot/requirements.txt

# 运行回测
CMD ["bash", "-c", "python main.py"]
