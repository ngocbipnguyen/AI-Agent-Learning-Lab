
import json
from memory import ConversationMemory

memory = ConversationMemory(
    file_path="memory_test_clear.json",
    max_messages=20,
    max_tokens=1000
)

# Thêm dữ liệu kiểm thử
memory.add_message("user", "Xin chào")
memory.add_message("assistant", "Chào bạn!")

print("=== BEFORE CLEAR ===")
print(memory.get_stats())

# Xóa lịch sử
memory.clear()

print("\n=== AFTER CLEAR ===")
print(memory.get_stats())

# Kiểm tra dữ liệu trong JSON
with open("memory_test_clear.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("\n=== JSON FILE ===")
print(data)
