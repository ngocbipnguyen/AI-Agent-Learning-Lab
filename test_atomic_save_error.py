
import os
import json
from memory import ConversationMemory

test_file = "memory_test_atomic_error.json"
temp_file = test_file + ".tmp"

# Khởi tạo Memory
memory = ConversationMemory(file_path=test_file)

# Tạo dữ liệu ban đầu trong file JSON chính
original_data = [
    {
        "role": "user",
        "content": "Dữ liệu gốc cần được bảo vệ."
    }
]

with open(test_file, "w", encoding="utf-8") as file:
    json.dump(original_data, file, ensure_ascii=False, indent=4)

# Tạo thư mục có tên trùng với file tạm
# Khi save_memory mở đường dẫn này để ghi, thao tác sẽ thất bại.
os.mkdir(temp_file)

print("=== ATOMIC SAVE ERROR TEST ===")

# Thử lưu dữ liệu mới
memory.add_message("user", "Dữ liệu mới.")

# Đọc lại file JSON chính
with open(test_file, "r", encoding="utf-8") as file:
    saved_data = json.load(file)

print("Dữ liệu gốc còn nguyên:", saved_data == original_data)
print("Dữ liệu trong file:", saved_data)
print("Dữ liệu trong RAM:", memory.get_messages())

# Dọn thư mục giả lập file tạm
os.rmdir(temp_file)
