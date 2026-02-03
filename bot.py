#!/usr/bin/env python3
"""
Twitter Auto Reply Bot - 支持 z.AI 和 ChatGPT
完全配置版本，支持多种 AI API调用
可在 config.py 中切换 AI 提供商
"""

import asyncio
import json
import requests
from playwright.async_api import async_playwright
import time
import os
import base64
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 导入配置
try:
    from config import *
    from offline_replies import get_offline_reply
except ImportError:
    print("❌ 无法导入配置文件，请确保 config.py 存在")
    exit(1)

def is_english_text(text):
    """检测文本是否主要是英文"""
    if not text:
        return False
    
    # 移除空格、数字、标点符号，只保留字母
    import re
    letters_only = re.sub(r'[^a-zA-Z\u4e00-\u9fff]', '', text)
    
    if not letters_only:
        return False
    
    # 计算英文字母的比例
    english_chars = sum(1 for c in letters_only if c.isascii())
    total_chars = len(letters_only)
    
    # 如果超过 70% 是英文字母，则认为是英文
    english_ratio = english_chars / total_chars
    return english_ratio > 0.7


class TwitterAutoReply:
    def __init__(self):
        # AI Provider 选择
        self.ai_provider = AI_PROVIDER.lower()
        
        # z.AI API配置
        self.zai_api_url = ZAI_API_URL
        self.zai_api_key = ZAI_API_KEY
        self.zai_model = ZAI_MODEL
        
        # ChatGPT/OpenAI API配置
        self.openai_api_url = OPENAI_API_URL
        self.openai_api_key = OPENAI_API_KEY
        self.openai_model = OPENAI_MODEL
        
        # CDP端口配置
        self.cdp_url = CDP_URL
        
        # 其他配置
        self.max_retries = MAX_RETRIES
        self.delay_between_runs = DELAY_BETWEEN_RUNS
        
        self.browser = None
        self.page = None
        
        # 显示当前配置
        provider_name = "ChatGPT (OpenAI)" if self.ai_provider == "chatgpt" else "z.AI (智谱)"
        current_model = self.openai_model if self.ai_provider == "chatgpt" else self.zai_model
        current_key = self.openai_api_key if self.ai_provider == "chatgpt" else self.zai_api_key
        key_configured = current_key and current_key not in ["zai-你的zai-api密钥-here", "sk-your-openai-api-key-here"]
        
        print(f"🔧 Twitter Auto Reply Bot 已初始化")
        print(f"🌐 CDP端口: {self.cdp_url}")
        print(f"🎯 AI提供商: {provider_name}")
        print(f"🤖 AI模型: {current_model}")
        print(f"🔑 API密钥: {'已配置' if key_configured else '❌ 未配置'}")
    
    async def connect_browser(self):
        """连接到浏览器"""
        print("🔍 步骤1: 连接浏览器...")
        for attempt in range(3):
            try:
                playwright = await async_playwright().start()
                # 连接到正确的CDP端口
                self.browser = await playwright.chromium.connect_over_cdp(self.cdp_url)
                print(f"✅ 成功连接到浏览器: {self.cdp_url}")
                return True
            except Exception as e:
                print(f"⚠️  尝试 {attempt + 1}/3 失败: {e}")
                if attempt < 2:
                    await asyncio.sleep(2)
        print("❌ 无法连接到浏览器，请检查:")
        print("   1. Chrome浏览器是否正在运行")
        print("   2. Clawdbot扩展是否已连接")
        return False
    
    async def get_first_tab(self):
        """获取第一个标签页"""
        print("🔍 步骤2: 获取第一个标签页...")
        try:
            contexts = self.browser.contexts
            if contexts and contexts[0].pages:
                self.page = contexts[0].pages[0]
                print(f"✅ 成功获取标签页: {self.page.url}")
                
                # 刷新页面确保内容是最新的
                print("🔄 刷新页面...")
                try:
                    await self.page.reload(timeout=15000)  # 15秒超时
                    await asyncio.sleep(3)  # 等待页面重新加载完成
                    print("✅ 页面刷新完成")
                except Exception as e:
                    print(f"⚠️  刷新失败，但继续执行: {e}")
                    # 即使刷新失败也继续，可能页面已经是最新状态
                
                return True
            print("❌ 没有找到标签页")
            return False
        except Exception as e:
            print(f"❌ 获取标签页失败: {e}")
            return False
    
    async def navigate_to_twitter(self):
        """导航到Twitter主页"""
        print("🔍 步骤3: 检查并导航到Twitter...")
        try:
            if "x.com" not in self.page.url:
                print("📍 导航到Twitter主页...")
                await self.page.goto("https://x.com/home", wait_until="networkidle")
                await asyncio.sleep(3)
            print("✅ 已在Twitter页面")
            return True
        except Exception as e:
            print(f"❌ 导航失败: {e}")
            return False
    
    async def get_first_tweet(self):
        """获取第一条推文"""
        print("🔍 步骤4: 获取第一条推文...")
        try:
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 尝试多个选择器
            selectors = [
                'article[data-testid="tweet"]',
                'article[role="article"]',
            ]
            
            for selector in selectors:
                try:
                    tweet_elements = await self.page.query_selector_all(selector)
                    if tweet_elements:
                        first_tweet = tweet_elements[0]
                        
                        # 获取推文文本
                        text_element = await first_tweet.query_selector('[data-testid="tweetText"]')
                        if not text_element:
                            text_element = await first_tweet.query_selector('div[lang]')
                        
                        if text_element:
                            text = await text_element.inner_text()
                            
                            # 获取作者信息
                            author_element = await first_tweet.query_selector('div[data-testid="User-Name"]')
                            author = ""
                            if author_element:
                                author = await author_element.inner_text()
                            
                            print(f"✅ 获取到推文:")
                            print(f"   作者: {author}")
                            print(f"   内容: {text[:100]}...")
                            
                            return {
                                "text": text, 
                                "author": author,
                                "timestamp": time.time()
                            }
                except Exception as e:
                    continue
            
            print("❌ 没有找到推文元素")
            return None
            
        except Exception as e:
            print(f"❌ 获取推文失败: {e}")
            return None
    
    def generate_reply_with_zai(self, tweet_text):
        """使用z.AI模型生成回复"""
        print("🔍 步骤5: 调用z.AI生成回复...")
        
        # 检查API密钥
        if not self.zai_api_key or self.zai_api_key == "zai-你的zai-api密钥-here":
            print("⚠️  z.AI API密钥未配置")
            return None
        
        print(f"🔑 API密钥: {self.zai_api_key[:15]}...{self.zai_api_key[-15:]}")
        print(f"🌐 API端点: {self.zai_api_url}")
        print(f"🤖 AI模型: {self.zai_model}")
        
        try:
            # 检测推文语言
            is_english = is_english_text(tweet_text)
            language = "English" if is_english else "Chinese"
            language_instruction = "5. Reply in English" if is_english else "5. 要用中文回复"
            system_prompt = "You are a witty Twitter user who writes short, funny replies in English." if is_english else "你是一个幽默风趣的推特用户，擅长写简短有趣的中文回复。"
            
            print(f"🌍 检测到语言: {language}")
            
            # 构造z.AI的prompt
            prompt = f"""
请为这条推特写一个简短、幽默、没有emoji的回复：

推特内容：{tweet_text}

要求：
1. 简短（20字以内）
2. 幽默有趣
3. 不要使用emoji
4. 只生成一个回复选项
{language_instruction}

回复内容：
"""
            
            # z.AI API请求
            headers = {
                "Authorization": f"Bearer {self.zai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.zai_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
                "stream": False
            }
            
            print(f"🤖 正在调用z.AI模型...")
            print(f"请求参数: model={self.zai_model}, temperature={TEMPERATURE}, max_tokens={MAX_TOKENS}")
            
            response = requests.post(
                self.zai_api_url,
                headers=headers,
                json=data,
                timeout=(API_CONNECT_TIMEOUT, API_TIMEOUT),
                verify=False  # 禁用SSL验证
            )
            
            print(f"📡 HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📄 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # 检查响应结构
                if 'choices' in result and len(result['choices']) > 0:
                    if 'message' in result['choices'][0]:
                        if 'content' in result['choices'][0]['message']:
                            reply = result['choices'][0]['message']['content'].strip()
                            
                            # 检查是否因token限制导致内容为空
                            finish_reason = result['choices'][0].get('finish_reason', '')
                            if finish_reason == 'length' and not reply:
                                print("⚠️  回复被截断（达到token限制），尝试减少token数量")
                                return None
                            
                            if reply:
                                print(f"✅ z.AI生成回复: {reply}")
                                return reply
                            else:
                                print("⚠️  AI生成了空回复")
                                return None
                
                print("❌ 响应结构异常")
                return None
            else:
                print(f"❌ z.AI API调用失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                
                # 尝试解析错误详情
                try:
                    error_info = response.json()
                    if 'error' in error_info:
                        error_msg = error_info['error'].get('message', '未知错误')
                        print(f"错误详情: {error_msg}")
                        
                        # 特殊处理余额不足的情况
                        if "余额不足" in error_msg or "资源包" in error_msg or "充值" in error_msg:
                            print("💡 提示: z.AI账户余额不足")
                            print("💡 解决方案: https://open.bigmodel.cn/console/payment")
                            return None
                        elif "模型不存在" in error_msg:
                            print("💡 提示: 模型名称错误，请检查配置")
                            return None
                except:
                    pass
                    
                return None
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 连接错误")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            print(f"响应内容: {response.text}")
            return None
        except Exception as e:
            print(f"❌ z.AI调用失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_reply_with_chatgpt(self, tweet_text):
        """使用ChatGPT模型生成回复"""
        print("🔍 步骤5: 调用ChatGPT生成回复...")
        
        # 检查API密钥
        if not self.openai_api_key or self.openai_api_key == "sk-your-openai-api-key-here":
            print("⚠️  OpenAI API密钥未配置")
            return None
        
        print(f"🔑 API密钥: {self.openai_api_key[:10]}...{self.openai_api_key[-5:]}")
        print(f"🌐 API端点: {self.openai_api_url}")
        print(f"🤖 AI模型: {self.openai_model}")
        
        try:
            # 检测推文语言
            is_english = is_english_text(tweet_text)
            language = "English" if is_english else "Chinese"
            language_instruction = "5. Reply in English" if is_english else "5. 要用中文回复"
            system_prompt = "You are a witty Twitter user who writes short, funny replies in English." if is_english else "你是一个幽默风趣的推特用户，擅长写简短有趣的中文回复。"
            
            print(f"🌍 检测到语言: {language}")
            
            # 构造ChatGPT的prompt
            prompt = f"""
请为这条推特写一个简短、幽默、没有emoji的回复：

推特内容：{tweet_text}

要求：
1. 简短（20字以内）
2. 幽默有趣
3. 不要使用emoji
4. 只生成一个回复选项
{language_instruction}

回复内容：
"""
            
            # ChatGPT API请求
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.openai_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS
            }
            
            print(f"🤖 正在调用ChatGPT模型...")
            print(f"请求参数: model={self.openai_model}, temperature={TEMPERATURE}, max_tokens={MAX_TOKENS}")
            
            response = requests.post(
                self.openai_api_url,
                headers=headers,
                json=data,
                timeout=(API_CONNECT_TIMEOUT, API_TIMEOUT)
            )
            
            print(f"📡 HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📄 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # 检查响应结构
                if 'choices' in result and len(result['choices']) > 0:
                    if 'message' in result['choices'][0]:
                        if 'content' in result['choices'][0]['message']:
                            reply = result['choices'][0]['message']['content'].strip()
                            
                            # 检查是否因token限制导致内容为空
                            finish_reason = result['choices'][0].get('finish_reason', '')
                            if finish_reason == 'length' and not reply:
                                print("⚠️  回复被截断（达到token限制），尝试减少token数量")
                                return None
                            
                            if reply:
                                print(f"✅ ChatGPT生成回复: {reply}")
                                return reply
                            else:
                                print("⚠️  AI生成了空回复")
                                return None
                
                print("❌ 响应结构异常")
                return None
            else:
                print(f"❌ ChatGPT API调用失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                
                # 尝试解析错误详情
                try:
                    error_info = response.json()
                    if 'error' in error_info:
                        error_msg = error_info['error'].get('message', '未知错误')
                        print(f"错误详情: {error_msg}")
                        
                        # 特殊处理常见错误
                        if "insufficient_quota" in str(error_info) or "exceeded" in str(error_info):
                            print("💡 提示: OpenAI账户配额不足")
                            print("💡 解决方案: https://platform.openai.com/account/billing")
                            return None
                        elif "invalid_api_key" in str(error_info):
                            print("💡 提示: API密钥无效，请检查配置")
                            return None
                except:
                    pass
                    
                return None
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 连接错误")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            print(f"响应内容: {response.text}")
            return None
        except Exception as e:
            print(f"❌ ChatGPT调用失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_reply(self, tweet_text):
        """根据配置选择AI提供商生成回复"""
        if self.ai_provider == "chatgpt":
            return self.generate_reply_with_chatgpt(tweet_text)
        else:
            return self.generate_reply_with_zai(tweet_text)
    
    async def send_reply(self, reply_text):
        """发送回复"""
        print("🔍 步骤6: 发送回复...")
        try:
            # 等待页面稳定
            await asyncio.sleep(1)
            
            # 尝试点击回复按钮
            reply_selectors = [
                'button[data-testid="reply"]',
                'button[aria-label*="回复"]',
                'button[aria-label*="Reply"]',
                'div[data-testid="reply"] button'
            ]
            
            reply_clicked = False
            for selector in reply_selectors:
                try:
                    reply_btn = await self.page.query_selector(selector)
                    if reply_btn:
                        await reply_btn.click()
                        await asyncio.sleep(1)
                        reply_clicked = True
                        print("✅ 点击了回复按钮")
                        break
                except:
                    continue
            
            if not reply_clicked:
                print("❌ 没有找到回复按钮")
                return False
            
            # 等待回复弹窗出现
            await asyncio.sleep(1)
            
            # 查找回复输入框
            input_selectors = [
                'div[data-testid="tweetTextarea_0"]',
                'div[contenteditable="true"][role="textbox"]',
                'textarea[placeholder*="回复"]',
                'textarea[placeholder*="reply"]'
            ]
            
            input_filled = False
            for selector in input_selectors:
                try:
                    input_box = await self.page.query_selector(selector)
                    if input_box:
                        # 清空输入框
                        await input_box.fill("")
                        await input_box.fill(reply_text)
                        await asyncio.sleep(0.5)
                        input_filled = True
                        print(f"✅ 输入回复: {reply_text}")
                        break
                except:
                    continue
            
            if not input_filled:
                print("❌ 没有找到输入框")
                return False
            
            # 查找发送按钮
            send_selectors = [
                'button[data-testid="tweetButtonInline"]',
                'button[data-testid="tweetButton"]',
                'div[role="button"] span:has-text("发布")',
                'div[role="button"] span:has-text("Post")'
            ]
            
            for selector in send_selectors:
                try:
                    send_btn = await self.page.query_selector(selector)
                    if send_btn and await send_btn.is_enabled():
                        await send_btn.click()
                        await asyncio.sleep(3)
                        print("✅ 点击了发送按钮")
                        return True
                except:
                    continue
            
            print("❌ 没有找到发送按钮")
            return False
            
        except Exception as e:
            print(f"❌ 发送回复失败: {e}")
            return False
    
    async def run(self, count=1):
        """运行主流程"""
        provider_name = "ChatGPT" if self.ai_provider == "chatgpt" else "z.AI"
        print(f"\n{'='*70}")
        print(f"🚀 Twitter Auto Reply Bot ({provider_name}) - 第 {count} 次执行")
        print(f"{'='*70}\n")
        
        success_count = 0
        
        # 1. 连接浏览器
        if not await self.connect_browser():
            return success_count
        
        # 2. 获取第一个标签页
        if not await self.get_first_tab():
            return success_count
        
        # 3. 导航到Twitter
        if not await self.navigate_to_twitter():
            return success_count
        
        # 4. 获取推文
        tweet = await self.get_first_tweet()
        if not tweet:
            return success_count
        
        # 5. 生成回复
        reply = self.generate_reply(tweet['text'])
        
        # 如果API失败，reply为None，不发送回复
        if not reply:
            print("⚠️  API调用失败，跳过回复")
            return success_count
        
        # 6. 发送回复
        if not await self.send_reply(reply):
            return success_count
        
        success_count += 1
        print(f"\n✅ 第 {count} 次执行完成！")
        print(f"{'='*70}\n")
        
        return success_count
    
    async def close(self):
        """关闭连接"""
        if self.browser:
            await self.browser.close()
            print("🔌 浏览器连接已关闭")

async def main():
    """主函数"""
    print("🔧 正在初始化Twitter Auto Reply Bot...")
    
    bot = TwitterAutoReply()
    
    try:
        # 运行一次（调试模式）
        success = await bot.run(count=1)
        
        if success > 0:
            print("\n🎉 成功完成一次完整执行！")
            print("📊 执行结果: ✅ 成功")
        else:
            print("\n❌ 执行失败，请检查日志")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())