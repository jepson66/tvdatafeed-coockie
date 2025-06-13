#!/usr/bin/env python3
"""
测试用户提供的 auth_token
专门测试 WebSocket 连接和真实历史数据获取
"""

import logging
import json
import requests
from tvDatafeed import TvDatafeed, Interval

# 设置日志级别为 DEBUG 以查看详细信息
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_with_provided_auth_token():
    """使用用户提供的 auth_token 测试"""
    print("🔑 测试用户提供的 auth_token")
    print("="*60)
    
    # 用户提供的 auth_token
    auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"
    
    print(f"🔑 Auth Token (前50字符): {auth_token[:50]}...")
    
    try:
        # 直接使用 auth_token 创建 TvDatafeed 实例
        # 我们需要修改一下，让它直接使用这个 token
        tv = TvDatafeed()
        tv.token = auth_token  # 直接设置 token
        
        print("✅ TvDatafeed 实例创建成功（使用提供的 auth_token）")
        
        # 测试 WebSocket 连接和数据获取
        test_cases = [
            {
                "symbol": "AAPL",
                "exchange": "NASDAQ", 
                "interval": Interval.in_daily,
                "n_bars": 5,
                "description": "NASDAQ:AAPL 日线数据（5条）"
            },
            {
                "symbol": "AAPL",
                "exchange": "NASDAQ",
                "interval": Interval.in_1_minute,
                "n_bars": 10,
                "description": "NASDAQ:AAPL 1分钟数据（10条）"
            },
            {
                "symbol": "EURUSD",
                "exchange": "FX_IDC",
                "interval": Interval.in_daily,
                "n_bars": 3,
                "description": "FX_IDC:EURUSD 日线数据（3条）"
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"\n📈 测试 {i+1}: {test_case['description']}")
            print(f"   符号: {test_case['symbol']}")
            print(f"   交易所: {test_case['exchange']}")
            print(f"   间隔: {test_case['interval'].value}")
            print(f"   K线数量: {test_case['n_bars']}")
            
            try:
                # 获取历史数据
                print("   🔌 正在建立 WebSocket 连接...")
                data = tv.get_hist(
                    symbol=test_case['symbol'],
                    exchange=test_case['exchange'],
                    interval=test_case['interval'],
                    n_bars=test_case['n_bars']
                )
                
                if data is not None and len(data) > 0:
                    print(f"   ✅ 成功获取 {len(data)} 条真实历史数据！")
                    print(f"   📊 数据结构: {list(data.columns)}")
                    print(f"   📅 时间范围: {data.index.min()} 到 {data.index.max()}")
                    
                    # 显示前几条数据
                    print(f"\n   📋 {test_case['description']} - 前3条数据:")
                    print(data.head(3).to_string())
                    
                    # 验证数据完整性
                    if all(col in data.columns for col in ['symbol', 'open', 'high', 'low', 'close', 'volume']):
                        print("   ✅ 数据结构正确，包含所有必要列（OHLCV）")
                        success_count += 1
                    else:
                        print("   ⚠️  数据结构不完整")
                        
                else:
                    print(f"   ❌ 未获取到数据")
                    
            except Exception as e:
                print(f"   ❌ 获取数据失败: {e}")
                logger.exception("详细错误信息:")
        
        if success_count > 0:
            print(f"\n🎉 使用提供的 auth_token 成功获取了 {success_count}/{len(test_cases)} 个测试用例的真实数据！")
            return True
        else:
            print(f"\n❌ 所有测试用例都失败了")
            return False
        
    except Exception as e:
        print(f"❌ 总体测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

def analyze_websocket_connection_process():
    """分析 WebSocket 连接过程"""
    print("\n🔍 WebSocket 连接过程分析")
    print("="*60)
    
    print("📋 get_hist 方法的 WebSocket 连接流程:")
    print("1. 调用 __create_connection() 建立 WebSocket 连接")
    print("   - 连接地址: wss://data.tradingview.com/socket.io/websocket")
    print("   - Headers: {'Origin': 'https://data.tradingview.com'}")
    print("   - 超时时间: 15秒")
    print("   - 重试机制: 最多3次，每次间隔2秒")
    
    print("\n2. 发送认证和配置消息:")
    print("   - set_auth_token: 设置认证 token")
    print("   - chart_create_session: 创建图表会话")
    print("   - quote_create_session: 创建报价会话") 
    print("   - quote_set_fields: 设置数据字段")
    print("   - quote_add_symbols: 添加符号")
    print("   - resolve_symbol: 解析符号")
    print("   - create_series: 创建数据序列")
    print("   - switch_timezone: 设置时区")
    
    print("\n3. 接收数据:")
    print("   - 循环接收 WebSocket 消息")
    print("   - 直到收到 'series_completed' 消息")
    print("   - 解析原始数据并转换为 pandas DataFrame")
    
    print("\n🔧 可能的连接问题:")
    print("1. 网络防火墙阻止 WebSocket 连接")
    print("2. 代理设置问题")
    print("3. auth_token 无效或过期")
    print("4. TradingView 服务器限制")
    
    print("\n💡 你提供的 auth_token 的优势:")
    print("- 跳过了复杂的登录和 cookie 验证过程")
    print("- 直接使用有效的认证 token")
    print("- 避免了 CAPTCHA 问题")

def decode_jwt_info():
    """解码 JWT token 信息（仅用于分析，不验证签名）"""
    print("\n🔍 JWT Token 信息分析")
    print("="*60)
    
    auth_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxMDc1NDM1NjUsImV4cCI6MTc0OTcwNTY5OSwiaWF0IjoxNzQ5NjkxMjk5LCJwbGFuIjoiIiwicHJvc3RhdHVzIjpudWxsLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjozLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9hbGVydF9jb25kaXRpb25zIjpudWxsLCJtYXhfb3ZlcmFsbF9hbGVydHMiOjIwMDAsIm1heF9hY3RpdmVfcHJpbWl0aXZlX2FsZXJ0cyI6MywibWF4X2FjdGl2ZV9jb21wbGV4X2FsZXJ0cyI6MCwibWF4X2Nvbm5lY3Rpb25zIjoyfQ.z-tc74sfQbuLjuI61GYrGJ7ESHksIvHnPUMcHx1cKQb2CNOs9KsV389HuN6XSJaAYocWJxFabhsGBzdFtpPPtM13GXKP2cYt51_Thun1eoRHAnbN8437q7e7MRakAodBAmOSzAp7nK-PYasdGIuEeQ0iwz2q1BpegARapYQCgO8"
    
    try:
        import base64
        import json
        from datetime import datetime
        
        # 分割 JWT token
        parts = auth_token.split('.')
        if len(parts) != 3:
            print("❌ 无效的 JWT token 格式")
            return
        
        # 解码 header
        header_data = base64.urlsafe_b64decode(parts[0] + '==').decode('utf-8')
        header = json.loads(header_data)
        print("📋 JWT Header:")
        for key, value in header.items():
            print(f"  {key}: {value}")
        
        # 解码 payload
        payload_data = base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8')
        payload = json.loads(payload_data)
        print("\n📋 JWT Payload:")
        for key, value in payload.items():
            if key in ['exp', 'iat']:
                # 转换时间戳
                dt = datetime.fromtimestamp(value)
                print(f"  {key}: {value} ({dt})")
            else:
                print(f"  {key}: {value}")
        
        # 检查 token 是否过期
        exp_time = datetime.fromtimestamp(payload['exp'])
        current_time = datetime.now()
        if current_time < exp_time:
            print(f"\n✅ Token 有效，到期时间: {exp_time}")
        else:
            print(f"\n❌ Token 已过期，过期时间: {exp_time}")
        
    except Exception as e:
        print(f"❌ 解码 JWT token 失败: {e}")

def main():
    print("🚀 使用提供的 auth_token 测试 WebSocket 连接")
    print("="*70)
    
    # 分析 WebSocket 连接过程
    analyze_websocket_connection_process()
    
    # 解码 JWT 信息
    decode_jwt_info()
    
    # 使用提供的 auth_token 进行测试
    result = test_with_provided_auth_token()
    
    print("\n" + "="*70)
    print("📋 测试结果汇总")
    print("="*70)
    
    if result:
        print("✅ 使用提供的 auth_token 成功获取了真实历史数据！")
        print("\n🎯 这证明了:")
        print("1. ✅ WebSocket 连接可以建立")
        print("2. ✅ auth_token 是有效的")
        print("3. ✅ 可以绕过 CAPTCHA 和复杂的登录过程")
        print("4. ✅ 能够获取真实的 OHLCV 历史数据")
        
        print("\n🚀 推荐使用方式:")
        print("""
# 直接使用 auth_token
from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()
tv.token = "你的_auth_token"  # 直接设置 token

# 获取真实历史数据
data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_1_minute, n_bars=100)
print(f"获取到 {len(data)} 条真实数据")
print(data.head())
        """)
        
    else:
        print("❌ 测试失败，可能的原因:")
        print("1. 网络连接问题（防火墙/代理）")
        print("2. WebSocket 连接被阻止")
        print("3. auth_token 可能已过期")
        print("4. TradingView 服务器问题")

if __name__ == "__main__":
    main() 