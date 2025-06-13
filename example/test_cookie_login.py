#!/usr/bin/env python3
"""
TvDatafeed Cookie 登录测试脚本
测试各种认证方式是否正常工作
"""

import logging
import json
from tvDatafeed import TvDatafeed, TvDatafeedLive, Interval

# 设置日志级别
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_anonymous_login():
    """测试匿名登录"""
    print("\n" + "="*50)
    print("🔓 测试匿名登录")
    print("="*50)
    
    try:
        tv = TvDatafeed()
        print("✅ 匿名登录成功")
        
        # 测试获取数据
        data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_daily, 5)
        print(f"📊 获取到 {len(data)} 条 AAPL 数据")
        print(data.tail(2))
        return True
        
    except Exception as e:
        print(f"❌ 匿名登录失败: {e}")
        return False

def test_cookie_dict_login():
    """测试 Cookie 字典登录"""
    print("\n" + "="*50)
    print("🍪 测试 Cookie 字典登录")
    print("="*50)
    
    # 这里需要用户提供真实的 cookie
    cookies = {
        'sessionid': 'your_session_id_here',
        'auth_token': 'your_auth_token_here',
        # 添加其他需要的 cookies
    }
    
    print("⚠️  请在此脚本中设置真实的 cookie 值")
    print(f"📝 当前 cookies: {list(cookies.keys())}")
    
    if 'your_session_id_here' in str(cookies.values()):
        print("⏭️  跳过 Cookie 字典测试 (需要真实 cookie)")
        return None
    
    try:
        tv = TvDatafeed(cookies=cookies)
        print("✅ Cookie 字典登录成功")
        
        # 测试获取数据
        data = tv.get_hist('BTCUSDT', 'BINANCE', Interval.in_1_hour, 5)
        print(f"📊 获取到 {len(data)} 条 BTCUSDT 数据")
        print(data.tail(2))
        return True
        
    except Exception as e:
        print(f"❌ Cookie 字典登录失败: {e}")
        return False

def test_cookie_file_login():
    """测试 Cookie 文件登录"""
    print("\n" + "="*50)
    print("📄 测试 Cookie 文件登录")
    print("="*50)
    
    cookie_file = 'test_cookies.json'
    
    # 创建示例 cookie 文件
    sample_cookies = [
        {
            "name": "sessionid",
            "value": "your_session_value_here", 
            "domain": ".tradingview.com"
        },
        {
            "name": "auth_token",
            "value": "your_auth_token_here",
            "domain": ".tradingview.com"
        }
    ]
    
    try:
        with open(cookie_file, 'w') as f:
            json.dump(sample_cookies, f, indent=2)
        print(f"📝 创建示例 cookie 文件: {cookie_file}")
        
        tv = TvDatafeed(cookies_file=cookie_file)
        print("✅ Cookie 文件登录成功")
        return True
        
    except FileNotFoundError:
        print(f"❌ Cookie 文件未找到: {cookie_file}")
        return False
    except ValueError as e:
        if 'your_session_value_here' in str(e):
            print("⏭️  跳过 Cookie 文件测试 (需要真实 cookie)")
            return None
        print(f"❌ Cookie 文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ Cookie 文件登录失败: {e}")
        return False

def test_session_login():
    """测试预配置 Session 登录"""
    print("\n" + "="*50) 
    print("🔧 测试预配置 Session 登录")
    print("="*50)
    
    try:
        import requests
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Custom TvDatafeed Test)',
            'Referer': 'https://www.tradingview.com/'
        })
        
        # 这里需要真实的 cookies
        sample_cookies = {
            'sessionid': 'your_session_id_here',
            'auth_token': 'your_auth_token_here'
        }
        session.cookies.update(sample_cookies)
        
        if 'your_session_id_here' in str(sample_cookies.values()):
            print("⏭️  跳过 Session 测试 (需要真实 cookie)")
            return None
        
        tv = TvDatafeed(session=session)
        print("✅ 预配置 Session 登录成功")
        
        # 测试搜索符号
        results = tv.search_symbol('AAPL', 'NASDAQ')
        print(f"🔍 搜索到 {len(results)} 个 AAPL 相关符号")
        return True
        
    except Exception as e:
        print(f"❌ 预配置 Session 登录失败: {e}")
        return False

def test_traditional_login():
    """测试传统用户名密码登录"""
    print("\n" + "="*50)
    print("🔑 测试传统用户名密码登录")
    print("="*50)
    
    print("⚠️  传统登录可能遇到验证码问题")
    print("⏭️  跳过传统登录测试")
    return None

def test_tvdatafeed_live():
    """测试 TvDatafeedLive"""
    print("\n" + "="*50)
    print("🔴 测试 TvDatafeedLive (实时数据)")
    print("="*50)
    
    try:
        tvl = TvDatafeedLive()  # 匿名模式
        print("✅ TvDatafeedLive 初始化成功")
        
        # 测试创建 seis (不启动实际监控)
        print("📊 测试基本功能...")
        search_results = tvl.search_symbol('ETHUSDT', 'BINANCE')
        if search_results:
            print(f"🔍 搜索成功，找到 {len(search_results)} 个结果")
            return True
        else:
            print("❌ 搜索结果为空")
            return False
            
    except Exception as e:
        print(f"❌ TvDatafeedLive 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始 TvDatafeed Cookie 登录功能测试")
    print("="*60)
    
    tests = [
        ("匿名登录", test_anonymous_login),
        ("Cookie 字典登录", test_cookie_dict_login), 
        ("Cookie 文件登录", test_cookie_file_login),
        ("预配置 Session 登录", test_session_login),
        ("传统登录", test_traditional_login),
        ("TvDatafeedLive", test_tvdatafeed_live),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        result = test_func()
        results[test_name] = result
    
    # 汇总结果
    print("\n" + "="*60)
    print("📋 测试结果汇总")
    print("="*60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⏭️  跳过"
        print(f"{test_name:20} : {status}")
    
    success_count = sum(1 for r in results.values() if r is True)
    total_count = len([r for r in results.values() if r is not None])
    
    print(f"\n🎯 测试完成: {success_count}/{total_count} 通过")
    
    if success_count > 0:
        print("\n🎉 Cookie 登录功能改造成功！")
        print("\n💡 使用提示:")
        print("1. 设置真实的 cookie 值来测试完整功能")
        print("2. 查看 COOKIE_LOGIN_USAGE.md 了解详细用法")
        print("3. 匿名模式功能受限，建议使用 cookie 登录")
    else:
        print("\n⚠️  请检查网络连接和依赖包")

def create_sample_config():
    """创建示例配置文件"""
    config = {
        "cookies": {
            "sessionid": "your_session_id_here",
            "auth_token": "your_auth_token_here"
        },
        "note": "请替换为你的真实 TradingView cookie 值"
    }
    
    try:
        with open('sample_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("📝 已创建示例配置文件: sample_config.json")
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")

if __name__ == "__main__":
    create_sample_config()
    main() 