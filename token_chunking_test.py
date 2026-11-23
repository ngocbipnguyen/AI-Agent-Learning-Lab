import tiktoken


def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:

    encoding = tiktoken.encoding_for_model("gpt-4o")

    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]

        chunk = encoding.decode(chunk_tokens)

        chunks.append(chunk)

        start += chunk_size - overlap

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
    chunk_size=30,
    overlap=5
)

# for index, chunk in enumerate(chunks):
#     print(f"\nChunk {index + 1}:")
#     print(chunk)

encoding = tiktoken.encoding_for_model("gpt-4o")

for index, chunk in enumerate(chunks):
    token_count = len(encoding.encode(chunk))

    print(f"\nChunk {index + 1}:")
    print("Token count:", token_count)
    print(chunk)