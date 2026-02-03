@echo off
REM Twitter Bot 无限循环运行脚本 (Windows版本)
REM 持续运行 bot.py，每次运行完成后立即开始下一次

REM 禁用 Node.js 弃用警告 (来自 Playwright)
set NODE_NO_WARNINGS=1

echo 🚀 Twitter Bot 无限循环启动...
echo 📅 开始时间: %date% %time%
echo ⏱️ 按 Ctrl+C 停止循环
echo ==================================================

REM 循环计数器
set loop_count=0

:loop
set /a loop_count+=1
echo.
echo 🔄 第 %loop_count% 次循环开始 - %date% %time%
echo ==================================================

REM 运行 bot.py 并捕获输出
set TEMP_OUTPUT=%TEMP%\bot_output_%RANDOM%.txt
python bot.py > "%TEMP_OUTPUT%" 2>&1
type "%TEMP_OUTPUT%"

REM 保存退出码
set BOT_EXIT=%errorlevel%

REM 提取并显示 AI 生成的回复
echo.
echo 💬 ═══════════════════════════════════════════════
for /f "tokens=*" %%a in ('findstr /C:"生成回复:" "%TEMP_OUTPUT%"') do (
    echo 💬 %%a
)
echo 💬 ═══════════════════════════════════════════════
echo.

REM 清理临时文件
del "%TEMP_OUTPUT%" 2>nul

REM 检查退出码
if %BOT_EXIT% equ 0 (
    echo ✅ 第 %loop_count% 次循环成功完成
) else (
    echo ⚠️  第 %loop_count% 次循环失败，退出码: %BOT_EXIT%
)

REM 记录结束时间
echo ⏰ 结束时间: %date% %time%
echo ==================================================

REM 等待5秒后开始下一次循环
echo ⏳ 等待5秒后开始下一次循环...
timeout /t 5 /nobreak >nul
goto loop