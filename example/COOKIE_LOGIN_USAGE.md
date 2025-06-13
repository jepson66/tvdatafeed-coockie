# 🍪 **TvDatafeed Cookie 登录使用指南**

> 这个版本的 TvDatafeed 支持通过 Cookie 登录 TradingView，可以绕过验证码限制。

## 📋 **支持的认证方式**

1. **Cookie 字典** - 直接传入 cookie 字典
2. **Cookie 文件** - 从 JSON 文件加载 cookie
3. **预配置 Session** - 传入已配置的 requests.Session 对象
4. **传统登录** - 用户名密码 (原有方式)
5. **匿名访问** - 无需登录 (功能受限)

---

## 🔧 **使用方法**

### **1. Cookie 字典方式 (推荐)**

```python
from tvDatafeed import TvDatafeed, Interval

# 方式1: 简单的 cookie 字典
cookies = {
    'sessionid': 'your_session_id_here',
    'auth_token': 'your_auth_token_here',
    # 可以添加其他必要的 cookie
}

tv = TvDatafeed(cookies=cookies)
data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_1_hour, 100)
print(data)
```

### **2. Cookie 文件方式**

#### **方式 A: 浏览器导出格式**

```json
[
  {
    "name": "sessionid",
    "value": "your_session_value",
    "domain": ".tradingview.com"
  },
  {
    "name": "auth_token",
    "value": "your_token_value",
    "domain": ".tradingview.com"
  }
]
```

```python
from tvDatafeed import TvDatafeed, Interval

# 从文件加载 cookies
tv = TvDatafeed(cookies_file='tv_cookies.json')
data = tv.get_hist('BTCUSDT', 'BINANCE', Interval.in_1_hour, 100)
```

#### **方式 B: 简化字典格式**

```json
{
  "sessionid": "your_session_value",
  "auth_token": "your_token_value"
}
```

### **3. 预配置 Session 方式 (高级用户)**

```python
import requests
from tvDatafeed import TvDatafeed, Interval

# 创建并配置 session
session = requests.Session()

# 添加 cookies
cookies = {
    'sessionid': 'your_session_id',
    'auth_token': 'your_auth_token'
}
session.cookies.update(cookies)

# 添加代理 (可选)
session.proxies = {
    'http': 'http://proxy:8080',
    'https': 'https://proxy:8080'
}

# 自定义 headers (可选)
session.headers.update({
    'User-Agent': 'Custom User Agent'
})

# 使用预配置的 session
tv = TvDatafeed(session=session)
data = tv.get_hist('ETHUSDT', 'BINANCE', Interval.in_daily, 365)
```

### **4. 传统方式 (向后兼容)**

```python
from tvDatafeed import TvDatafeed, Interval

# 用户名密码登录 (可能遇到验证码)
tv = TvDatafeed(username='your_username', password='your_password')

# 匿名访问 (功能受限)
tv = TvDatafeed()
```

---

## 🍪 **如何获取 Cookie**

### **方法 1: 浏览器开发者工具**

1. 登录 TradingView
2. 按 `F12` 打开开发者工具
3. 进入 `Application` 标签页
4. 点击左侧 `Cookies` → `https://www.tradingview.com`
5. 找到并复制 `sessionid`、`auth_token` 等 cookie 值

### **方法 2: 浏览器插件导出**

1. 安装 "Cookie Editor" 或类似插件
2. 在 TradingView 页面点击插件图标
3. 选择导出为 JSON 格式
4. 保存到文件供程序使用

---

## 🚨 **注意事项**

### **Cookie 安全**

- ⚠️ **不要分享你的 cookie 文件**，它包含登录凭据
- 🔒 将 cookie 文件添加到 `.gitignore`
- 📝 定期更新 cookie (通常 30 天有效期)

### **错误处理**

```python
from tvDatafeed import TvDatafeed, Interval
import logging

# 开启日志查看详细信息
logging.basicConfig(level=logging.INFO)

try:
    tv = TvDatafeed(cookies_file='cookies.json')
    data = tv.get_hist('AAPL', 'NASDAQ', Interval.in_1_hour, 100)
    print("✅ 登录成功")
except FileNotFoundError:
    print("❌ Cookie 文件未找到")
except ValueError as e:
    print(f"❌ Cookie 格式错误: {e}")
except Exception as e:
    print(f"❌ 其他错误: {e}")
```

---

## 📊 **完整示例**

```python
from tvDatafeed import TvDatafeed, TvDatafeedLive, Interval
import pandas as pd

def main():
    # Cookie 登录
    cookies = {
        'sessionid': 'your_session_id',
        'auth_token': 'your_auth_token'
    }

    # 创建 TvDatafeed 实例
    tv = TvDatafeed(cookies=cookies)

    # 获取历史数据
    print("🔄 获取 AAPL 历史数据...")
    aapl_data = tv.get_hist(
        symbol='AAPL',
        exchange='NASDAQ',
        interval=Interval.in_1_hour,
        n_bars=100
    )
    print(f"✅ 获取到 {len(aapl_data)} 条 AAPL 数据")
    print(aapl_data.head())

    # 搜索符号
    print("\n🔍 搜索 Bitcoin 相关符号...")
    search_results = tv.search_symbol('BITCOIN', 'BINANCE')
    for result in search_results[:5]:  # 显示前5个结果
        print(f"- {result.get('symbol')} ({result.get('exchange')})")

    # 实时数据 (TvDatafeedLive)
    print("\n🔴 启动实时数据监控...")
    tvl = TvDatafeedLive(cookies=cookies)

    def data_callback(seis, data):
        print(f"🔄 {seis.symbol} 新数据: Close={data.close[0]:.2f}")

    # 创建监控
    seis = tvl.new_seis('ETHUSDT', 'BINANCE', Interval.in_1_minute)
    consumer = tvl.new_consumer(seis, data_callback)

    print("✅ 实时监控已启动，按 Ctrl+C 停止")

if __name__ == "__main__":
    main()
```

---

## 🔧 **故障排除**

### **常见问题**

1. **Cookie 无效**

   ```
   ❌ Cookie validation failed
   ```

   - 解决: 重新登录 TradingView 并获取新的 cookie

2. **文件格式错误**

   ```
   ❌ Invalid JSON in cookies file
   ```

   - 解决: 检查 JSON 格式是否正确

3. **网络问题**
   ```
   ❌ Connection timeout
   ```
   - 解决: 检查网络连接或使用代理

### **调试模式**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

tv = TvDatafeed(cookies_file='cookies.json')
# 将显示详细的登录和请求日志
```

---

## 🆚 **认证方式优先级**

当多个认证参数同时提供时，优先级如下：

1. `session` (最高优先级)
2. `cookies_file`
3. `cookies`
4. `username` + `password`
5. 匿名访问 (最低优先级)

---

**🎉 现在你可以稳定地访问 TradingView 数据，无需担心验证码问题！**
