#!/usr/bin/env python3
"""
测试修复后的API调用
"""

import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_fixed_api():
    """测试修复后的API调用"""
    print("🔍 测试修复后的API调用...")
    
    try:
        from config import ZAI_API_KEY, ZAI_API_URL, ZAI_MODEL, MAX_TOKENS
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    print(f"🔑 API密钥: {ZAI_API_KEY[:15]}...{ZAI_API_KEY[-15:]}")
    print(f"🌐 API端点: {ZAI_API_URL}")
    print(f"🤖 AI模型: {ZAI_MODEL}")
    print(f"🎯 最大tokens: {MAX_TOKENS}")
    
    # 测试不同推文内容
    test_tweets = [
        "今天天气真好，适合散步",
        "早上好，新的一天开始了",
        "刚吃完饭，好饱",
        "晚上吃什么呢？好纠结"
    ]
    
    headers = {
        "Authorization": f"Bearer {ZAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    for i, tweet_text in enumerate(test_tweets):
        print(f"\n📝 测试推文 {i+1}: {tweet_text}")
        
        prompt = f"""
请为这条推特写一个简短、幽默、没有emoji的回复：

推特内容：{tweet_text}

要求：
1. 简短（20字以内）
2. 幽默有趣
3. 不要使用emoji
4. 只生成一个回复选项
5. 要用中文回复

回复内容：
"""
        
        data = {
            "model": ZAI_MODEL,
            "messages": [
                {"role": "system", "content": "你是一个幽默风趣的推特用户，擅长写简短有趣的中文回复。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": MAX_TOKENS,
            "stream": False
        }
        
        try:
            response = requests.post(
                ZAI_API_URL,
                headers=headers,
                json=data,
                timeout=15,
                verify=False
            )
            
            print(f"📡 HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # 使用修复后的逻辑
                if 'choices' in result and len(result['choices']) > 0:
                    if 'message' in result['choices'][0]:
                        if 'content' in result['choices'][0]['message']:
                            reply = result['choices'][0]['message']['content'].strip()
                            
                            # 检查是否因token限制导致内容为空
                            finish_reason = result['choices'][0].get('finish_reason', '')
                            if finish_reason == 'length' and not reply:
                                print("⚠️  回复被截断（达到token限制）")
                                reply = None
                            
                            if reply:
                                print(f"✅ 成功生成回复: '{reply}'")
                                print(f"   长度: {len(reply)} 字符")
                            else:
                                print("❌ 生成空回复")
                        else:
                            print("❌ message中没有content")
                    else:
                        print("❌ choice中没有message")
                else:
                    print("❌ 响应中没有choices")
                    
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"错误响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 修复后的API调用测试")
    print("=" * 60)
    
    test_fixed_api()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)