import asyncio
import os
import pandas as pd
import ccxt
from ai_decision import DeepSeekClient


def fetch_ohlcv(exchange_id: str, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
    """
    使用 ccxt 获取历史 K 线数据。
    :param exchange_id: 交易所名称，回测用 'okx'
    :param symbol: 交易对，例如 'BTC/USDT'
    :param timeframe: K 线周期，如 '1h'
    :param limit: 获取的条数
    """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


async def backtest():
    """
    简易回测框架：
    - 获取历史行情
    - 构建 AI 提示并调用 DeepSeek 决策
    - 根据信号模拟持仓和资金曲线
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    deepseek_client = DeepSeekClient(api_key)

    df = fetch_ohlcv("okx", "BTC/USDT", "1h", limit=200)
    initial_balance = 10000.0
    balance = initial_balance
    position = 0  # 当前持仓数量 (正数表示多头，负数为空头)
    trade_size = 0.01  # 假设每次交易 0.01 BTC

    # 遍历历史K线，逐条生成信号并模拟交易
    for i in range(50, len(df)):
        window = df.iloc[i-50:i]  # 最近 50 条数据作为分析窗口
        # 构建简单的描述性 prompt，也可以加入技术指标
        trend = "uptrend" if window["close"].iloc[-1] > window["close"].iloc[0] else "downtrend"
        prompt = f"BTC/USDT market trend: {trend}. Should I BUY or SELL? Answer only BUY or SELL."
        try:
            signal = await deepseek_client.generate_signal(prompt)
        except Exception as e:
            print("Error calling DeepSeek:", e)
            continue

        price = df["close"].iloc[i]
        if signal.upper().startswith("BUY") and balance > trade_size * price:
            # 开多仓
            balance -= trade_size * price
            position += trade_size
            print(f"[{df['datetime'].iloc[i]}] BUY {trade_size} BTC @ {price:.2f}")
        elif signal.upper().startswith("SELL") and position >= trade_size:
            # 平仓
            balance += trade_size * price
            position -= trade_size
            print(f"[{df['datetime'].iloc[i]}] SELL {trade_size} BTC @ {price:.2f}")

    # 回测结束，计算收益
    final_balance = balance + position * df["close"].iloc[-1]
    profit = final_balance - initial_balance
    print(f"Initial balance: {initial_balance}, Final balance: {final_balance:.2f}, Profit: {profit:.2f}")


if __name__ == "__main__":
    asyncio.run(backtest())
