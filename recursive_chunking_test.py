

def get_overlap_text(text: str, overlap: int) -> str:
    if overlap <= 0:
        return ""

    start = max(0, len(text) - overlap)

    # Nếu đang nằm giữa một từ, bỏ phần từ bị cắt
    if start > 0 and text[start] != " ":
        next_space = text.find(" ", start)

        if next_space == -1:
            return ""

        start = next_space + 1

    return text[start:].strip()



def recursive_chunk(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20,
    separators: list[str] | None = None
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size phải lớn hơn 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap phải >= 0 và nhỏ hơn chunk_size")

    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]

    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    if not separators:
        raise ValueError("Không còn separator để chia nhỏ")

    separator = separators[0]
    remaining_separators = separators[1:]

    if separator:
        splits = text.split(separator)
    else:
        splits = list(text)

    chunks = []
    current_chunk = ""

    for part in splits:
        if not part.strip():
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
                sub_chunks = recursive_chunk(
                    text=part,
                    chunk_size=chunk_size,
                    overlap=0,
                    separators=remaining_separators
                )

                chunks.extend(sub_chunks)
                current_chunk = ""

            else:
                current_chunk = part

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Thêm overlap giữa các chunk
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = [chunks[0]]

        for i in range(1, len(chunks)):
            previous_chunk = chunks[i - 1]
            current_chunk = chunks[i]

            overlap_text = get_overlap_text(
                previous_chunk,
                overlap
            )

            # Giữ chunk trong giới hạn chunk_size
            separator_space = 1

            available_space = chunk_size - len(current_chunk) - separator_space

            if available_space > 0:
                overlap_text = get_overlap_text(
                    previous_chunk,
                    min(overlap, available_space)
                )

                new_chunk = overlap_text + " " + current_chunk
                new_chunk = new_chunk.strip()
            else:
                new_chunk = current_chunk

            overlapped_chunks.append(new_chunk)

        chunks = overlapped_chunks

    return chunks


document = """
OpenAI liên tục nghiên cứu và phát triển
các mô hình trí tuệ nhân tạo có khả năng
xử lý ngôn ngữ tự nhiên và phân tích dữ liệu.

Google cũng đang đầu tư mạnh vào AI,
đặc biệt là các mô hình ngôn ngữ lớn
và công nghệ AI phục vụ doanh nghiệp.
"""

chunks = recursive_chunk(
    document,
    chunk_size=50,
    overlap=15
)

for index, chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}:")
    print("Character count:", len(chunk))
    print(chunk)


# test_text = "OpenAI liên tục nghiên cứu và phát triển"

# print("\n=== TEST OVERLAP ===")
# print("Original:", test_text)
# print("Overlap:", get_overlap_text(test_text, 15))


previous_chunk = "OpenAI liên tục nghiên cứu và phát triển"
current_chunk = "các mô hình trí tuệ nhân tạo có khả năng"

overlap_text = get_overlap_text(previous_chunk, 15)

new_chunk = overlap_text + " " + current_chunk

print("\n=== TEST MERGE ===")
print("Previous:", previous_chunk)
print("Overlap:", overlap_text)
print("Current:", current_chunk)
print("Merged:", new_chunk)
print("Character count:", len(new_chunk))