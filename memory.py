
import json
import os


class ConversationMemory:

    def __init__(self, file_path="memory.json", max_messages=20):
        self.file_path = file_path
        self.max_messages = max_messages
        self.messages = []

        # Tự động tải lịch sử hội thoại khi khởi tạo
        self.load_memory()

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

        # Giới hạn số lượng tin nhắn
        self.messages = self.messages[-self.max_messages:]

        # Tự động lưu sau mỗi tin nhắn
        self.save_memory()

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
        self.save_memory()

    def load_memory(self):
        """Đọc lịch sử hội thoại từ file JSON."""

        if os.path.exists(self.file_path):

            with open(self.file_path, "r", encoding="utf-8") as file:
                self.messages = json.load(file)

    def save_memory(self):
        """Lưu lịch sử hội thoại vào file JSON."""

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.messages,
                file,
                ensure_ascii=False,
                indent=4
            )
    def get_stats(self):
        return {
            "total_messages": len(self.messages),
            "max_messages": self.max_messages,
            "remaining_slots": self.max_messages - len(self.messages)
        }