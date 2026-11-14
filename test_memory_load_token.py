
import json
from memory import ConversationMemory

# Tạo dữ liệu gồm 3 tin nhắn
test_data = [
    {"role": "user", "content": "Tin nhắn thứ nhất."},
    {"role": "user", "content": "Tin nhắn thứ hai."},
    {
        "role": "user",
        "content": "Đây là một tin nhắn rất dài nhằm kiểm tra chức năng giới hạn Token của hệ thống Memory."
    }
]

# Lưu dữ liệu vào file JSON riêng
with open("memory_test_token.json", "w", encoding="utf-8") as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

# Khởi tạo Memory với giới hạn 20 Token
memory = ConversationMemory(
    file_path="memory_test_token.json",
    max_messages=20,
    max_tokens=20
)

# Hiển thị kết quả
print("=== MEMORY LOAD TOKEN TEST ===")

for message in memory.get_messages():
    print(message["content"])

stats = memory.get_stats()

print("Tổng số tin nhắn:", stats["total_messages"])
print("Tổng Token:", stats["total_tokens"])
print("Giới hạn Token:", stats["max_tokens"])
