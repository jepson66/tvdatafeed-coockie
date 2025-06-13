#!/usr/bin/env python3
"""
简化的 WebSocket 连接测试
使用提供的 auth_token 测试连接过程
"""

import logging
from tvDatafeed import TvDatafeed, Interval

# 设置简洁的日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_websocket_with_auth_token():
    """使用提供的 auth_token 测试 WebSocket 连接"""
    
    print("🔑 使用提供的 auth_token 测试 WebSocket 连接")
    print("="*50)
    
    # 你提供的 auth_token
    auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"
    
    try:
        # 创建 TvDatafeed 实例并设置 token
        tv = TvDatafeed()
        tv.token = auth_token
        
        print("✅ TvDatafeed 实例创建成功")
        print(f"🔑 Token 设置完成 (前30字符): {auth_token[:30]}...")
        
        # 测试获取 AAPL 日线数据
        print("\n📈 测试获取 AAPL 日线数据...")
        print("🔌 正在建立 WebSocket 连接...")
        
        data = tv.get_hist(
            symbol="AAPL",
            exchange="NASDAQ", 
            interval=Interval.in_daily,
            n_bars=5
        )
        
        if data is not None and len(data) > 0:
            print(f"✅ 成功获取 {len(data)} 条历史数据！")
            print(f"📊 数据列: {list(data.columns)}")
            print(f"📅 时间范围: {data.index.min()} 到 {data.index.max()}")
            
            print("\n📋 AAPL 最新5天数据:")
            print(data.to_string())
            
            return True
        else:
            print("❌ 未获取到数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("🚀 WebSocket 连接流程测试")
    print("="*50)
    
    print("📋 get_hist 方法的连接步骤:")
    print("1. 调用 __create_connection() 建立 WebSocket")
    print("   - 地址: wss://data.tradingview.com/socket.io/websocket")
    print("   - 超时: 15秒，重试3次")
    print("2. 发送 set_auth_token 消息")
    print("3. 创建图表和报价会话")
    print("4. 设置数据字段和符号")
    print("5. 创建数据序列 (关键步骤)")
    print("6. 循环接收数据直到 'series_completed'")
    print("7. 解析数据为 pandas DataFrame")
    
    print("\n" + "="*50)
    
    # 执行测试
    success = test_websocket_with_auth_token()
    
    print("\n" + "="*50)
    if success:
        print("🎉 WebSocket 连接测试成功！")
        print("✅ 证明了 auth_token 有效")
        print("✅ WebSocket 连接正常")
        print("✅ 数据获取成功")
    else:
        print("❌ WebSocket 连接测试失败")
        print("可能原因:")
        print("- 网络连接问题")
        print("- WebSocket 被防火墙阻止")
        print("- auth_token 过期")

if __name__ == "__main__":
    main() 