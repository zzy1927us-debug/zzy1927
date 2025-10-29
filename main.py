# Disclaimer: This script is for internal testing and educational purposes only and should not be used as the basis for real investment decisions.

import asyncio
import os
import pandas as pd
import ccxt
from ai_decision import DeepSeekClient

# Standard prompt template for DeepSeek suggestions.
# You can modify the custom_prompt argument when calling get_suggestion to include additional context.
PROMPT_TEMPLATE = "{symbol} market trend: {trend}. {custom_prompt} Should I BUY or SELL? Answer only BUY or SELL."

def fetch_ohlcv(exchange_id: str, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch historical OHLCV data using ccxt.
    """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

async def get_suggestion(symbol: str, timeframe: str, custom_prompt: str = "") -> None:
    """
    Provide a buy/sell suggestion based on recent price trends and a custom prompt.
    This function does not execute any trades; it only prints the suggestion.

    Args:
        symbol: Trading pair symbol, e.g. "BTC/USDT".
        timeframe: Candle timeframe, e.g. "1h" or "1d".
        custom_prompt: Additional descriptive text to guide DeepSeek. Keep it concise and clear.
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    deepseek_client = DeepSeekClient(api_key)

    # Fetch recent market data from OKX
    df = fetch_ohlcv("okx", symbol, timeframe, limit=60)
    window = df.iloc[-50:]
    trend = "uptrend" if window["close"].iloc[-1] > window["close"].iloc[0] else "downtrend"

    # Use the standard prompt template to construct the prompt for DeepSeek
    prompt = PROMPT_TEMPLATE.format(symbol=symbol, trend=trend, custom_prompt=custom_prompt)
    try:
        suggestion = await deepseek_client.generate_signal(prompt)
        print(f"[{df['datetime'].iloc[-1]}] Suggested action: {suggestion}")
    except Exception as e:
        print("Error calling DeepSeek:", e)

if __name__ == "__main__":
    # Example usage: get a suggestion for BTC/USDT on a 1-hour timeframe.
    # Modify symbol, timeframe, and custom_prompt as needed. For example:
    # asyncio.run(get_suggestion("ETH/USDT", "1h", custom_prompt="I prefer momentum trading."))
    asyncio.run(get_suggestion("BTC/USDT", "1h"))
