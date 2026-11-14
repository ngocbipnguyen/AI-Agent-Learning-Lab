
import json
from memory import ConversationMemory

# Tạo dữ liệu JSON có role không hợp lệ
test_data = [
    {
        "role": "admin",
        "content": "Tin nhắn không hợp lệ."
    }
]

with open("memory_test_invalid_role.json", "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

# Khởi tạo Memory để kiểm tra dữ liệu
memory = ConversationMemory(
    file_path="memory_test_invalid_role.json"
)

print("=== INVALID ROLE TEST ===")
print("Số tin nhắn được tải:", len(memory.get_messages()))
print("Dữ liệu Memory:", memory.get_messages())
