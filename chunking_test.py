def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            end = text.rfind(" ", start, end)

            if end == -1 or end <= start:
                end = start + chunk_size

        chunk = text[start:end].strip()
        chunks.append(chunk)

        start = end - overlap

    return chunks


document = """
Trí tuệ nhân tạo đang phát triển nhanh chóng.
OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn.
Google phát triển các công nghệ AI mới.
NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu.
Microsoft mở rộng hệ thống điện toán đám mây.
"""

chunks = chunk_text(
    text=document,
    chunk_size=100,
    overlap=20
)

for index, chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}:")
    print(chunk)