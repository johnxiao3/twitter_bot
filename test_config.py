#!/usr/bin/env python3
"""
配置测试脚本
用于验证所有配置是否正确
"""

import os
import sys

def test_config():
    """测试配置文件"""
    print("🔍 测试配置文件...")
    
    try:
        from config import ZAI_API_KEY, ZAI_API_URL, CDP_URL
        print("✅ 配置文件导入成功")
        
        # 检查API密钥
        if ZAI_API_KEY == "zai-你的zai-api密钥-here":
            print("⚠️  警告: API密钥未配置")
            print("   请在 config.py 中设置你的z.AI API密钥")
            return False
        else:
            print(f"✅ API密钥已配置: {ZAI_API_KEY[:10]}...")
        
        print(f"✅ API端点: {ZAI_API_URL}")
        print(f"✅ CDP端口: {CDP_URL}")
        return True
        
    except ImportError as e:
        print(f"❌ 配置文件导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("\n🔍 测试依赖包...")
    
    required_packages = [
        'playwright',
        'requests',
        'asyncio'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            all_installed = False
    
    return all_installed

def test_browser():
    """测试浏览器连接"""
    print("\n🔍 测试浏览器连接...")
    
    try:
        import requests
        from config import CDP_URL
        
        response = requests.get(f"{CDP_URL}/json", timeout=2)
        if response.status_code == 200:
            print(f"✅ 浏览器已连接: {CDP_URL}")
            return True
        else:
            print(f"⚠️  浏览器连接异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到浏览器: {e}")
        print("   请确保:")
        print("   1. Chrome浏览器正在运行")
        print("   2. Clawdbot扩展已连接")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 Twitter Auto Reply Bot - 配置测试")
    print("=" * 60)
    
    results = []
    
    # 测试配置
    results.append(("配置文件", test_config()))
    
    # 测试依赖
    results.append(("依赖包", test_dependencies()))
    
    # 测试浏览器
    results.append(("浏览器连接", test_browser()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果:")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 所有测试通过！可以运行 bot.py 了")
        print("运行命令: python bot.py")
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        print("修复方法:")
        print("1. 配置API密钥: 编辑 config.py")
        print("2. 安装依赖: pip install -r requirements.txt")
        print("3. 启动浏览器: 确保Chrome运行并连接Clawdbot")

if __name__ == "__main__":
    main()