
from memory import ConversationMemory

memory = ConversationMemory(max_messages=5, max_tokens=20)

# Xóa dữ liệu cũ để kiểm thử
memory.clear()

# Thêm 2 tin nhắn
memory.add_message("user", "Xin chào")
memory.add_message("assistant", "Chào bạn!")

# Lấy thống kê
stats = memory.get_stats()

print("=== MEMORY STATISTICS ===")
print("Tổng số tin nhắn:", stats["total_messages"])
print("Giới hạn tin nhắn:", stats["max_messages"])
print("Số chỗ còn lại:", stats["remaining_slots"])
print("Tổng số Token:", stats["total_tokens"])
print("Giới hạn Token:", stats["max_tokens"])
print("Số Token còn lại:", stats["remaining_tokens"])
