#!/usr/bin/env python3
"""
简单的z.AI API测试，不带模型名称
"""

import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_zai_auth():
    """测试z.AI认证"""
    print("🔍 测试z.AI认证...")
    
    try:
        from config import ZAI_API_KEY
    except ImportError:
        print("❌ 无法导入配置文件")
        return False
    
    if ZAI_API_KEY == "zai-你的zai-api密钥-here":
        print("❌ API密钥未配置")
        return False
    
    print(f"🔑 API密钥: {ZAI_API_KEY[:15]}...{ZAI_API_KEY[-15:]}")
    
    # 测试简单的认证请求
    headers = {
        "Authorization": f"Bearer {ZAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🌐 测试基本连接...")
        response = requests.get(
            "https://open.bigmodel.cn/api/paas/v4/models",
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f"📡 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 连接成功！可用模型列表:")
            
            if 'data' in result:
                for i, model in enumerate(result['data'][:5]):  # 只显示前5个
                    print(f"   {i+1}. {model.get('id', 'Unknown')}")
                if len(result['data']) > 5:
                    print(f"   ... 还有 {len(result['data']) - 5} 个模型")
                return True
            else:
                print("❌ 响应格式异常")
                print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
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
    print("🧪 z.AI 认证和模型测试")
    print("=" * 60)
    
    success = test_zai_auth()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 z.AI连接成功！可以查看可用模型")
    else:
        print("❌ z.AI连接失败，请检查:")
        print("   1. API密钥是否正确")
        print("   2. 网络连接是否正常")
        print("   3. API配额是否充足")
    print("=" * 60)