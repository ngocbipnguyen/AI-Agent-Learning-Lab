
from memory import ConversationMemory
import json

# Tạo dữ liệu JSON có một tin nhắn không hợp lệ
test_data = [
    {"role": "user", "content": "Xin chào"},
    {"invalid": "data"}
]

with open("memory_test_error.json", "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

# Khởi tạo Memory
memory = ConversationMemory(
    file_path="memory_test_error.json"
)

print("=== MEMORY STRUCTURE TEST ===")
print("Số tin nhắn:", len(memory.get_messages()))
print("Dữ liệu Memory:", memory.get_messages())
