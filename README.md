# Twitter Auto Reply Bot (z.AI版)

基于Python的Twitter自动回复机器人，使用z.AI模型生成幽默回复。

## 🚀 功能特点

- ✅ 自动获取Twitter第一条推文
- ✅ 使用z.AI模型生成幽默中文回复
- ✅ 自动发送回复到推文
- ✅ 完整的错误处理和日志记录
- ✅ 支持自定义配置

## 📋 系统要求

- Python 3.8+
- Chrome浏览器（已启动，连接Clawdbot扩展）
- z.AI API密钥

## 🔧 安装和配置

### 1. 创建项目目录
```bash
mkdir -p ~/twitter_bot
cd ~/twitter_bot
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. 配置API密钥
编辑 `config.py` 文件，替换API密钥：
```python
ZAI_API_KEY = "zai-你的真实API密钥-here"
```

### 4. 高级配置（可选）
可以调整以下配置来优化性能：

```python
# API超时配置（秒）
API_TIMEOUT = 15          # API请求超时时间
API_CONNECT_TIMEOUT = 5   # API连接超时时间
MAX_TOKENS = 1000         # 最大生成token数
TEMPERATURE = 0.8         # AI生成温度（0-1，越高越随机）
```

### 5. 运行脚本
```bash
python bot.py
```

## 📁 项目结构

```
twitter_bot/
├── bot.py              # 主程序文件
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── README.md          # 说明文档
├── twitter_bot.log    # 日志文件
└── data/             # 数据目录（可选）
    └── tweets.json   # 推文数据记录
```

## 🎯 使用说明

### 运行模式

- **调试模式**（默认）：运行1次
- **循环模式**：可以修改代码中的 `count` 参数

### 执行流程

1. 🔗 连接浏览器 (CDP端口18800)
2. 📄 获取第一个标签页
3. 🌐 导航到Twitter主页
4. 📝 获取第一条推文
5. 🤖 调用z.AI生成回复
6. ✉️ 自动发送回复
7. ✅ 显示执行结果

## ⚙️ 配置选项

### z.AI配置
- `ZAI_API_KEY`: 你的z.AI API密钥
- `ZAI_API_URL`: API端点（通常不需要修改）
- `ZAI_MODEL`: 使用的模型（默认: glm-4）

### 浏览器配置
- `CDP_PORT`: CDP调试端口（默认: 18800）

### 运行配置
- `MAX_RETRIES`: 最大重试次数
- `DELAY_BETWEEN_RUNS`: 每次运行间隔（秒）

### 回复配置
- `MAX_REPLY_LENGTH`: 最大回复长度（字符）
- `TEMPERATURE`: AI生成温度（0-1）
- `MAX_TOKENS`: 最大生成token数

## 🔍 故障排除

### 常见问题

1. **无法连接浏览器**
   - 确保Chrome浏览器正在运行
   - 检查Clawdbot扩展是否已连接
   - 确认CDP端口正确（18800）

2. **API调用失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 检查API配额是否充足

3. **无法找到推文元素**
   - 确保已登录Twitter
   - 页面是否完全加载
   - 检查推文元素选择器是否正确

### 日志查看
```bash
tail -f twitter_bot.log
```

## 🤝 自定义和扩展

### 修改回复策略
在 `bot.py` 的 `generate_reply_with_zai` 方法中修改prompt。

### 添加新的AI模型
在配置文件中添加新的模型配置，并在相应方法中添加调用逻辑。

### 批量运行
修改 `run` 方法的 `count` 参数或添加循环逻辑。

### 无限循环运行
使用提供的循环脚本持续运行机器人：

```bash
# Linux/Mac
./run_loop.sh

# Windows
run_loop.bat
```

循环脚本特性：
- ✅ 自动重启失败的运行
- ✅ 详细的运行日志
- ✅ 运行统计信息
- ✅ 可配置的循环间隔
- ✅ 按 Ctrl+C 停止

## 📊 性能优化

## 📊 性能优化

- 减少重试次数以提高速度
- 增加延迟以避免频率限制
- 优化元素选择器以提高稳定性

## 🔒 注意事项

- 请妥善保管API密钥
- 遵守Twitter的使用条款
- 注意不要频繁发送回复以避免被封禁

## 📞 支持

如有问题请检查日志文件或联系开发者。