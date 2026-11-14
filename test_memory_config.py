
from memory import ConversationMemory

print("=== MEMORY CONFIG TEST ===")

test_cases = [
    {"max_messages": 0, "max_tokens": 1000},
    {"max_messages": -5, "max_tokens": 1000},
    {"max_messages": 20, "max_tokens": -100},
    {"max_messages": "20", "max_tokens": 1000},
    {"max_messages": 20, "max_tokens": "1000"}
]

for config in test_cases:
    try:
        memory = ConversationMemory(**config)
        print("Cấu hình hợp lệ:", config)

    except ValueError as error:
        print("Phát hiện lỗi:", error)

# Kiểm tra cấu hình hợp lệ
memory = ConversationMemory(
    max_messages=20,
    max_tokens=1000
)

print("Cấu hình mặc định hợp lệ:", memory.get_stats())
