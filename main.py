
import json
from openai import OpenAI
from dotenv import load_dotenv

from tools.calculator import calculator
from tools.search_news import search_news
from memory import ConversationMemory
# 1. Đọc API Key từ file .env
load_dotenv(override=True)
client = OpenAI()

# 2. Khai báo công cụ cho AI
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Thực hiện phép tính cộng, trừ, nhân, chia hai số.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Phép tính cần thực hiện."
                    },
                    "a": {
                        "type": "number",
                        "description": "Số thứ nhất."
                    },
                    "b": {
                        "type": "number",
                        "description": "Số thứ hai."
                    }
                },
                "required": ["operation", "a", "b"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "Tìm kiếm tin tức mới nhất trên Internet theo chủ đề người dùng yêu cầu.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Chủ đề tin tức cần tìm kiếm."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Số lượng kết quả tin tức tối đa."
                    }
                },
                "required": ["query", "max_results"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]


# 3. Khởi tạo bộ nhớ hội thoại
memory = ConversationMemory()

# 4. Vòng lặp hội thoại
while True:

    user_input = input("\nBạn: ").strip()

    # Kiểm tra lệnh thoát
    if user_input.lower() in ["exit", "quit", "thoat", "thoát"]:
        print("AI: Tạm biệt! Hẹn gặp lại.")
        break

    if not user_input:
        continue

    # Lưu câu hỏi người dùng
    memory.add_message("user", user_input)

    messages = [
        {
            "role": "system",
            "content": """
            Bạn là trợ lý AI thông minh.

            Quy tắc sử dụng công cụ:
            - Khi người dùng yêu cầu tính toán, hãy sử dụng Calculator Tool.
            - Khi người dùng yêu cầu tìm kiếm tin tức, hãy sử dụng News Search Tool.
            - Khi người dùng trò chuyện hoặc hỏi kiến thức thông thường, hãy trả lời trực tiếp.
            - Không được tự bịa tin tức. Chỉ trình bày tin tức dựa trên kết quả từ News Search Tool.
            """
        }
    ]

    # Đưa lịch sử hội thoại vào messages
    messages.extend(memory.get_messages())

    # 5. Gửi yêu cầu đến AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # 6. Kiểm tra AI có yêu cầu gọi công cụ không
    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    if assistant_message.tool_calls:

        for tool_call in assistant_message.tool_calls:

            arguments = json.loads(tool_call.function.arguments)

            # Calculator Tool
            if tool_call.function.name == "calculator":

                print("\n[AI yêu cầu gọi Calculator Tool]")
                print("Tham số:", arguments)

                result = calculator(**arguments)

                tool_result = {"result": result}

                print("[Calculator trả kết quả]:", result)

            # News Search Tool
            elif tool_call.function.name == "search_news":

                print("\n[AI yêu cầu gọi News Search Tool]")
                print("Tham số:", arguments)

                result = search_news(**arguments)

                tool_result = {"results": result}

                print("[News Search trả kết quả]:", result)

            else:
                tool_result = {"error": "Tool không được hỗ trợ."}

            # Gửi kết quả Tool trở lại AI
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    ensure_ascii=False
                )
            })

        # AI tổng hợp kết quả
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        ai_response = final_response.choices[0].message.content

    else:
        ai_response = assistant_message.content

    # Hiển thị câu trả lời
    print("\nAI:", ai_response)

    # Lưu câu trả lời vào Memory
    memory.add_message("assistant", ai_response)
