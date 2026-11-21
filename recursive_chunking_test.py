

def chunk_text(
    text: str,
    chunk_size: int = 100,
    separators: list[str] | None = None
) -> list[str]:

    if separators is None:
        separators = ["\n\n", ".", " ", ""]

    if len(text) <= chunk_size:
        return [text.strip()]

    separator = separators[0]
    remaining_separators = separators[1:]

    if separator:
        parts = text.split(separator)
    else:
        parts = list(text)

    chunks = []
    current_chunk = ""

    for part in parts:
        if not part:
            continue

        candidate = (
            current_chunk + separator + part
            if current_chunk else part
        )

        if len(candidate) <= chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            if len(part) > chunk_size:
                if remaining_separators:
                    chunks.extend(
                        chunk_text(
                            part,
                            chunk_size,
                            remaining_separators
                        )
                    )
                else:
                    chunks.extend(
                        part[i:i + chunk_size]
                        for i in range(0, len(part), chunk_size)
                    )
                current_chunk = ""
            else:
                current_chunk = part

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks



# document = """
# Trí tuệ nhân tạo đang phát triển nhanh chóng.
# OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn.
# Google phát triển các công nghệ AI mới.
# NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu.
# Microsoft mở rộng hệ thống điện toán đám mây.
# """

# chunks = chunk_text(document, chunk_size=100)

# for index, chunk in enumerate(chunks):
#     print(f"\nChunk {index + 1}:")
#     print(chunk)


# long_text = (
#     "Trí tuệ nhân tạo đang phát triển nhanh chóng "
#     "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn "
#     "Google phát triển các công nghệ AI mới "
#     "NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu"
# )

# print("\n=== TEST LONG TEXT ===")

# long_chunks = chunk_text(long_text, chunk_size=50)

# for index, chunk in enumerate(long_chunks):
#     print(f"\nChunk {index + 1}:")
#     print("Character count:", len(chunk))
#     print(chunk)


# very_long_text = "A" * 120

# print("\n=== TEST VERY LONG WORD ===")

# very_long_chunks = chunk_text(
#     very_long_text,
#     chunk_size=50
# )

# for index, chunk in enumerate(very_long_chunks):
#     print(f"\nChunk {index + 1}:")
#     print("Character count:", len(chunk))
#     print(chunk)



def add_overlap(
    chunks: list[str],
    overlap: int = 2
) -> list[str]:

    result = []

    for index, chunk in enumerate(chunks):
        if index == 0:
            result.append(chunk)
            continue

        previous_words = chunks[index - 1].split()
        current_words = chunk.split()

        overlap_words = previous_words[-overlap:]

        new_chunk = " ".join(
            overlap_words + current_words
        )

        result.append(new_chunk)

    return result


# sample_chunks = [
#     "Trí tuệ nhân tạo đang phát triển nhanh chóng",
#     "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn",
#     "Google phát triển các công nghệ AI mới"
# ]

# overlapped_chunks = add_overlap(sample_chunks, overlap=2)

# print("\n=== OVERLAP TEST ===")

# for index, chunk in enumerate(overlapped_chunks):
#     print(f"\nChunk {index + 1}:")
#     print(chunk)



import tiktoken

def add_token_overlap(
    chunks: list[str],
    overlap: int = 5
) -> list[str]:

    encoding = tiktoken.encoding_for_model("gpt-4o")

    result = []

    for index, chunk in enumerate(chunks):
        if index == 0:
            result.append(chunk)
            continue

        previous_tokens = encoding.encode(chunks[index - 1])
        current_tokens = encoding.encode(chunk)

        overlap_tokens = previous_tokens[-overlap:]

        new_tokens = overlap_tokens + current_tokens

        overlap_text = encoding.decode(overlap_tokens)
        new_chunk = overlap_text.rstrip() + " " + chunk.lstrip()

        result.append(new_chunk)

    return result


sample_chunks = [
    "Trí tuệ nhân tạo đang phát triển nhanh chóng",
    "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn",
    "Google phát triển các công nghệ AI mới"
]

overlapped_chunks = add_token_overlap(
    sample_chunks,
    overlap=5
)

print("\n=== TOKEN OVERLAP TEST ===")

for index, chunk in enumerate(overlapped_chunks):
    print(f"\nChunk {index + 1}:")

    token_count = len(
        tiktoken.encoding_for_model("gpt-4o").encode(chunk)
    )

    print("Token count:", token_count)
    print(chunk)
