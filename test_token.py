from memory import ConversationMemory

# Khởi tạo Memory
memory = ConversationMemory()

# Văn bản cần đếm
text = "Tôi đang học xây dựng AI Agent bằng Python."

# Đếm Token
total_tokens = memory.count_tokens(text)

print("Nội dung:", text)
print("Tổng số Token:", total_tokens)