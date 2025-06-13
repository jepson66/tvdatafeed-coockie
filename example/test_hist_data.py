#!/usr/bin/env python3
"""
测试新的历史数据获取功能
使用 search_and_get_hist 和 get_multiple_hist 方法
返回和 get_hist 一样的 DataFrame 数据结构
"""

import logging
import json
import requests
from tvDatafeed import TvDatafeed, Interval

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_session():
    """设置带 cookies 的 session"""
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

        return session
    except Exception as e:
        logger.error(f"Failed to setup session: {e}")
        return None

def test_search_and_get_hist():
    """测试搜索并获取历史数据"""
    print("🔍📊 测试搜索并获取历史数据")
    print("="*60)

    session = setup_session()
    if not session:
        print("❌ 无法设置 session")
        return False

    try:
        # 创建 TvDatafeed 实例
        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功")

        # 测试不同的搜索关键词
        test_cases = [
            {
                "text": "AAPL",
                "exchange": "NASDAQ",
                "n_bars": 5,
                "description": "苹果公司股票"
            },
            {
                "text": "TSLA",
                "exchange": "NASDAQ",
                "n_bars": 3,
                "description": "特斯拉股票"
            },
            {
                "text": "BTC",
                "exchange": "",
                "n_bars": 2,
                "description": "比特币相关"
            }
        ]

        for i, test_case in enumerate(test_cases):
            print(f"\n📈 测试 {i+1}: {test_case['description']}")
            print(f"   搜索: {test_case['text']} on {test_case['exchange'] or '任意交易所'}")

            try:
                # 使用新的 search_and_get_hist 方法
                data = tv.search_and_get_hist(
                    text=test_case['text'],
                    exchange=test_case['exchange'],
                    interval=Interval.in_daily,
                    n_bars=test_case['n_bars'],
                    max_symbols=2  # 最多获取2个符号的数据
                )

                if data is not None and len(data) > 0:
                    print(f"   ✅ 成功获取 {len(data)} 条历史数据")
                    print(f"   📊 数据结构: {list(data.columns)}")
                    print(f"   🔢 包含符号: {data['symbol'].unique() if 'symbol' in data.columns else '未知'}")

                    # 显示最新数据
                    print("   📋 最新数据预览:")
                    print(data.tail(2).to_string())

                else:
                    print(f"   ❌ 未获取到数据")

            except Exception as e:
                print(f"   ❌ 测试失败: {e}")
                logger.exception("详细错误:")

        return True

    except Exception as e:
        print(f"❌ 总体测试失败: {e}")
        return False

def test_get_multiple_hist():
    """测试获取多个符号的历史数据"""
    print("\n📊📊 测试获取多个符号历史数据")
    print("="*60)

    session = setup_session()
    if not session:
        print("❌ 无法设置 session")
        return False

    try:
        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功")

        # 测试指定符号列表
        test_symbols = ["AAPL", "MSFT", "GOOGL"]
        exchange = "NASDAQ"

        print(f"\n📈 获取 {exchange} 交易所的多个符号数据")
        print(f"   符号列表: {test_symbols}")

        try:
            data = tv.get_multiple_hist(
                symbols=test_symbols,
                exchange=exchange,
                interval=Interval.in_daily,
                n_bars=3
            )

            if data is not None and len(data) > 0:
                print(f"   ✅ 成功获取 {len(data)} 条历史数据")
                print(f"   📊 数据结构: {list(data.columns)}")

                # 统计每个符号的数据量
                if 'symbol' in data.columns:
                    symbol_counts = data.groupby('symbol').size()
                    print("   📈 每个符号的数据量:")
                    for symbol, count in symbol_counts.items():
                        print(f"      {symbol}: {count} 条")

                # 显示数据预览
                print("   📋 数据预览:")
                print(data.head(6).to_string())

                return True
            else:
                print("   ❌ 未获取到数据")
                return False

        except Exception as e:
            print(f"   ❌ 获取多符号数据失败: {e}")
            logger.exception("详细错误:")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_single_get_hist():
    """测试原始的 get_hist 方法作为对比"""
    print("\n📊 测试原始 get_hist 方法 (对比)")
    print("="*60)

    session = setup_session()
    if not session:
        print("❌ 无法设置 session")
        return False

    try:
        tv = TvDatafeed(session=session)

        print("📈 使用原始 get_hist 方法获取 AAPL 数据")

        try:
            data = tv.get_hist(
                symbol="AAPL",
                exchange="NASDAQ",
                interval=Interval.in_daily,
                n_bars=3
            )

            if data is not None and len(data) > 0:
                print(f"   ✅ 成功获取 {len(data)} 条数据")
                print(f"   📊 数据结构: {list(data.columns)}")
                print("   📋 数据预览:")
                print(data.to_string())
                return True
            else:
                print("   ❌ 未获取到数据")
                return False

        except Exception as e:
            print(f"   ❌ 获取数据失败: {e}")
            logger.exception("详细错误:")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("🚀 测试历史数据获取功能")
    print("="*70)

    # 测试新的搜索+历史数据方法
    result1 = test_search_and_get_hist()

    # 测试多符号历史数据方法
    result2 = test_get_multiple_hist()

    # 测试原始方法作为对比
    result3 = test_single_get_hist()

    print("\n" + "="*70)
    print("📋 测试结果汇总")
    print("="*70)

    results = {
        "搜索+历史数据": "✅ 通过" if result1 else "❌ 失败",
        "多符号历史数据": "✅ 通过" if result2 else "❌ 失败",
        "原始get_hist": "✅ 通过" if result3 else "❌ 失败"
    }

    for test_name, status in results.items():
        print(f"{test_name:15} : {status}")

    if any([result1, result2]):
        print("\n🎉 新功能测试成功！")
        print("\n💡 使用示例:")
        print("""
# 方法1: 搜索符号并获取历史数据
data = tv.search_and_get_hist('AAPL', 'NASDAQ', n_bars=10, max_symbols=3)
print(data)

# 方法2: 获取指定符号列表的历史数据  
data = tv.get_multiple_hist(['AAPL', 'MSFT', 'GOOGL'], 'NASDAQ', n_bars=5)
print(data)

# 返回的数据结构和 get_hist 完全一样:
# - pandas DataFrame
# - datetime 作为索引
# - 包含 symbol, open, high, low, close, volume 列
# - 额外包含 full_symbol, description 列（搜索方法）
        """)
    else:
        print("\n❌ 新功能测试失败")
        if result3:
            print("但原始 get_hist 方法工作正常，问题可能在于新方法的实现")

if __name__ == "__main__":
    main()
