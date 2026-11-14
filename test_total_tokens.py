from memory import ConversationMemory

# Khởi tạo Memory
memory = ConversationMemory(max_messages=20, max_tokens=1000)

# Xóa lịch sử cũ
memory.clear()

# Thêm 3 tin nhắn
memory.add_message("user", "Xin chào")
memory.add_message("assistant", "Chào bạn!")
memory.add_message("user", "Tôi đang học AI Agent bằng Python.")

# Tính tổng Token
total = memory.get_total_tokens()

print("=== TOTAL TOKENS ===")
print("Số lượng tin nhắn:", len(memory.get_messages()))
print("Tổng số Token:", total)