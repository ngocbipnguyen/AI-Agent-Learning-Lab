
import json
from memory import ConversationMemory

memory = ConversationMemory(
    file_path="memory_test_save.json"
)

# Xóa dữ liệu cũ
memory.clear()

# Thêm dữ liệu tiếng Việt
memory.add_message("user", "Xin chào! Tôi đang học AI Agent.")
memory.add_message("assistant", "Chào bạn! Chúng ta cùng học Python nhé.")

print("=== MEMORY SAVE TEST ===")

# Đọc dữ liệu trực tiếp từ JSON
with open("memory_test_save.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Dữ liệu đã lưu:")
print(json.dumps(data, ensure_ascii=False, indent=4))

print("\nSố tin nhắn:", len(data))
print("Kiểm tra tiếng Việt:", "Xin chào!" in data[0]["content"])
