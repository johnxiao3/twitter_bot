#!/bin/bash

# Twitter Bot 智能无限循环运行脚本
# 持续运行 bot.py，提供详细的运行状态和日志记录

# 禁用 Node.js 弃用警告 (来自 Playwright)
export NODE_NO_WARNINGS=1

# 配置参数
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/bot_loop_$(date +%Y%m%d_%H%M%S).log"
SLEEP_TIME=0  # 次�运行之间的等待时间（秒）
MAX_LOOPS=0  # 最大循环次数（0表示无限）

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "🚀 Twitter Bot 智能无限循环启动..."
echo "📅 启动时间: $(date)"
echo "📁 日志文件: $LOG_FILE"
echo "⏱️  循环间隔: $SLEEP_TIME 秒"
echo "🔢 最大循环: $MAX_LOOPS 次 (0=无限)"
echo "📝 按 Ctrl+C 停止循环"
echo "=================================================="

# 循环计数器
loop_count=0
start_time=$(date +%s)
start_time_str=$(date)

# 记录函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 主循环
while [ $MAX_LOOPS -eq 0 ] || [ $loop_count -lt $MAX_LOOPS ]; do
    loop_count=$((loop_count + 1))
    
    echo ""
    log "🔄 第 $loop_count 次循环开始"
    log "=================================================="
    
    # 记录开始时间
    loop_start=$(date +%s)
    loop_start_str=$(date)
    
    # 运行 bot.py 并记录输出到临时文件
    log "🤖 运行 bot.py..."
    TEMP_OUTPUT=$(mktemp)
    python3 bot.py 2>&1 | tee -a "$LOG_FILE" "$TEMP_OUTPUT"
    
    # 检查退出码
    exit_code=${PIPESTATUS[0]}
    loop_end=$(date +%s)
    loop_duration=$((loop_end - loop_start))
    
    # 提取并显示 AI 生成的回复
    ai_response=$(grep -E "(z\.AI|ChatGPT)生成回复:" "$TEMP_OUTPUT" | tail -1 | sed 's/.*生成回复: //')
    tweet_content=$(grep "内容:" "$TEMP_OUTPUT" | head -1 | sed 's/.*内容: //')
    
    if [ -n "$ai_response" ]; then
        echo ""
        log "💬 ═══════════════════════════════════════════════"
        log "💬 AI 回复: $ai_response"
        log "💬 ═══════════════════════════════════════════════"
        echo ""
    fi
    
    # 清理临时文件
    rm -f "$TEMP_OUTPUT"
    
    if [ $exit_code -eq 0 ]; then
        log "✅ 第 $loop_count 次循环成功完成 (耗时: ${loop_duration}秒)"
    else
        log "⚠️  第 $loop_count 次循环失败，退出码: $exit_code (耗时: ${loop_duration}秒)"
    fi
    
    # 计算运行统计
    total_time=$((loop_end - start_time))
    total_time_str=$(date -u -r $total_time +%H:%M:%S)
    
    log "📊 运行统计:"
    log "   当前循环: $loop_count / $MAX_LOOPS"
    log "   总运行时间: $total_time_str"
    log "   平均每次: $((total_time / loop_count))秒"
    log "   成功率: $(( (exit_code == 0) ? 100 : 0 ))%"
    
    # 检查是否需要结束
    if [ $MAX_LOOPS -ne 0 ] && [ $loop_count -ge $MAX_LOOPS ]; then
        log "🎉 达到最大循环次数 ($MAX_LOOPS)，停止运行"
        break
    fi
    
    # 等待后开始下一次循环
    log "⏳ 等待 $SLEEP_TIME 秒后开始下一次循环..."
    sleep $SLEEP_TIME
done

# 记录总结
end_time=$(date +%s)
end_time_str=$(date)
total_runtime=$((end_time - start_time))
total_runtime_str=$(date -u -r $total_runtime +%H:%M:%S)

echo ""
echo "=================================================="
echo "🎯 循环运行完成"
echo "📅 开始时间: $start_time_str"
echo "📅 结束时间: $end_time_str"
echo "⏱️  总运行时间: $total_runtime_str"
echo "🔄 总循环次数: $loop_count"
echo "📁 日志文件: $LOG_FILE"
echo "=================================================="