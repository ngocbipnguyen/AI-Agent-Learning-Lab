
import json
import os
import tiktoken

class ConversationMemory:

    
    def __init__(
        self,
        file_path="memory.json",
        max_messages=20,
        max_tokens=1000
    ):
        # Kiểm tra cấu hình
        if not isinstance(max_messages, int) or isinstance(max_messages, bool) or max_messages <= 0:
            raise ValueError("max_messages phải là số nguyên lớn hơn 0.")

        if not isinstance(max_tokens, int) or isinstance(max_tokens, bool) or max_tokens <= 0:
            raise ValueError("max_tokens phải là số nguyên lớn hơn 0.")

        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path phải là chuỗi hợp lệ.")

        self.file_path = file_path
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4o")

        self.messages = []
        self.load_memory()


    
    
    def add_message(self, role: str, content: str):
        # Kiểm tra kiểu dữ liệu
        if not isinstance(role, str):
            raise TypeError("role phải là chuỗi.")

        if not isinstance(content, str):
            raise TypeError("content phải là chuỗi.")

        # Kiểm tra nội dung rỗng
        if not role.strip():
            raise ValueError("role không được để trống.")

        if not content.strip():
            raise ValueError("content không được để trống.")

        # Kiểm tra vai trò hợp lệ
        if role not in ["user", "assistant"]:
            raise ValueError("role chỉ được là 'user' hoặc 'assistant'.")

        # Kiểm tra số Token của tin nhắn mới
        new_message_tokens = self.count_tokens(content)

        # Từ chối nếu tin nhắn mới vượt giới hạn
        if new_message_tokens > self.max_tokens:
            print("Tin nhắn vượt quá giới hạn Token, không được lưu.")
            return

        self.messages.append({"role": role, "content": content})

        # Giới hạn số lượng tin nhắn
        self.messages = self.messages[-self.max_messages:]

        # Giới hạn tổng số Token
        while self.messages and self.get_total_tokens() > self.max_tokens:
            self.messages.pop(0)

        self.save_memory()



    def get_messages(self):
        return [message.copy() for message in self.messages]

    
    def clear(self):
        """Xóa toàn bộ lịch sử hội thoại."""
        self.messages.clear()
        self.save_memory()
        print("Đã xóa toàn bộ lịch sử hội thoại.")


    

    def load_memory(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Dữ liệu Memory phải có dạng danh sách.")

            # Kiểm tra cấu trúc từng tin nhắn
            for message in data:
                if not isinstance(message, dict):
                    raise ValueError("Tin nhắn phải có dạng dictionary.")

                if message.get("role") not in ["user", "assistant"]:
                    raise ValueError("Role chỉ được là 'user' hoặc 'assistant'.")

                if not isinstance(message.get("content"), str):
                    raise ValueError("Content phải có kiểu chuỗi.")
                
                if not message["role"].strip():
                            raise ValueError("Role không được để trống.")
                
                if not message["content"].strip():
                    raise ValueError("Content không được để trống.")
                        # Tự động tải lịch sử hội thoại khi khởi tạo

            self.messages = data
            # Giới hạn số lượng tin nhắn khi tải
            self.messages = self.messages[-self.max_messages:]

            # Giới hạn tổng Token khi tải
            while len(self.messages) > 1 and self.get_total_tokens() > self.max_tokens:
                self.messages.pop(0)

            # Lưu lại dữ liệu sau khi điều chỉnh
            self.save_memory()
        except (json.JSONDecodeError, OSError, ValueError) as error:
            print(f"Lỗi khi tải Memory: {error}")
            self.messages = []


    
    def save_memory(self):
        """Lưu lịch sử hội thoại bằng cơ chế Atomic File Write."""

        temp_file = self.file_path + ".tmp"

        try:
            # Bước 1: Ghi dữ liệu vào file tạm
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(
                    self.messages,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

                file.flush()
                os.fsync(file.fileno())

            # Bước 2: Thay thế file chính sau khi ghi thành công
            os.replace(temp_file, self.file_path)

        except OSError as error:
            print(f"Lỗi khi lưu Memory: {error}")

            # Xóa file tạm nếu còn tồn tại
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass


    
    def get_stats(self):
        total_tokens = self.get_total_tokens()

        return {
            "total_messages": len(self.messages),
            "max_messages": self.max_messages,
            "remaining_slots": max(0, self.max_messages - len(self.messages)),
            "total_tokens": total_tokens,
            "max_tokens": self.max_tokens,
            "remaining_tokens": max(0, self.max_tokens - total_tokens)
        }

    
    def count_tokens(self, text: str) -> int:
        """Đếm số lượng token trong văn bản."""
        tokens = self.encoding.encode(text)
        return len(tokens)

    
    def get_total_tokens(self) -> int:
        """Tính tổng số token trong lịch sử hội thoại."""

        total = 0

        for message in self.messages:
            total += self.count_tokens(message["content"])

        return total