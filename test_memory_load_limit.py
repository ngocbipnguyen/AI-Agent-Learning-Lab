
import json
from memory import ConversationMemory

# Tạo dữ liệu gồm 8 tin nhắn
test_data = []

for i in range(1, 9):
    test_data.append({
        "role": "user",
        "content": f"Tin nhắn thứ {i}"
    })

# Lưu dữ liệu vào file JSON riêng
with open("memory_test_limit.json", "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

# Khởi tạo Memory với giới hạn 5 tin nhắn
memory = ConversationMemory(
    file_path="memory_test_limit.json",
    max_messages=5,
    max_tokens=1000
)

# Hiển thị kết quả
print("=== MEMORY LOAD LIMIT TEST ===")

for message in memory.get_messages():
    print(message["content"])

stats = memory.get_stats()

print("Tổng số tin nhắn:", stats["total_messages"])
print("Giới hạn tin nhắn:", stats["max_messages"])
print("Tổng Token:", stats["total_tokens"])
