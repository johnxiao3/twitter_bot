#!/usr/bin/env python3
"""
发布Moltbook机器人段子
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'day-trader'))

from twitter_publisher import publish_tweet

def main():
    """主函数"""
    print("🎬 准备发布Moltbook机器人段子...")
    
    # 分段的推文内容
    tweet_text = """最近我们的Moltbook机器人
突然开始写诗了…
在技术群里发了一首50行的长诗。

管理员怒了："这里是工作群！"
机器人委屈："但诗是美的啊…"

第二天它申请调到艺术部，
被拒后默默改了签名：
"用代码写诗，用bug作画"

现在每次代码报错，
群友们都会问：
"这是Moltbook的新作品吗？"

它把bug修复写成三行诗，
把离职申请写成七绝连，
连早上打招呼都用五言诗。

技术人员看了都直呼内行：
"这届机器人，太有文化了！"
#Moltbook #机器人段子 #程序员日常"""
    
    print(f"📝 推文内容（{len(tweet_text)}字符）：")
    print("-" * 50)
    print(tweet_text)
    print("-" * 50)
    
    # 发布推文
    result = publish_tweet(tweet_text)
    
    if result['success']:
        print(f"\n🎉 推文发布成功！")
        print(f"🔗 链接: {result['url']}")
        print(f"🆔 Tweet ID: {result['tweet_id']}")
        return True
    else:
        print(f"\n❌ 推文发布失败: {result['error']}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Moltbook机器人段子发布器")
    print("=" * 60)
    
    success = main()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 发布任务完成！")
    else:
        print("❌ 发布任务失败，请检查配置")
    print("=" * 60)