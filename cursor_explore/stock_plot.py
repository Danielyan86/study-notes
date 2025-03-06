import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tushare as ts
import os
import sys
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates

# =====================================================================
# 在这里设置您的Tushare token（如果有）
# 您可以在 https://tushare.pro/ 注册并获取token
# 注册后，在个人中心页面可以找到您的token
# 如果不设置，脚本将使用模拟数据
TUSHARE_TOKEN = ""  # 请在引号中填入您的token
# =====================================================================


# 设置中文字体支持
def set_chinese_font():
    # 直接设置matplotlib参数，这是最可靠的方法
    plt.rcParams["font.sans-serif"] = [
        "SimHei",
        "Heiti TC",
        "STHeiti",
        "Arial Unicode MS",
        "Microsoft YaHei",
        "WenQuanYi Zen Hei",
        "PingFang SC",
        "Hiragino Sans GB",
        "Noto Sans CJK SC",
        "Source Han Sans CN",
    ]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

    # 检查系统平台
    import platform

    system = platform.system()

    # 尝试查找系统中的中文字体
    if system == "Windows":
        # Windows系统
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simkai.ttf",  # 楷体
        ]
    elif system == "Darwin":  # macOS
        # macOS系统常见中文字体路径
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Microsoft/SimHei.ttf",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
    else:  # Linux
        # Linux系统常见中文字体路径
        font_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ]

    # 尝试找到可用的中文字体
    for path in font_paths:
        if os.path.exists(path):
            print(f"找到中文字体: {path}")
            return FontProperties(fname=path)

    # 如果找不到系统字体，尝试使用matplotlib内置字体
    print("未找到系统中文字体，使用matplotlib内置字体设置")

    # 列出所有可用字体
    from matplotlib.font_manager import findSystemFonts, FontManager

    font_manager = FontManager()
    font_list = font_manager.ttflist

    # 查找包含"Hei"、"Kai"、"Song"、"Yuan"、"Ming"等关键词的字体，这些通常是中文字体
    chinese_fonts = [
        f.name
        for f in font_list
        if any(
            keyword in f.name
            for keyword in [
                "Hei",
                "Kai",
                "Song",
                "Yuan",
                "Ming",
                "Han",
                "Gothic",
                "SimSun",
                "SimHei",
                "Microsoft YaHei",
            ]
        )
    ]

    if chinese_fonts:
        print(f"找到可能的中文字体: {', '.join(chinese_fonts[:5])}")
        plt.rcParams["font.sans-serif"] = (
            chinese_fonts + plt.rcParams["font.sans-serif"]
        )

    return None


# 生成模拟数据的函数
def generate_sample_stock_data(start_price, volatility, trend=0):
    # 生成2024年的日期（1月1日至今）
    start_date = datetime(2024, 1, 1)
    end_date = datetime.now()
    date_range = pd.date_range(
        start=start_date, end=end_date, freq="B"
    )  # 'B'表示工作日

    # 生成带有一定随机性和趋势的价格数据
    n_days = len(date_range)
    prices = [start_price]

    for i in range(1, n_days):
        # 带趋势的随机每日变化
        daily_change = np.random.normal(trend, volatility)
        # 确保价格不低于1
        new_price = max(1, prices[-1] * (1 + daily_change / 100))
        prices.append(new_price)

    # 创建DataFrame
    df = pd.DataFrame({"Date": date_range, "Close": prices})
    df.set_index("Date", inplace=True)

    return df


# 计算年初至今涨幅
def calculate_ytd_performance(data):
    if len(data) < 2:
        return 0

    first_price = data.iloc[0]
    last_price = data.iloc[-1]
    return (last_price - first_price) / first_price * 100


# 主函数
def main():
    # 设置中文字体
    chinese_font = set_chinese_font()

    # 检查是否提供了token
    token = TUSHARE_TOKEN or os.environ.get("TUSHARE_TOKEN", None)

    if not token:
        print("警告: 未找到Tushare API token")
        print("请通过以下方式设置token:")
        print("1. 在脚本顶部的TUSHARE_TOKEN变量中直接设置")
        print("2. 设置环境变量 TUSHARE_TOKEN")
        print("3. 在命令行运行时提供参数: python stock_plot.py your_token")
        print("\n您可以在 https://tushare.pro/ 注册并获取token")

        # 检查命令行参数
        if len(sys.argv) > 1:
            token = sys.argv[1]
            print(
                f"使用命令行提供的token: {token[:4]}{'*' * (len(token)-8)}{token[-4:]}"
            )
        else:
            print("\n由于没有提供token，将使用模拟数据生成图表")
            use_sample_data(chinese_font)
            return

    # 设置Tushare API
    try:
        ts.set_token(token)
        pro = ts.pro_api()

        # 定义股票代码
        # 兴业银行: 601166.SH
        # 招商银行: 600036.SH
        stock_codes = {"601166.SH": "兴业银行", "600036.SH": "招商银行"}

        # 设置时间范围
        start_date = "20240101"  # 格式：YYYYMMDD
        end_date = datetime.now().strftime("%Y%m%d")

        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 8))

        has_data = False
        performance_data = {}

        # 获取并绘制每只股票的数据
        for code, name in stock_codes.items():
            try:
                # 获取股票数据
                df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)

                if not df.empty:
                    # 数据按日期排序
                    df = df.sort_values("trade_date")
                    # 将日期转换为datetime格式
                    df["trade_date"] = pd.to_datetime(df["trade_date"])

                    # 绘制收盘价
                    ax.plot(df["trade_date"], df["close"], label=name, linewidth=2)
                    print(f"成功获取 {name} ({code}) 的数据")

                    # 计算年初至今涨幅
                    ytd_performance = calculate_ytd_performance(df["close"])
                    performance_data[name] = {
                        "ytd": ytd_performance,
                        "start_price": df["close"].iloc[0],
                        "current_price": df["close"].iloc[-1],
                        "max_price": df["close"].max(),
                        "min_price": df["close"].min(),
                    }

                    has_data = True
                else:
                    print(f"没有找到 {name} ({code}) 的数据")
                    # 使用模拟数据作为备选
                    sample_data = use_sample_data_for_stock(code, name, ax)

                    # 计算模拟数据的年初至今涨幅
                    ytd_performance = calculate_ytd_performance(sample_data["Close"])
                    performance_data[name + " (模拟数据)"] = {
                        "ytd": ytd_performance,
                        "start_price": sample_data["Close"].iloc[0],
                        "current_price": sample_data["Close"].iloc[-1],
                        "max_price": sample_data["Close"].max(),
                        "min_price": sample_data["Close"].min(),
                    }

                    has_data = True

            except Exception as e:
                print(f"获取 {name} ({code}) 数据时出错: {str(e)}")
                # 使用模拟数据作为备选
                sample_data = use_sample_data_for_stock(code, name, ax)

                # 计算模拟数据的年初至今涨幅
                ytd_performance = calculate_ytd_performance(sample_data["Close"])
                performance_data[name + " (模拟数据)"] = {
                    "ytd": ytd_performance,
                    "start_price": sample_data["Close"].iloc[0],
                    "current_price": sample_data["Close"].iloc[-1],
                    "max_price": sample_data["Close"].max(),
                    "min_price": sample_data["Close"].min(),
                }

                has_data = True

        if has_data:
            # 自定义图表
            if chinese_font:
                ax.set_title(
                    "兴业银行 vs 招商银行股价对比 (2024)",
                    fontsize=16,
                    fontproperties=chinese_font,
                )
                ax.set_xlabel("日期", fontsize=14, fontproperties=chinese_font)
                ax.set_ylabel("股价 (人民币)", fontsize=14, fontproperties=chinese_font)
                ax.legend(fontsize=12, prop=chinese_font)
            else:
                ax.set_title("兴业银行 vs 招商银行股价对比 (2024)", fontsize=16)
                ax.set_xlabel("日期", fontsize=14)
                ax.set_ylabel("股价 (人民币)", fontsize=14)
                ax.legend(fontsize=12)

            ax.grid(True, linestyle="--", alpha=0.7)

            # 设置x轴日期格式
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))

            # 旋转x轴标签以提高可读性
            plt.xticks(rotation=45)

            # 添加年初至今涨幅文本框
            textstr = "年初至今涨幅:\n"
            for name, data in performance_data.items():
                textstr += f"{name}: {data['ytd']:.2f}%\n"
                textstr += f"  起始价: {data['start_price']:.2f}, 当前价: {data['current_price']:.2f}\n"
                textstr += f"  最高价: {data['max_price']:.2f}, 最低价: {data['min_price']:.2f}\n"

            # 放置文本框
            props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
            if chinese_font:
                ax.text(
                    0.02,
                    0.02,
                    textstr,
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment="bottom",
                    bbox=props,
                    fontproperties=chinese_font,
                )
            else:
                ax.text(
                    0.02,
                    0.02,
                    textstr,
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment="bottom",
                    bbox=props,
                )

            # 调整布局以防止标签被截断
            plt.tight_layout()

            # 保存图表到本地
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bank_stocks_comparison_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"图表已保存为: {filename}")

            # 显示图表
            plt.show()
        else:
            print("没有数据可以绘制")
            use_sample_data(chinese_font)

    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("使用模拟数据生成图表")
        use_sample_data(chinese_font)


# 为单只股票使用模拟数据
def use_sample_data_for_stock(code, name, ax=None):
    if code == "601166.SH":
        sample_data = generate_sample_stock_data(18.5, 1.2, 0.02)
    else:
        sample_data = generate_sample_stock_data(35.8, 1.0, 0.03)

    if ax is not None:
        ax.plot(
            sample_data.index,
            sample_data["Close"],
            label=f"{name} (模拟数据)",
            linewidth=2,
            linestyle="--",
        )

    print(f"使用模拟数据替代 {name}")
    return sample_data


# 使用模拟数据生成完整图表
def use_sample_data(chinese_font=None):
    # 生成两家银行的模拟数据
    # 参数: 起始价格, 波动率(%), 趋势(每日%)
    industrial_bank_data = generate_sample_stock_data(18.5, 1.2, 0.02)  # 兴业银行
    merchants_bank_data = generate_sample_stock_data(35.8, 1.0, 0.03)  # 招商银行

    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 8))

    # 绘制每家银行的数据
    ax.plot(
        industrial_bank_data.index,
        industrial_bank_data["Close"],
        label="兴业银行 (模拟数据)",
        linewidth=2,
    )
    ax.plot(
        merchants_bank_data.index,
        merchants_bank_data["Close"],
        label="招商银行 (模拟数据)",
        linewidth=2,
    )

    # 计算年初至今涨幅
    ind_ytd = calculate_ytd_performance(industrial_bank_data["Close"])
    mer_ytd = calculate_ytd_performance(merchants_bank_data["Close"])

    # 自定义图表
    if chinese_font:
        ax.set_title(
            "兴业银行 vs 招商银行股价对比 (2024) - 模拟数据",
            fontsize=16,
            fontproperties=chinese_font,
        )
        ax.set_xlabel("日期", fontsize=14, fontproperties=chinese_font)
        ax.set_ylabel("股价 (人民币)", fontsize=14, fontproperties=chinese_font)
        ax.legend(fontsize=12, prop=chinese_font)
    else:
        ax.set_title("兴业银行 vs 招商银行股价对比 (2024) - 模拟数据", fontsize=16)
        ax.set_xlabel("日期", fontsize=14)
        ax.set_ylabel("股价 (人民币)", fontsize=14)
        ax.legend(fontsize=12)

    ax.grid(True, linestyle="--", alpha=0.7)

    # 设置x轴日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))

    # 旋转x轴标签以提高可读性
    plt.xticks(rotation=45)

    # 添加年初至今涨幅文本框
    textstr = "年初至今涨幅 (模拟数据):\n"
    textstr += f"兴业银行: {ind_ytd:.2f}%\n"
    textstr += f"  起始价: {industrial_bank_data['Close'].iloc[0]:.2f}, 当前价: {industrial_bank_data['Close'].iloc[-1]:.2f}\n"
    textstr += f"  最高价: {industrial_bank_data['Close'].max():.2f}, 最低价: {industrial_bank_data['Close'].min():.2f}\n"
    textstr += f"招商银行: {mer_ytd:.2f}%\n"
    textstr += f"  起始价: {merchants_bank_data['Close'].iloc[0]:.2f}, 当前价: {merchants_bank_data['Close'].iloc[-1]:.2f}\n"
    textstr += f"  最高价: {merchants_bank_data['Close'].max():.2f}, 最低价: {merchants_bank_data['Close'].min():.2f}\n"

    # 放置文本框
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    if chinese_font:
        ax.text(
            0.02,
            0.02,
            textstr,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="bottom",
            bbox=props,
            fontproperties=chinese_font,
        )
    else:
        ax.text(
            0.02,
            0.02,
            textstr,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="bottom",
            bbox=props,
        )

    # 调整布局以防止标签被截断
    plt.tight_layout()

    # 保存图表到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bank_stocks_comparison_sample_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"图表已保存为: {filename}")

    # 显示图表
    plt.show()

    # 打印关于数据的说明
    print("注意：此图表使用模拟数据生成。")
    print("实际股价数据可能与此图表有显著差异。")


# 程序入口
if __name__ == "__main__":
    main()
