#!/usr/bin/env python3
"""
测试推文提取
"""

import asyncio
import json
from playwright.async_api import async_playwright
import time
import os
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_tweet_extraction():
    """测试推文提取"""
    print("🔍 测试推文提取...")
    
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
            
            # 使用正确的选择器
            selector = 'article[data-testid="tweet"]'
            print(f"🔍 使用选择器: {selector}")
            
            tweet_elements = await page.query_selector_all(selector)
            print(f"找到 {len(tweet_elements)} 个推文")
            
            if len(tweet_elements) > 0:
                first_tweet = tweet_elements[0]
                print("✅ 获取到第一个推文")
                
                # 尝试不同的文本选择器
                text_selectors = [
                    '[data-testid="tweetText"]',
                    'div[lang]',
                    'div.css-901oao',
                    'div[role="article"] div[lang]',
                    'div.css-175oi2r.r-1udbk01 div[lang]'
                ]
                
                for text_selector in text_selectors:
                    try:
                        text_element = await first_tweet.query_selector(text_selector)
                        if text_element:
                            text = await text_element.inner_text()
                            if text.strip():
                                print(f"✅ 使用选择器 '{text_selector}' 成功获取文本:")
                                print(f"   文本长度: {len(text)}")
                                print(f"   文本内容: '{text[:100]}...'")
                                return text
                    except Exception as e:
                        print(f"❌ 选择器 '{text_selector}' 失败: {e}")
                
                print("❌ 没有找到有效的文本选择器")
                return None
            
            else:
                print("❌ 没有找到推文元素")
                return None
            
        else:
            print("❌ 没有找到标签页")
            return None
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

async def main():
    """主函数"""
    print("=" * 60)
    print("🧪 推文提取测试")
    print("=" * 60)
    
    text = await test_tweet_extraction()
    
    print("\n" + "=" * 60)
    if text:
        print("🎉 成功提取推文内容！")
        print(f"提取的文本: '{text[:200]}...'")
    else:
        print("❌ 无法提取推文内容")
        print("需要更新推文选择器")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())