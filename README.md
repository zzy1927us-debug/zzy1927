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

## Disclaimer

This project is for educational and backtesting purposes only. It does not execute real trades and should not be used for financial advice or actual investment decisions.
