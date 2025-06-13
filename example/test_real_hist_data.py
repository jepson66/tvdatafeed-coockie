#!/usr/bin/env python3
"""
测试真实历史数据获取
专门测试获取真实的 OHLCV K线数据
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

def setup_session_with_cookies():
    """设置带真实 cookies 的 session"""
    try:
        # 读取真实 cookies
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        # 创建 session 并注入 cookies
        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        # 设置完整的 headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tradingview.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.tradingview.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        })

        logger.info("Session with cookies created successfully")
        return session
    except Exception as e:
        logger.error(f"Failed to setup session: {e}")
        return None

def test_real_hist_data():
    """测试获取真实历史数据"""
    print("📊 测试获取真实历史数据")
    print("="*60)

    session = setup_session_with_cookies()
    if not session:
        print("❌ 无法设置 session")
        return False

    try:
        # 创建 TvDatafeed 实例
        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功（使用真实 cookies）")

        # 测试用例 - 不同的时间间隔和股票
        test_cases = [
            {
                "symbol": "AAPL",
                "exchange": "NASDAQ",
                "interval": Interval.in_1_minute,
                "n_bars": 5,
                "description": "美国 AAPL 最近5条1分钟数据"
            },
            {
                "symbol": "AAPL",
                "exchange": "NASDAQ",
                "interval": Interval.in_daily,
                "n_bars": 3,
                "description": "美国 AAPL 最近3条日线数据"
            },
            {
                "symbol": "000001",
                "exchange": "SZSE",
                "interval": Interval.in_1_minute,
                "n_bars": 5,
                "description": "中国000001最近5条1分钟数据"
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
                data = tv.get_hist(
                    symbol=test_case['symbol'],
                    exchange=test_case['exchange'],
                    interval=test_case['interval'],
                    n_bars=test_case['n_bars']
                )

                if data is not None and len(data) > 0:
                    print(f"   ✅ 成功获取 {len(data)} 条真实历史数据")
                    print(f"   📊 数据结构: {list(data.columns)}")
                    print(f"   📅 时间范围: {data.index.min()} 到 {data.index.max()}")

                    # 显示数据
                    print(f"\n   📋 {test_case['description']}:")
                    print(data.to_string())

                    # 验证数据完整性
                    if all(col in data.columns for col in ['symbol', 'open', 'high', 'low', 'close', 'volume']):
                        print("   ✅ 数据结构正确，包含所有必要列")
                        success_count += 1
                    else:
                        print("   ⚠️  数据结构不完整")

                else:
                    print(f"   ❌ 未获取到数据")

            except Exception as e:
                print(f"   ❌ 获取数据失败: {e}")
                logger.exception("详细错误信息:")

        if success_count > 0:
            print(f"\n🎉 成功获取了 {success_count}/{len(test_cases)} 个测试用例的真实数据！")
            return True
        else:
            print(f"\n❌ 所有测试用例都失败了")
            return False

    except Exception as e:
        print(f"❌ 总体测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

def test_search_and_get_real_hist():
    """测试搜索并获取真实历史数据"""
    print("\n🔍📊 测试搜索并获取真实历史数据")
    print("="*60)

    session = setup_session_with_cookies()
    if not session:
        print("❌ 无法设置 session")
        return False

    try:
        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功")

        # 测试搜索 + 真实历史数据
        search_keyword = "AAPL"
        exchange = "NASDAQ"

        print(f"\n🔍 搜索 {search_keyword} 符号...")

        # 使用新的搜索+历史数据方法
        data = tv.search_and_get_hist(
            text=search_keyword,
            exchange=exchange,
            interval=Interval.in_daily,
            n_bars=3,
            max_symbols=1  # 只获取1个符号避免超时
        )

        if data is not None and len(data) > 0:
            print(f"✅ 成功获取 {len(data)} 条真实历史数据")
            print(f"📊 数据结构: {list(data.columns)}")
            print(f"🔢 包含符号: {data['symbol'].unique()}")

            print(f"\n📋 {search_keyword} 真实历史数据:")
            print(data.to_string())

            return True
        else:
            print("❌ 未获取到真实历史数据")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

def main():
    print("🚀 真实历史数据获取测试")
    print("="*70)

    # 测试直接获取历史数据
    result1 = test_real_hist_data()

    # 测试搜索+获取历史数据
    result2 = test_search_and_get_real_hist()

    print("\n" + "="*70)
    print("📋 测试结果汇总")
    print("="*70)

    results = {
        "直接获取历史数据": "✅ 通过" if result1 else "❌ 失败",
        "搜索+历史数据": "✅ 通过" if result2 else "❌ 失败"
    }

    for test_name, status in results.items():
        print(f"{test_name:15} : {status}")

    if result1 or result2:
        print("\n🎉 至少一种方式可以获取真实历史数据！")
        print("\n💡 成功的方法可以获取到类似这样的数据:")
        print("""
datetime                    symbol      open     high      low    close   volume
2025-06-06 03:55:00    NASDAQ:AAPL   200.38   200.570   200.300   200.46  29661.0
2025-06-06 03:56:00    NASDAQ:AAPL   200.42   200.520   200.280   200.35  26666.0
2025-06-06 03:57:00    NASDAQ:AAPL   200.38   200.485   200.300   200.43  29823.0
        """)

        print("\n🚀 推荐使用方式:")
        print("""
# 获取真实历史数据
from tvDatafeed import TvDatafeed, Interval
import requests, json

# 设置带 cookies 的 session
with open("tv_cookies.json", 'r') as f:
    cookie_list = json.load(f)

session = requests.Session()
for c in cookie_list:
    session.cookies.set(c['name'], c['value'], domain=c['domain'])

tv = TvDatafeed(session=session)

# 获取1分钟级别的真实数据
data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_1_minute, n_bars=100)
print(f"美国AAPL最近{len(data)}条1分钟数据:")
print(data)

# 或者使用搜索+获取数据
data = tv.search_and_get_hist('AAPL', 'NASDAQ', Interval.in_1_minute, n_bars=100)
print(data)
        """)
    else:
        print("\n❌ 所有测试都失败了")
        print("\n🔍 可能的原因:")
        print("1. WebSocket 连接问题（网络/防火墙）")
        print("2. Cookie 权限不足")
        print("3. TradingView API 限制")
        print("4. 需要调整连接参数或重新获取 cookies")

if __name__ == "__main__":
    main()
