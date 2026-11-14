
from memory import ConversationMemory

memory = ConversationMemory(
    file_path="memory_test_validation.json",
    max_messages=20,
    max_tokens=1000
)

print("=== ADD MESSAGE VALIDATION TEST ===")

test_cases = [
    ("user", "Xin chào"),
    ("admin", "Tin nhắn không hợp lệ"),
    ("", "Role rỗng"),
    ("user", ""),
    (123, "Role sai kiểu dữ liệu"),
    ("user", 123)
]

for role, content in test_cases:
    try:
        memory.add_message(role, content)
        print("Chấp nhận:", role, content)

    except (TypeError, ValueError) as error:
        print("Từ chối:", error)

print("\n=== KẾT QUẢ ===")
print("Số tin nhắn hợp lệ:", len(memory.get_messages()))

for message in memory.get_messages():
    print(message)
