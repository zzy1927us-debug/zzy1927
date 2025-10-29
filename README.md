# Auto Trader Simulation
This repository provides a simple backtesting framework for cryptocurrency trading using passivbot as the execution engine and DeepSeek AI for decision making. It is intended for educational purposes and simulation only; do not use it for live trading.

## Contents
- `ai_decision.py`: asynchronous client for DeepSeek API to generate trading signals.
- `main.py`: backtest script fetching historical data via ccxt and simulating trades based on DeepSeek signals.
- `requirements.txt`: Python dependencies.
- `setup.sh`: script to set up environment and install passivbot.
- `Dockerfile`: container recipe to build environment for simulation.
- `docker-compose.yml`: one-click deployment using Docker Compose.

## Quick Start
1. Clone this repository:
```bash
git clone https://github.com/zzy1927us-debug/zzy1927.git
cd zzy1927
```
2. Install dependencies and clone passivbot:
```bash
bash setup.sh
```
3. Set your DeepSeek API key:
```bash
export DEEPSEEK_API_KEY=your_api_key
```
4. Run the backtest:
```bash
python main.py
```
5. Alternatively, build and run using Docker:
```bash
docker build -t ai-passivbot .
docker run -e DEEPSEEK_API_KEY=your_api_key ai-passivbot
```
6. Or use Docker Compose for a one-click deployment:
```bash
docker compose up --build
```

## Using the Prompt Template
This project includes a standard prompt template for DeepSeek suggestions. The template looks like:
```
{symbol} market trend: {trend}. {custom_prompt} Should I BUY or SELL? Answer only BUY or SELL.
```
- **symbol**: the trading pair (e.g., "BTC/USDT").
- **trend**: automatically computed from recent price data (uptrend or downtrend).
- **custom_prompt**: your own phrase describing strategy or preferences, such as "I prefer momentum-based trading" or "Consider RSI and MACD indicators".

To use the template, modify the `custom_prompt` parameter when calling `get_suggestion` in `main.py`. For example:
```python
asyncio.run(get_suggestion("BTC/USDT", "1h", custom_prompt="I prefer momentum-based trading"))
```
This will fetch recent market data, determine the trend, build the full prompt, and print DeepSeek's buy/sell suggestion. The suggestions are for internal testing only and should not be used as investment advice.

## Disclaimer
This project is for educational and backtesting purposes only. It does not execute real trades and should not be used for financial advice or actual investment decisions.
