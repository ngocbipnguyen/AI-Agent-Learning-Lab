
import json
from memory import ConversationMemory

# Tạo dữ liệu JSON có content rỗng
test_data = [
    {
        "role": "user",
        "content": ""
    }
]

with open("memory_test_empty_content.json", "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

# Khởi tạo Memory
memory = ConversationMemory(
    file_path="memory_test_empty_content.json"
)

print("=== EMPTY CONTENT TEST ===")
print("Số tin nhắn được tải:", len(memory.get_messages()))
print("Dữ liệu Memory:", memory.get_messages())
