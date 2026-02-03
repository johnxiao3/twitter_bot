# Twitter Bot 离线回复模板
# 当z.AI API不可用时的自动回复选项

# 幽默回复模板
HUMOR_REPLIES = [
    "说得有道理！",
    "太有趣了！",
    "同意！",
    "同感",
    "哈哈哈",
    "确实如此",
    "好观点",
    "赞同",
    "很有意思",
    "说到点子上了"
]

# 通用回复模板
GENERAL_REPLIES = [
    "感谢分享",
    "学到了",
    "受教了",
    "收藏了",
    "学习了",
    "明白了",
    "懂了",
    "了解",
    "知道了",
    "收到"
]

def get_offline_reply(tweet_text):
    """根据推文内容选择合适的离线回复"""
    import random
    
    # 简单的内容分析
    if any(word in tweet_text for word in ['天气', '今天', '明天', '下雨', '晴天']):
        return random.choice(['天气不错呢', '今天天气真好', '适合出门'])
    elif any(word in tweet_text for word in ['谢谢', '感谢', '感谢分享']):
        return random.choice(['不客气', '欢迎分享', '互相学习'])
    elif any(word in tweet_text for word in ['学习', '学习', '教程']):
        return random.choice(['学到了', '很有帮助', '感谢分享'])
    else:
        # 随机选择回复类型
        if random.random() > 0.5:
            return random.choice(HUMOR_REPLIES)
        else:
            return random.choice(GENERAL_REPLIES)