# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import akshare as ak
import mplfinance as mpf

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

    stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
    stock_us_daily_df = stock_us_daily_df[["open", "high", "low", "close", "volume"]]
    stock_us_daily_df.columns = ["Open", "High", "Low", "Close", "Volume"]
    stock_us_daily_df.index.name = "Date"
    stock_us_daily_df = stock_us_daily_df["2020-04-01": "2020-04-29"]
    mpf.plot(stock_us_daily_df, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=False)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
