# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import akshare as ak
import mplfinance as mpf
import pandas as pd


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

    stock_us_daily_df = ak.stock_zh_a_hist(symbol="601012", adjust="qfq",
                                           start_date="2021-07-01", end_date="2021-07-30")
    stock_us_daily_df.index = pd.to_datetime(stock_us_daily_df["日期"])
    stock_us_daily_df = stock_us_daily_df[["开盘", "最高", "最低", "收盘", "成交额"]]
    stock_us_daily_df.columns = ["开盘", "最高", "最低", "收盘", "成交额"]
    stock_us_daily_df.index.name = "日期"
    mpf.plot(stock_us_daily_df, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=False,
             columns=["开盘", "最高", "最低", "收盘", "成交额"])


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
