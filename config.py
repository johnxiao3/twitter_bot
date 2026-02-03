# Twitter Bot 配置文件

# ============================================================
# 🔄 AI Provider 选择 (切换 AI 服务提供商)
# ============================================================
# 可选值: "zai" 或 "chatgpt"
AI_PROVIDER = "chatgpt"

# ============================================================
# 🤖 z.AI API配置 (智谱 GLM)
# ============================================================
ZAI_API_KEY = "API"  # 🔑 请替换为你的z.AI API密钥
ZAI_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZAI_MODEL = "GLM-4.7-Flash"  # 注意：需要账户余额充足才能使用

# ============================================================
# 🤖 ChatGPT API配置 (OpenAI)
# ============================================================
OPENAI_API_KEY = "API"  # 🔑 请替换为你的 OpenAI API密钥
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o"  # GPT-4o 模型

# ============================================================
# 浏览器CDP端口
CDP_PORT = 18792
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"

# 运行配置
MAX_RETRIES = 3
DELAY_BETWEEN_RUNS = 5

# 回复配置
MAX_REPLY_LENGTH = 200  # 最大回复长度（字符）
TEMPERATURE = 0.8  # AI生成温度（0-1，越高越随机）
MAX_TOKENS = 2500  # 最大生成token数，确保回复不会被截断

# API超时配置
API_TIMEOUT = 60  # API请求超时时间（秒）
API_CONNECT_TIMEOUT = 5  # API连接超时时间（秒）

# 日志配置
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "twitter_bot.log"