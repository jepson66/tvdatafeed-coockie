#!/usr/bin/env python3
"""
简化的 Cookie 登录测试
只测试核心功能，不涉及 WebSocket
"""

import json
import requests
from tvDatafeed import TvDatafeed, Interval

def test_simple_cookie_login():
    """简单的 Cookie 登录测试"""
    print("🍪 简化的 Cookie 登录测试")
    print("="*50)

    try:
        # 读取真实的 cookie 文件
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        # 手动创建 session 并注入 cookies
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        # 设置合适的 headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tradingview.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        })

        print("✅ 成功创建带 cookies 的 session")

        # 使用 session 创建 TvDatafeed
        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功")

        # 测试搜索功能 - 多个符号
        test_symbols = [
            ("AAPL", "NASDAQ"),
            ("TSLA", "NASDAQ"),
            ("BTCUSDT", "BINANCE"),
            ("EURUSD", "FX_IDC")
        ]

        all_success = True
        for symbol, exchange in test_symbols:
            try:
                print(f"\n🔍 搜索 {symbol} ({exchange})...")
                results = tv.search_symbol(symbol, exchange)
                if results and len(results) > 0:
                    print(f"   ✅ 找到 {len(results)} 个结果")
                    # 显示第一个结果
                    first_result = results[0]
                    print(f"   📝 第一个结果: {first_result.get('symbol', 'N/A')} - {first_result.get('description', 'N/A')}")
                else:
                    print(f"   ❌ 没有找到结果")
                    all_success = False
            except Exception as e:
                print(f"   ❌ 搜索失败: {e}")
                all_success = False

        if all_success:
            print("\n🎉 所有搜索测试都成功!")
            return True
        else:
            print("\n⚠️  部分搜索测试失败")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_direct_api_call():
    """直接测试 API 调用"""
    print("\n🌐 直接 API 调用测试")
    print("="*50)

    try:
        # 读取 cookies
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        # 创建 session
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        # 测试不同的 API 端点
        test_apis = [
            {
                "name": "符号搜索 API",
                "url": "https://symbol-search.tradingview.com/symbol_search/?text=AAPL&exchange=NASDAQ&lang=en&type=&domain=production",
                "method": "GET"
            },
            {
                "name": "Scanner API",
                "url": "https://scanner.tradingview.com/america/scan",
                "method": "POST",
                "data": {
                    "symbols": {
                        "tickers": ["NASDAQ:AAPL"],
                        "query": {"types": []}
                    },
                    "columns": ["open", "high", "low", "close", "volume"]
                }
            }
        ]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tradingview.com/',
            'Accept': 'application/json, text/plain, */*'
        }

        for api in test_apis:
            try:
                print(f"\n📡 测试 {api['name']}...")

                if api["method"] == "GET":
                    response = session.get(api["url"], headers=headers, timeout=10)
                else:
                    response = session.post(api["url"], json=api["data"], headers=headers, timeout=10)

                print(f"   状态码: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   ✅ 成功获取 {len(data)} 条数据")
                        elif isinstance(data, dict):
                            print(f"   ✅ 成功获取数据，键: {list(data.keys())}")
                        else:
                            print(f"   ✅ 成功获取响应")
                    except:
                        print(f"   ✅ 成功获取响应 (非JSON)")
                elif response.status_code == 403:
                    print(f"   ⚠️  权限不足 (403)")
                else:
                    print(f"   ❌ 请求失败")

            except Exception as e:
                print(f"   ❌ API 调用失败: {e}")

    except Exception as e:
        print(f"❌ 直接 API 测试失败: {e}")

def main():
    print("🚀 简化 Cookie 登录测试")
    print("="*60)

    # 核心功能测试
    result = test_simple_cookie_login()

    # 直接 API 测试
    test_direct_api_call()

    print("\n" + "="*60)
    print("📋 测试结果")
    print("="*60)

    if result:
        print("✅ Cookie 登录和搜索功能正常工作!")
        print("\n💡 结论:")
        print("- 你的 Cookie 是有效的")
        print("- 搜索功能正常")
        print("- 可以正常使用 TvDatafeed 进行符号搜索")
        print("- WebSocket 历史数据功能可能需要额外配置")

        print("\n🎯 推荐用法:")
        print("""
# 使用你的 cookie 文件
from tvDatafeed import TvDatafeed
import requests
import json

# 加载 cookies
with open("tv_cookies.json", 'r') as f:
    cookie_list = json.load(f)

session = requests.Session()
for c in cookie_list:
    session.cookies.set(c['name'], c['value'], domain=c['domain'])

tv = TvDatafeed(session=session)
results = tv.search_symbol('AAPL', 'NASDAQ')
print(results)
        """)
    else:
        print("❌ Cookie 登录测试失败")

if __name__ == "__main__":
    main()
