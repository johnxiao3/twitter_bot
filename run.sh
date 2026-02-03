#!/bin/bash
# Twitter Auto Reply Bot 启动脚本

echo "🚀 启动 Twitter Auto Reply Bot (z.AI版)"

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "❌ 配置文件不存在"
    exit 1
fi

echo "✅ 所有检查完成，正在启动..."

# 禁用 Node.js 弃用警告 (来自 Playwright)
export NODE_NO_WARNINGS=1

python bot.py