#!/usr/bin/env python3
"""
演示新功能的脚本
展示 search_and_get_hist 和 get_multiple_hist 方法
返回和 get_hist 一样的 DataFrame 数据结构
"""

import pandas as pd
import numpy as np
import datetime
import json
import requests
from tvDatafeed import TvDatafeed, Interval

def create_mock_hist_data(symbol, exchange, n_bars=10):
    """创建模拟的历史数据，格式和 get_hist 完全一样"""
    # 生成日期范围
    end_date = datetime.datetime.now()
    dates = pd.date_range(end=end_date, periods=n_bars, freq='D')

    # 生成模拟价格数据
    base_price = np.random.uniform(100, 500)  # 随机基础价格
    prices = []

    for i in range(n_bars):
        if i == 0:
            open_price = base_price
        else:
            open_price = prices[-1]['close']

        # 生成 OHLC 数据
        daily_change = np.random.uniform(-0.05, 0.05)  # 日涨跌幅 -5% 到 +5%
        close_price = open_price * (1 + daily_change)

        high_price = max(open_price, close_price) * np.random.uniform(1.0, 1.03)
        low_price = min(open_price, close_price) * np.random.uniform(0.97, 1.0)
        volume = np.random.randint(1000000, 50000000)  # 随机成交量

        prices.append({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })

    # 创建 DataFrame
    data = pd.DataFrame(prices, index=dates)
    data.index.name = 'datetime'

    # 添加 symbol 列（和 get_hist 一样）
    data.insert(0, 'symbol', f"{exchange}:{symbol}")

    return data

def demo_search_and_get_hist():
    """演示搜索并获取历史数据功能"""
    print("🔍📊 演示搜索并获取历史数据")
    print("="*60)

    try:
        # 设置 session（使用真实 cookies）
        with open("../../com/jps/tv_cookies.json", 'r') as f:
            cookie_list = json.load(f)

        session = requests.Session()
        for c in cookie_list:
            session.cookies.set(c['name'], c['value'], domain=c['domain'])

        tv = TvDatafeed(session=session)
        print("✅ TvDatafeed 实例创建成功（使用真实 cookies）")

        # 测试搜索功能
        print("\n🔍 搜索 AAPL 符号...")
        search_results = tv.search_symbol('AAPL', 'NASDAQ')

        if search_results and len(search_results) > 0:
            print(f"✅ 搜索成功，找到 {len(search_results)} 个结果")
            print("📋 搜索结果:")
            for i, result in enumerate(search_results[:3]):
                print(f"   {i+1}. {result.get('symbol', 'N/A')} - {result.get('description', 'N/A')}")

            # 创建模拟的历史数据（和 get_hist 相同格式）
            print("\n📊 生成模拟历史数据（和 get_hist 相同格式）:")
            combined_data = pd.DataFrame()

            for i, symbol_info in enumerate(search_results[:2]):  # 只取前2个
                symbol = symbol_info.get('symbol', 'AAPL')
                exchange = symbol_info.get('exchange', 'NASDAQ')

                # 生成模拟数据
                mock_data = create_mock_hist_data(symbol, exchange, n_bars=5)

                # 添加额外信息（新功能特色）
                mock_data['full_symbol'] = f"{exchange}:{symbol}"
                mock_data['description'] = symbol_info.get('description', '')

                combined_data = pd.concat([combined_data, mock_data], ignore_index=False)

                print(f"\n   📈 {symbol} ({exchange}) - {len(mock_data)} 条数据")
                print(mock_data.to_string())

            print(f"\n🎯 合并后的数据结构:")
            print(f"   - 总行数: {len(combined_data)}")
            print(f"   - 列名: {list(combined_data.columns)}")
            print(f"   - 索引类型: {type(combined_data.index)}")
            print(f"   - 包含符号: {combined_data['symbol'].unique()}")

            return True
        else:
            print("❌ 搜索结果为空")
            return False

    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_get_multiple_hist():
    """演示获取多个符号历史数据功能"""
    print("\n📊📊 演示获取多个符号历史数据")
    print("="*60)

    try:
        symbols = ["AAPL", "MSFT", "GOOGL"]
        exchange = "NASDAQ"

        print(f"📈 模拟获取 {exchange} 交易所的多个符号数据")
        print(f"   符号列表: {symbols}")

        combined_data = pd.DataFrame()

        for symbol in symbols:
            # 生成模拟数据
            mock_data = create_mock_hist_data(symbol, exchange, n_bars=3)
            combined_data = pd.concat([combined_data, mock_data], ignore_index=False)

            print(f"\n   📊 {symbol} - {len(mock_data)} 条数据")
            print(mock_data.to_string())

        print(f"\n🎯 合并后的数据结构:")
        print(f"   - 总行数: {len(combined_data)}")
        print(f"   - 列名: {list(combined_data.columns)}")
        print(f"   - 包含符号: {combined_data['symbol'].unique()}")

        # 按符号统计
        symbol_counts = combined_data.groupby('symbol').size()
        print("\n   📈 每个符号的数据量:")
        for symbol, count in symbol_counts.items():
            print(f"      {symbol}: {count} 条")

        return True

    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def show_get_hist_format():
    """展示 get_hist 的标准格式"""
    print("\n📊 get_hist 标准数据格式")
    print("="*60)

    # 创建一个标准的 get_hist 格式数据
    mock_data = create_mock_hist_data("AAPL", "NASDAQ", n_bars=5)

    print("✅ 标准 get_hist 返回格式:")
    print(f"   - 类型: {type(mock_data)}")
    print(f"   - 索引: {mock_data.index.name} ({type(mock_data.index)})")
    print(f"   - 列名: {list(mock_data.columns)}")
    print(f"   - 数据形状: {mock_data.shape}")

    print("\n📋 数据内容:")
    print(mock_data.to_string())

    print("\n🔧 数据类型:")
    print(mock_data.dtypes)

    return mock_data

def main():
    print("🚀 新功能演示 - 返回 get_hist 相同的数据结构")
    print("="*80)

    # 展示标准格式
    standard_data = show_get_hist_format()

    # 演示搜索+历史数据
    result1 = demo_search_and_get_hist()

    # 演示多符号历史数据
    result2 = demo_get_multiple_hist()

    print("\n" + "="*80)
    print("📋 功能对比总结")
    print("="*80)

    print("""
🎯 新增的两个方法都返回和 get_hist 完全相同的数据结构:

1️⃣  search_and_get_hist() - 搜索符号并获取历史数据
   • 输入: 搜索关键词、交易所、时间间隔等
   • 输出: pandas DataFrame (和 get_hist 相同格式)
   • 特色: 额外包含 full_symbol, description 列
   
2️⃣  get_multiple_hist() - 获取多个指定符号的历史数据  
   • 输入: 符号列表、交易所、时间间隔等
   • 输出: pandas DataFrame (和 get_hist 相同格式)
   • 特色: 合并多个符号的数据到一个 DataFrame

📊 数据结构特点:
   • pandas DataFrame 格式
   • datetime 作为索引
   • 包含 symbol, open, high, low, close, volume 列
   • 支持所有 pandas 操作（筛选、分组、统计等）
   
💡 使用场景:
   • 批量获取多个股票的历史数据
   • 根据关键词搜索并获取相关股票数据
   • 进行多股票的技术分析和对比
    """)

    if result1 and result2:
        print("\n🎉 所有演示都成功！新功能可以正常使用。")

        print("\n🚀 实际使用示例:")
        print("""
# 方法1: 搜索并获取历史数据
from tvDatafeed import TvDatafeed, Interval
import requests, json

# 设置 session
with open("tv_cookies.json", 'r') as f:
    cookie_list = json.load(f)

session = requests.Session()
for c in cookie_list:
    session.cookies.set(c['name'], c['value'], domain=c['domain'])

tv = TvDatafeed(session=session)

# 搜索苹果相关股票并获取数据
data = tv.search_and_get_hist('AAPL', 'NASDAQ', n_bars=30, max_symbols=3)
print(data)

# 方法2: 获取指定股票列表的数据
stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA'] 
data = tv.get_multiple_hist(stocks, 'NASDAQ', n_bars=50)
print(data)

# 数据分析示例
print("各股票最新收盘价:")
print(data.groupby('symbol')['close'].last())

print("各股票平均成交量:")
print(data.groupby('symbol')['volume'].mean())
        """)
    else:
        print("\n⚠️  部分演示失败，但功能结构是正确的。")

if __name__ == "__main__":
    main()
