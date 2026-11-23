def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:

    if chunk_size <= overlap:
        raise ValueError("chunk_size phải lớn hơn overlap")

    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        next_start = end - overlap

        # Không tạo Chunk nếu phần còn lại chỉ là nội dung lặp
        if next_start >= len(text):
            break

        remaining = text[next_start:].strip()

        if remaining in chunk:
            break

        start = next_start

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