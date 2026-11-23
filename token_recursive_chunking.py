
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


# text = "OpenAI đang phát triển công nghệ AI."

# print("Token count:", count_tokens(text))



def recursive_split(
    text: str,
    chunk_size: int = 100,
    separators: list[str] | None = None
) -> list[str]:

    if separators is None:
        separators = ["\n\n", ".", " ", ""]

    if count_tokens(text) <= chunk_size:
        return [text.strip()]

    separator = separators[0]
    remaining = separators[1:]

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

        if count_tokens(candidate) <= chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            if count_tokens(part) > chunk_size:
                if remaining:
                    chunks.extend(
                        recursive_split(
                            part,
                            chunk_size,
                            remaining
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




def apply_overlap(
    chunks: list[str],
    chunk_size: int = 30,
    overlap: int = 5
) -> list[str]:

    result = []

    for index, chunk in enumerate(chunks):
        if index == 0:
            result.append(chunk)
            continue

        previous_words = chunks[index - 1].split()
        overlap_words = []

        for word in reversed(previous_words):
            candidate = " ".join([word] + overlap_words)

            if count_tokens(candidate) > overlap:
                break

            overlap_words = [word] + overlap_words

        overlap_text = " ".join(overlap_words)

        new_chunk = (
            overlap_text + " " + chunk
            if overlap_text else chunk
        )

        while count_tokens(new_chunk) > chunk_size and overlap_words:
            overlap_words.pop(0)
            overlap_text = " ".join(overlap_words)

            new_chunk = (
                overlap_text + " " + chunk
                if overlap_text else chunk
            )

        result.append(new_chunk)

    return result




document = """
Trí tuệ nhân tạo đang phát triển nhanh chóng.
OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn.

Google phát triển các công nghệ AI mới.
NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu.
Microsoft mở rộng hệ thống điện toán đám mây.
"""

# chunks = recursive_split(document, chunk_size=30)
chunks = recursive_split(document, chunk_size=30)

chunks = apply_overlap(
    chunks,
    chunk_size=30,
    overlap=5
)


print("\n=== OVERLAP VALIDATION ===")

for index in range(1, len(chunks)):
    previous = chunks[index - 1]
    current = chunks[index]

    previous_tokens = encoding.encode(previous)
    current_tokens = encoding.encode(current)

    print(f"\nChunk {index + 1}:")

    print(
        "Previous chunk tokens:",
        len(previous_tokens)
    )

    print(
        "Current chunk tokens:",
        len(current_tokens)
    )

    print("Current chunk starts with:", current[:40])
    print("Within limit:", count_tokens(current) <= 30)




