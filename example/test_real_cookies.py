#!/usr/bin/env python3
"""
测试真实 Cookie 文件的脚本
使用 com/jps/tv_cookies.json 进行测试
"""

import logging
import os
import sys
from tvDatafeed import TvDatafeed, Interval

# 设置日志级别为 DEBUG 以查看详细信息
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_real_cookie_file():
    """测试真实的 cookie 文件"""
    print("🍪 测试真实 Cookie 文件")
    print("="*50)

    # Cookie 文件路径
    cookie_file = "../../com/jps/tv_cookies.json"

    if not os.path.exists(cookie_file):
        print(f"❌ Cookie 文件不存在: {cookie_file}")
        return False

    try:
        print(f"📂 使用 Cookie 文件: {cookie_file}")

        # 创建 TvDatafeed 实例
        tv = TvDatafeed(cookies_file=cookie_file)
        print("✅ TvDatafeed 实例创建成功")

        # 测试搜索功能
        print("\n🔍 测试搜索功能...")
        search_results = tv.search_symbol('AAPL', 'NASDAQ')
        if search_results:
            print(f"✅ 搜索成功，找到 {len(search_results)} 个结果")
            # 显示前几个结果
            for i, result in enumerate(search_results[:3]):
                print(f"   {i+1}. {result.get('symbol', 'N/A')} - {result.get('description', 'N/A')}")
        else:
            print("❌ 搜索结果为空")
            return False

        # 测试获取历史数据
        print("\n📊 测试获取历史数据...")
        try:
            data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_daily, 5)
            if data is not None and len(data) > 0:
                print(f"✅ 成功获取 {len(data)} 条 AAPL 历史数据")
                print("\n最新数据:")
                print(data.tail(2))
                return True
            else:
                print("❌ 获取的历史数据为空")
                return False

        except Exception as e:
            print(f"❌ 获取历史数据失败: {e}")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

def test_cookie_extraction():
    """测试 Cookie 提取逻辑"""
    print("\n🔧 测试 Cookie 提取逻辑")
    print("="*50)

    import json
    cookie_file = "../../com/jps/tv_cookies.json"

    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)

        print(f"📄 Cookie 文件格式: {'列表' if isinstance(cookie_data, list) else '字典'}")

        if isinstance(cookie_data, list):
            cookies = {}
            for item in cookie_data:
                if 'name' in item and 'value' in item:
                    cookies[item['name']] = item['value']

            print(f"📋 提取到的 Cookie 数量: {len(cookies)}")
            print("🔑 关键 Cookies:")

            key_cookies = ['sessionid', 'auth_token', 'device_t', 'sessionid_sign']
            for key in key_cookies:
                if key in cookies:
                    value = cookies[key]
                    masked_value = value[:8] + "..." + value[-8:] if len(value) > 16 else value
                    print(f"   ✅ {key}: {masked_value}")
                else:
                    print(f"   ❌ {key}: 未找到")

            return cookies
        else:
            print("❌ 不支持的 Cookie 格式")
            return None

    except Exception as e:
        print(f"❌ Cookie 提取失败: {e}")
        return None

def test_manual_session():
    """手动测试 session 方式"""
    print("\n🔧 测试手动 Session 方式")
    print("="*50)

    import requests
    import json

    try:
        # 读取 cookies
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        # 创建 session 并注入 cookies
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        # 设置 headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tradingview.com/'
        })

        print("🌐 手动创建 session 并注入 cookies")

        # 使用 session 创建 TvDatafeed
        tv = TvDatafeed(session=session)
        print("✅ 使用预配置 session 创建 TvDatafeed 成功")

        # 测试搜索
        search_results = tv.search_symbol('TSLA', 'NASDAQ')
        if search_results:
            print(f"✅ 搜索成功，找到 {len(search_results)} 个 TSLA 结果")
            return True
        else:
            print("❌ 搜索结果为空")
            return False

    except Exception as e:
        print(f"❌ 手动 session 测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

def main():
    print("🚀 开始测试真实 Cookie 登录")
    print("="*60)

    # 测试 Cookie 提取
    cookies = test_cookie_extraction()

    # 测试文件方式
    result1 = test_real_cookie_file()

    # 测试手动 session 方式
    result2 = test_manual_session()

    print("\n" + "="*60)
    print("📋 测试结果汇总")
    print("="*60)

    results = {
        "Cookie 文件方式": "✅ 通过" if result1 else "❌ 失败",
        "手动 Session 方式": "✅ 通过" if result2 else "❌ 失败"
    }

    for test_name, status in results.items():
        print(f"{test_name:20} : {status}")

    if result1 or result2:
        print("\n🎉 至少一种方式测试成功！")
        print("\n💡 建议:")
        if result2 and not result1:
            print("- 文件方式失败但手动 session 成功，可能是认证逻辑需要优化")
        if result1:
            print("- Cookie 文件方式成功，可以直接使用")
    else:
        print("\n❌ 所有测试都失败了")
        print("\n🔍 可能的原因:")
        print("1. Cookie 已过期，需要重新获取")
        print("2. 网络连接问题")
        print("3. TradingView API 变化")

if __name__ == "__main__":
    main()
