from memory import ConversationMemory

# Khởi tạo bộ nhớ
memory = ConversationMemory()

# Thêm hội thoại
memory.add_message("user", "Tôi tên là Minh.")
memory.add_message("assistant", "Xin chào Minh!")

# Lấy lịch sử hội thoại
print("=== CONVERSATION MEMORY ===")

for message in memory.get_messages():
    print(message["role"], ":", message["content"])

# Kiểm tra số lượng tin nhắn
print("\nTổng số tin nhắn:", len(memory.get_messages()))