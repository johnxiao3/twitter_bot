#!/usr/bin/env python3
"""
测试z.AI不同模型的可用性
"""

import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_models():
    """测试不同模型的可用性"""
    print("🔍 测试不同模型的可用性...")
    
    try:
        from config import ZAI_API_KEY
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    # 测试的模型列表
    test_models = [
        "glm-4.5-air",  # 可能是免费版本
        "glm-4-air",    # 尝试其他可能免费的模型
        "chatglm3-gtb", # 尝试基础模型
        "glm-4",        # 原始模型
    ]
    
    headers = {
        "Authorization": f"Bearer {ZAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    results = {}
    
    for model_name in test_models:
        print(f"\n🤖 测试模型: {model_name}")
        
        # 简单的测试请求
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": "你好"}
            ],
            "temperature": 0.1,
            "max_tokens": 10,
            "stream": False
        }
        
        try:
            response = requests.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers=headers,
                json=data,
                timeout=10,
                verify=False
            )
            
            print(f"   HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"   ✅ 成功! 回复: '{reply.strip()}'")
                results[model_name] = "SUCCESS"
                break  # 找到可用的模型就停止
            else:
                error_info = response.json()
                error_msg = error_info.get('error', {}).get('message', '未知错误')
                print(f"   ❌ 失败: {error_msg}")
                
                if "余额不足" in error_msg or "资源包" in error_msg:
                    results[model_name] = "INSUFFICIENT_BALANCE"
                else:
                    results[model_name] = f"ERROR: {error_msg}"
                    
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            results[model_name] = f"EXCEPTION: {e}"
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 z.AI 模型可用性测试")
    print("=" * 60)
    
    results = test_models()
    
    print("\n" + "=" * 60)
    print("📊 测试结果:")
    print("=" * 60)
    
    for model, status in results.items():
        if status == "SUCCESS":
            print(f"✅ {model}: 可用")
        else:
            print(f"❌ {model}: {status}")
    
    if "SUCCESS" in results.values():
        print("\n🎉 找到可用模型！")
    else:
        print("\n⚠️  所有模型都不可用，可能的原因:")
        print("   1. 账户余额不足")
        print("   2. 需要充值才能使用")
        print("   3. API密钥权限不足")
    print("=" * 60)