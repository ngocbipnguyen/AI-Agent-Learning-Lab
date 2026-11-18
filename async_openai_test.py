
import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

async def ask_ai(client, question):
    response = await client.responses.create(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        input=question
    )

    return response.output_text


async def main():
    async with AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    ) as client:

        results = await asyncio.gather(
        ask_ai(client, "AI Agent là gì?"),
        ask_ai(client, "CrewAI là gì?"),
        ask_ai(client, "Python Async/Await là gì?"),
        return_exceptions=True
    )

    for i, result in enumerate(results, start=1):
        print(f"\n=== CÂU TRẢ LỜI {i} ===")

        if isinstance(result, Exception):
            print(f"Lỗi: {result}")
        else:
            print(result)

asyncio.run(main())
