@echo off
REM Twitter Auto Reply Bot 启动脚本 (Windows)

echo 🚀 启动 Twitter Auto Reply Bot (z.AI版)

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate

REM 安装依赖
echo 📥 安装依赖...
pip install -r requirements.txt

REM 检查配置文件
if not exist "config.py" (
    echo ❌ 配置文件不存在
    pause
    exit /b 1
)

echo ✅ 所有检查完成，正在启动...

REM 禁用 Node.js 弃用警告 (来自 Playwright)
set NODE_NO_WARNINGS=1

python bot.py

pause