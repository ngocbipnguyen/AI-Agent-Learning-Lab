from memory import ConversationMemory

# Khởi tạo Memory với giới hạn 5 tin nhắn
memory = ConversationMemory(max_messages=5)

# Xóa lịch sử cũ
memory.clear()

# Thêm 3 tin nhắn thử nghiệm
memory.add_message("user", "Xin chào")
memory.add_message("assistant", "Chào bạn!")
memory.add_message("user", "Tôi đang học AI Agent")

# Lấy thống kê Memory
stats = memory.get_stats()

print("=== MEMORY STATISTICS ===")
print("Tổng số tin nhắn:", stats["total_messages"])
print("Giới hạn tối đa:", stats["max_messages"])
print("Số vị trí còn trống:", stats["remaining_slots"])