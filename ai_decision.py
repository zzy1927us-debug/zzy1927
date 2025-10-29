import asyncio
import aiohttp
import os

class DeepSeekClient:
    """
    示例 DeepSeek API 客户端。
    通过异步方式调用 DeepSeek API，根据市场行情和上下文生成买入/卖出信号。
    请将 DEEPSEEK_API_KEY 替换为真实密钥。
    """

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url

    async def generate_signal(self, prompt: str) -> str:
        """
        调用 DeepSeek API 生成交易信号。
        :param prompt: 用于模型的提示，例如“BTC/USDT 下一步是买入还是卖出？请仅回答 BUY 或 SELL”。
        :return: 返回模型回答的字符串。
        """
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai",      # 根据 API 文档选择模型
            "prompt": prompt,
            "max_tokens": 5,
            "temperature": 0.0
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(f"DeepSeek API error: {resp.status} {text}")
                data = await resp.json()
                return data["choices"][0]["message"]["content"].strip()

async def example():
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    client = DeepSeekClient(api_key)
    # 示例提示：可将历史数据特征、技术指标拼接到 prompt 中
    prompt = "BTC/USDT market trend: uptrend with increasing volume. Should I BUY or SELL? Answer only BUY or SELL."
    signal = await client.generate_signal(prompt)
    print("AI signal:", signal)

if __name__ == "__main__":
    asyncio.run(example())
