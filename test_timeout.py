#!/usr/bin/env python3
"""
测试超时配置
"""

import sys
import time

def test_timeout_config():
    """测试超时配置是否正确导入"""
    print("🔍 测试超时配置...")
    
    try:
        from config import API_TIMEOUT, API_CONNECT_TIMEOUT
        print(f"✅ API_TIMEOUT: {API_TIMEOUT} 秒")
        print(f"✅ API_CONNECT_TIMEOUT: {API_CONNECT_TIMEOUT} 秒")
        
        # 验证配置值是否合理
        if API_TIMEOUT <= 0:
            print("❌ API_TIMEOUT 必须大于0")
            return False
        if API_CONNECT_TIMEOUT <= 0:
            print("❌ API_CONNECT_TIMEOUT 必须大于0")
            return False
        if API_CONNECT_TIMEOUT >= API_TIMEOUT:
            print("❌ API_CONNECT_TIMEOUT 应该小于 API_TIMEOUT")
            return False
            
        print("✅ 超时配置验证通过")
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入超时配置: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 超时配置测试")
    print("=" * 60)
    
    success = test_timeout_config()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 超时配置测试通过！")
    else:
        print("❌ 超时配置测试失败")
        print("请检查 config.py 文件中的超时配置")
    print("=" * 60)