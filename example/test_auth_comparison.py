#!/usr/bin/env python3
"""
对比不同认证方式的数据访问权限
测试 cookie 认证是否能绕过 CAPTCHA 限制，获取更多数据
"""

import os
import logging
import json
import requests
from tvDatafeed import TvDatafeed, Interval

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_no_auth():
    """测试无认证方式"""
    print("🚫 测试无认证方式")
    print("-" * 40)

    try:
        tv = TvDatafeed()  # 无认证
        print(f"🔑 Token: {tv.token}")

        # 测试获取数据
        data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_daily, n_bars=100)

        if data is not None and len(data) > 0:
            print(f"✅ 获取到 {len(data)} 条数据")
            print(f"📅 时间范围: {data.index.min()} 到 {data.index.max()}")
            return len(data)
        else:
            print("❌ 未获取到数据")
            return 0

    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0

def test_cookie_auth():
    """测试 cookie 认证方式"""
    print("\n🍪 测试 Cookie 认证方式")
    print("-" * 40)

    try:
        # 读取 cookies
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        # 创建带 cookies 的 session
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        tv = TvDatafeed(session=session)
        print(f"🔑 Token: {tv.token}")

        # 测试获取数据
        data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_daily, n_bars=100)

        if data is not None and len(data) > 0:
            print(f"✅ 获取到 {len(data)} 条数据")
            print(f"📅 时间范围: {data.index.min()} 到 {data.index.max()}")
            return len(data)
        else:
            print("❌ 未获取到数据")
            return 0

    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0

def test_direct_token_auth():
    """测试直接使用 auth_token"""
    print("\n🎫 测试直接 Auth Token 方式")
    print("-" * 40)

    try:
        auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"

        tv = TvDatafeed()
        tv.token = auth_token  # 直接设置有效的 token
        print(f"🔑 Token: {auth_token[:50]}...")

        # 测试获取数据
        data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_daily, n_bars=100)

        if data is not None and len(data) > 0:
            print(f"✅ 获取到 {len(data)} 条数据")
            print(f"📅 时间范围: {data.index.min()} 到 {data.index.max()}")
            return len(data)
        else:
            print("❌ 未获取到数据")
            return 0

    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0

def test_data_quality_comparison():
    """对比不同认证方式的数据质量"""
    print("\n📊 数据质量对比测试")
    print("=" * 60)

    # 测试不同时间周期的数据获取能力
    test_cases = [
        {"interval": Interval.in_daily, "n_bars": 100, "desc": "日线数据(100条)"},
        {"interval": Interval.in_1_hour, "n_bars": 200, "desc": "1小时数据(200条)"},
        {"interval": Interval.in_1_minute, "n_bars": 500, "desc": "1分钟数据(500条)"},
    ]

    auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"

    # 创建不同认证方式的实例
    tv_no_auth = TvDatafeed()

    # Cookie 认证
    try:
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])
        tv_cookie = TvDatafeed(session=session)
    except:
        tv_cookie = None

    # Token 认证
    tv_token = TvDatafeed()
    tv_token.token = auth_token

    results = {}

    for test_case in test_cases:
        print(f"\n📈 测试: {test_case['desc']}")
        print("-" * 40)

        # 无认证
        try:
            data = tv_no_auth.get_hist('AAPL', 'NASDAQ', test_case['interval'], test_case['n_bars'])
            no_auth_count = len(data) if data is not None else 0
        except:
            no_auth_count = 0

        # Cookie 认证
        if tv_cookie:
            try:
                data = tv_cookie.get_hist('AAPL', 'NASDAQ', test_case['interval'], test_case['n_bars'])
                cookie_count = len(data) if data is not None else 0
            except:
                cookie_count = 0
        else:
            cookie_count = 0

        # Token 认证
        try:
            data = tv_token.get_hist('AAPL', 'NASDAQ', test_case['interval'], test_case['n_bars'])
            token_count = len(data) if data is not None else 0
        except:
            token_count = 0

        print(f"无认证:     {no_auth_count:3d} 条")
        print(f"Cookie认证: {cookie_count:3d} 条")
        print(f"Token认证:  {token_count:3d} 条")

        results[test_case['desc']] = {
            'no_auth': no_auth_count,
            'cookie': cookie_count,
            'token': token_count
        }

    return results

def main():
    print("🔍 TradingView 认证方式数据访问权限对比")
    print("=" * 60)
    print("目标: 验证 Cookie 认证是否能绕过 CAPTCHA 限制，获取更多数据")

    # 基础测试
    no_auth_data = test_no_auth()
    cookie_data = test_cookie_auth()
    token_data = test_direct_token_auth()

    # 详细对比测试
    detailed_results = test_data_quality_comparison()

    # 总结
    print("\n" + "=" * 60)
    print("📋 测试结果总结")
    print("=" * 60)

    print(f"基础测试 (AAPL 日线 100条):")
    print(f"  无认证:     {no_auth_data:3d} 条")
    print(f"  Cookie认证: {cookie_data:3d} 条")
    print(f"  Token认证:  {token_data:3d} 条")

    print(f"\n详细测试结果:")
    for desc, counts in detailed_results.items():
        print(f"  {desc}:")
        print(f"    无认证:     {counts['no_auth']:3d} 条")
        print(f"    Cookie认证: {counts['cookie']:3d} 条")
        print(f"    Token认证:  {counts['token']:3d} 条")

    # 分析结论
    print(f"\n🎯 结论分析:")
    if cookie_data > no_auth_data:
        print("✅ Cookie 认证确实能获取更多数据，成功绕过了 CAPTCHA 限制！")
    elif cookie_data == token_data:
        print("✅ Cookie 认证效果等同于完整 Token 认证！")
    else:
        print("⚠️  Cookie 认证可能需要进一步优化")

    if token_data > no_auth_data:
        print("✅ 有效的 auth_token 确实能获取更多数据")

    print(f"\n💡 建议:")
    print("- 如果 Cookie 认证数据量 > 无认证，说明 Cookie 方案有效")
    print("- 如果 Cookie 认证数据量 = Token 认证，说明 Cookie 完全等效")
    print("- 可以使用 Cookie 方式避免 CAPTCHA，获取完整数据访问权限")

if __name__ == "__main__":
    main()
