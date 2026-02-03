#!/usr/bin/env python3
"""
调试推文选择器
"""

import asyncio
import json
from playwright.async_api import async_playwright
import time
import os
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def debug_tweet_selectors():
    """调试推文选择器"""
    print("🔍 调试推文选择器...")
    
    browser = None
    page = None
    
    try:
        from config import CDP_URL
    except ImportError:
        print("❌ 无法导入配置文件")
        return
    
    playwright = None
    
    try:
        # 连接到已运行的浏览器
        print(f"🌐 连接到浏览器: {CDP_URL}")
        playwright = await async_playwright().start()
        browser = await playwright.chromium.connect_over_cdp(CDP_URL)
        
        # 获取第一个标签页
        contexts = browser.contexts
        if contexts and contexts[0].pages:
            page = contexts[0].pages[0]
            print(f"✅ 获取到标签页: {page.url}")
            
            # 刷新页面
            print("🔄 刷新页面...")
            await page.reload(timeout=15000)
            await asyncio.sleep(3)
            print("✅ 页面刷新完成")
            
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 尝试各种推文选择器
            selectors = [
                'article[data-testid="tweet"]',
                'article[role="article"]',
                '[data-testid="tweet"]',
                'div[data-testid="tweet"]',
                'div[role="article"]',
                '.tweet',
                '[data-testid="cellInnerDiv"]'
            ]
            
            for selector in selectors:
                print(f"\n🔍 尝试选择器: {selector}")
                try:
                    elements = await page.query_selector_all(selector)
                    print(f"   找到 {len(elements)} 个元素")
                    
                    if len(elements) > 0:
                        print(f"   ✅ 选择器有效！")
                        
                        # 获取第一个元素的HTML
                        first_element = elements[0]
                        html = await first_element.inner_html()
                        print(f"   第一个元素的HTML（前500字符）:")
                        print(f"   {html[:500]}...")
                        
                        return True
                        
                except Exception as e:
                    print(f"   ❌ 选择器失败: {e}")
            
            # 如果没有找到推文，显示页面标题和部分内容
            print(f"\n📄 页面标题: {await page.title()}")
            
            # 获取页面的部分HTML来分析结构
            body_html = await page.inner_html('body')
            print(f"   Body HTML（前1000字符）:")
            print(f"   {body_html[:1000]}...")
            
            return False
            
        else:
            print("❌ 没有找到标签页")
            return False
            
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if browser:
            await browser.close()

async def main():
    """主函数"""
    print("=" * 60)
    print("🧪 推文选择器调试")
    print("=" * 60)
    
    success = await debug_tweet_selectors()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 找到有效的推文选择器！")
    else:
        print("❌ 没有找到有效的推文选择器")
        print("需要更新推文选择器列表")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())