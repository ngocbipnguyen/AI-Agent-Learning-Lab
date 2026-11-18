
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

print("OpenAI API Key:", "Đã cấu hình" if openai_api_key else "Chưa cấu hình")
print("Tavily API Key:", "Đã cấu hình" if tavily_api_key else "Chưa cấu hình")
print("Model:", model_name)
