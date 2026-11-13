from memory import ConversationMemory

# Tạo Memory với giới hạn 5 tin nhắn
memory = ConversationMemory(max_messages=5)

# Xóa lịch sử cũ để kiểm tra độc lập
memory.clear()

# Thêm 8 tin nhắn
for i in range(1, 9):
    memory.add_message("user", f"Tin nhắn số {i}")

# Hiển thị kết quả
print("=== KIỂM TRA MEMORY LIMIT ===")

for message in memory.get_messages():
    print(message["content"])

print("\nTổng số tin nhắn:", len(memory.get_messages()))