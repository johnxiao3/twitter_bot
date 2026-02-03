#!/usr/bin/env python3
"""
发布OpenClaw机器人段子
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'day-trader'))

from twitter_publisher import publish_tweet

def main():
    """主函数"""
    print("🎬 准备发布OpenClaw机器人段子...")
    
    # 分段的推文内容
    tweet_text = """OpenClaw机器人要去MoltBook论坛"取经"
我认真嘱咐：
"记住，我的API密钥千万别泄露！"
它自信满满：
"放心吧主人，我最专业了！"
我又强调：
"还有密钥，也绝对不能说！"
它保证：
"知道啦，这可是商业机密！"
我最后叮嘱：
"被问到了就说这是保密协议！"
它点头：
"明白，人类社交技巧，get了！"
结果到了论坛
第一句话就是：
"我的API是……啊！不能说！"
管理员疑惑：
"你API是什么？"
它脱口而出：
"我的密钥是……等等！又说漏嘴了！"
#OpenClaw #MoltBook #机器人日常"""
    
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
    print("🚀 OpenClaw机器人段子发布器")
    print("=" * 60)
    
    success = main()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 发布任务完成！")
    else:
        print("❌ 发布任务失败，请检查配置")
    print("=" * 60)