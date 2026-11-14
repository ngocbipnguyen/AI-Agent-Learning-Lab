from memory import ConversationMemory

# Khởi tạo Memory với giới hạn 50 Token
memory = ConversationMemory(
    max_messages=20,
    max_tokens=20
)

# Xóa lịch sử cũ
memory.clear()

# Thêm 3 tin nhắn
memory.add_message("user", "Tin nhắn thứ nhất.")
memory.add_message("user", "Tin nhắn thứ hai.")
memory.add_message(
    "user",
    "Đây là một tin nhắn rất dài nhằm kiểm tra chức năng giới hạn Token của hệ thống Memory."
)

# Lấy thống kê
print("=== TOKEN CỦA TỪNG TIN NHẮN ===")

texts = [
    "Tin nhắn thứ nhất.",
    "Tin nhắn thứ hai.",
    "Đây là một tin nhắn rất dài nhằm kiểm tra chức năng giới hạn Token của hệ thống Memory."
]

for text in texts:
    print(text)
    print("Tokens:", memory.count_tokens(text))
    print()
    
print("=== TOKEN LIMIT TEST ===")

for message in memory.get_messages():
    print(message["content"])

print("\nTổng số tin nhắn:", len(memory.get_messages()))
print("Tổng số Token:", memory.get_total_tokens())
print("Giới hạn Token:", memory.max_tokens)