#!/bin/bash
# 一键部署脚本，建议在 Ubuntu 20.04+ 下运行

set -e

# 安装系统依赖
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# 克隆 Passivbot（用于扩展）
if [ ! -d passivbot ]; then
  git clone https://github.com/enarjord/passivbot.git
fi

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 可选：安装 passivbot 依赖（用于深入集成）
cd passivbot
pip install -r requirements.txt
cd ..

echo "安装完成。请设置环境变量 DEEPSEEK_API_KEY，然后运行 'python main.py' 进行回测。"
