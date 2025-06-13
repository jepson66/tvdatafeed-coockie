#!/usr/bin/env python3
"""
使用代理测试 WebSocket 连接和 get_hist 方法
"""

import os
import logging
from tvDatafeed import TvDatafeed, Interval

# 设置代理环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_with_proxy_and_auth_token():
    """使用代理和 auth_token 测试"""
    print("🌐 使用代理测试 WebSocket 连接")
    print("="*60)
    print(f"🔗 代理设置: http://127.0.0.1:7890")
    
    # 你提供的 auth_token
    auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"
    
    try:
        # 创建 TvDatafeed 实例
        tv = TvDatafeed()
        tv.token = auth_token  # 直接设置你提供的 token
        
        print("✅ TvDatafeed 实例创建成功")
        print(f"🔑 使用提供的 auth_token")
        
        # 测试多个场景
        test_cases = [
            {
                "symbol": "AAPL",
                "exchange": "NASDAQ",
                "interval": Interval.in_daily,
                "n_bars": 5,
                "description": "AAPL 日线数据"
            },
            {
                "symbol": "AAPL", 
                "exchange": "NASDAQ",
                "interval": Interval.in_1_minute,
                "n_bars": 10,
                "description": "AAPL 1分钟数据"
            },
            {
                "symbol": "EURUSD",
                "exchange": "FX_IDC", 
                "interval": Interval.in_daily,
                "n_bars": 3,
                "description": "EURUSD 日线数据"
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"\n📈 测试 {i+1}: {test_case['description']}")
            print(f"   符号: {test_case['symbol']}")
            print(f"   交易所: {test_case['exchange']}")
            print(f"   间隔: {test_case['interval'].value}")
            print(f"   数量: {test_case['n_bars']}")
            
            try:
                print("   🔌 正在建立 WebSocket 连接...")
                
                data = tv.get_hist(
                    symbol=test_case['symbol'],
                    exchange=test_case['exchange'],
                    interval=test_case['interval'],
                    n_bars=test_case['n_bars']
                )
                
                if data is not None and len(data) > 0:
                    print(f"   ✅ 成功获取 {len(data)} 条历史数据！")
                    print(f"   📊 数据列: {list(data.columns)}")
                    print(f"   📅 时间范围: {data.index.min()} 到 {data.index.max()}")
                    
                    # 显示前3条数据
                    print(f"\n   📋 {test_case['description']} - 前3条:")
                    print(data.head(3).to_string())
                    
                    success_count += 1
                else:
                    print("   ❌ 未获取到数据")
                    
            except Exception as e:
                print(f"   ❌ 获取失败: {e}")
                logger.exception("详细错误:")
        
        print(f"\n🎯 测试结果: {success_count}/{len(test_cases)} 成功")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ 总体测试失败: {e}")
        logger.exception("详细错误:")
        return False

def main():
    print("🚀 使用代理测试 WebSocket 连接和历史数据获取")
    print("="*70)
    
    # 显示代理设置
    print("🌐 代理配置:")
    print(f"   HTTP_PROXY: {os.environ.get('HTTP_PROXY', 'Not set')}")
    print(f"   HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', 'Not set')}")
    
    # 执行测试
    success = test_with_proxy_and_auth_token()
    
    print("\n" + "="*70)
    print("📋 测试总结")
    print("="*70)
    
    if success:
        print("🎉 测试成功！")
        print("✅ WebSocket 连接正常")
        print("✅ auth_token 有效")
        print("✅ 可以获取真实的 OHLCV 历史数据")
        print("\n💡 这证明了:")
        print("- get_hist 方法确实可以通过 WebSocket 获取数据")
        print("- 你的 auth_token 是完全有效的")
        print("- 代理解决了网络连接问题")
    else:
        print("❌ 测试失败")
        print("可能原因:")
        print("- 代理设置问题")
        print("- WebSocket 仍然被阻止")
        print("- auth_token 问题")

if __name__ == "__main__":
    main() 