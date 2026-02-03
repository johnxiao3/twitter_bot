#!/usr/bin/env python3
"""
z.AI API测试脚本
专门用于测试z.AI API调用
"""

import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_zai_api():
    """测试z.AI API调用"""
    print("🔍 测试z.AI API连接...")
    
    # 从配置文件读取API信息
    try:
        from config import ZAI_API_KEY, ZAI_API_URL, ZAI_MODEL, TEMPERATURE, MAX_TOKENS
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    # 检查API密钥
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
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    
    try:
        print(f"🤖 发送测试请求...")
        print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            ZAI_API_URL,
            headers=headers,
            json=data,
            timeout=10,
            verify=False  # 禁用SSL验证
        )
        
        print(f"📡 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API调用成功！")
            print(f"📄 完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 提取回复内容
            if 'choices' in result and len(result['choices']) > 0:
                if 'message' in result['choices'][0]:
                    if 'content' in result['choices'][0]['message']:
                        reply = result['choices'][0]['message']['content'].strip()
                        print(f"🎯 AI回复: {reply}")
                        return True
            
            print("❌ 响应结构异常")
            return False
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            
            # 尝试解析错误详情
            try:
                error_info = response.json()
                print(f"错误详情: {error_info}")
            except:
                pass
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 z.AI API连接测试")
    print("=" * 60)
    
    success = test_zai_api()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 z.AI API测试成功！可以运行机器人了")
    else:
        print("❌ z.AI API测试失败，请检查:")
        print("   1. API密钥是否正确")
        print("   2. 网络连接是否正常")
        print("   3. API配额是否充足")
    print("=" * 60)