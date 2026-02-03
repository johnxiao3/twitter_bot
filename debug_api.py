#!/usr/bin/env python3
"""
调试API响应结构
"""

import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def debug_api_response():
    """调试API响应结构"""
    print("🔍 调试API响应结构...")
    
    try:
        from config import ZAI_API_KEY, ZAI_API_URL, ZAI_MODEL
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    if ZAI_API_KEY == "zai-你的zai-api密钥-here":
        print("❌ API密钥未配置")
        return False
    
    print(f"🔑 API密钥: {ZAI_API_KEY[:15]}...{ZAI_API_KEY[-15:]}")
    print(f"🌐 API端点: {ZAI_API_URL}")
    print(f"🤖 AI模型: {ZAI_MODEL}")
    
    # 构造测试请求
    prompt = "请为这条推特写一个简短、幽默的回复：今天天气真好，适合散步"
    
    headers = {
        "Authorization": f"Bearer {ZAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": ZAI_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个幽默风趣的推特用户"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 50,
        "stream": False
    }
    
    try:
        print(f"🤖 发送调试请求...")
        print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
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
            print(f"\n📄 完整响应结构:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 详细分析响应结构
            print(f"\n🔍 响应结构分析:")
            print(f"包含的顶级键: {list(result.keys())}")
            
            if 'choices' in result:
                print(f"choices数组长度: {len(result['choices'])}")
                for i, choice in enumerate(result['choices']):
                    print(f"choices[{i}]: {list(choice.keys())}")
                    if 'message' in choice:
                        message = choice['message']
                        print(f"  message包含: {list(message.keys())}")
                        if 'content' in message:
                            content = message['content']
                            print(f"  content长度: {len(content)}")
                            print(f"  content内容: '{content}'")
                        else:
                            print(f"  ❌ message中没有content")
                    else:
                        print(f"  ❌ choice中没有message")
            else:
                print("❌ 响应中没有choices键")
                
            return True
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 z.AI API响应结构调试")
    print("=" * 60)
    
    success = debug_api_response()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 API调用成功，已详细分析响应结构")
    else:
        print("❌ API调用失败，无法分析响应结构")
    print("=" * 60)