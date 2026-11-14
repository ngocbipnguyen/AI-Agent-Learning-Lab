
from memory import ConversationMemory

memory = ConversationMemory(
    file_path="memory_test_get_messages.json"
)

# Thêm dữ liệu thử nghiệm
memory.add_message("user", "Tôi đang học Python.")
memory.add_message("assistant", "Chúng ta đang học Memory.")

# Lấy danh sách tin nhắn
messages = memory.get_messages()

# Thử xóa dữ liệu bên ngoài
messages.clear()

print("=== GET MESSAGES TEST ===")
print("Dữ liệu bên ngoài:", messages)
print("Dữ liệu bên trong Memory:", memory.messages)

print("Số tin nhắn còn lại:", len(memory.messages))
