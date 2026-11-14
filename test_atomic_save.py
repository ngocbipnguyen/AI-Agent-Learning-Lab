
import os
import json
from memory import ConversationMemory

test_file = "memory_test_atomic.json"
temp_file = test_file + ".tmp"

# Khởi tạo Memory
memory = ConversationMemory(file_path=test_file)

# Xóa dữ liệu cũ
memory.clear()

# Thêm tin nhắn
memory.add_message("user", "Kiểm tra Atomic File Write.")

print("=== ATOMIC SAVE TEST ===")

# Kiểm tra file chính
print("File chính tồn tại:", os.path.exists(test_file))

# Kiểm tra file tạm
print("File tạm còn tồn tại:", os.path.exists(temp_file))

# Đọc dữ liệu từ file chính
with open(test_file, "r", encoding="utf-8") as file:
    data = json.load(file)

print("Dữ liệu đã lưu:", data)
print("Số tin nhắn:", len(data))
