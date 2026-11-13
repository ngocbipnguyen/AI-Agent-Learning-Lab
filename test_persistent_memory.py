
from memory import ConversationMemory

# Khởi tạo Persistent Memory
memory = ConversationMemory()

# Thêm hội thoại
memory.add_message("user", "Tôi tên là Minh.")
memory.add_message("assistant", "Xin chào Minh!")

print("=== PERSISTENT MEMORY ===")

# Hiển thị lịch sử hội thoại
for message in memory.get_messages():
    print(message["role"], ":", message["content"])

print("\nTổng số tin nhắn:", len(memory.get_messages()))

print("\nĐã lưu dữ liệu vào memory.json")
