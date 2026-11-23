


# def get_overlap_text(text: str, overlap: int) -> str:
#     if overlap <= 0:
#         return ""

#     start = max(0, len(text) - overlap)

#     # Nếu đang nằm giữa một từ, bỏ phần từ bị cắt
#     if start > 0 and text[start] != " ":
#         next_space = text.find(" ", start)

#         if next_space == -1:
#             return ""

#         start = next_space + 1

#     return text[start:].strip()



# def recursive_chunk(
#     text: str,
#     chunk_size: int = 100,
#     overlap: int = 20,
#     separators: list[str] | None = None
# ) -> list[str]:

#     if chunk_size <= 0:
#         raise ValueError("chunk_size phải lớn hơn 0")

#     if overlap < 0 or overlap >= chunk_size:
#         raise ValueError("overlap phải >= 0 và nhỏ hơn chunk_size")

#     if separators is None:
#         separators = ["\n\n", "\n", ". ", " ", ""]

#     text = text.strip()

#     if not text:
#         return []

#     if len(text) <= chunk_size:
#         return [text]

#     if not separators:
#         raise ValueError("Không còn separator để chia nhỏ")
# >>>>>>> 35eb7e7 (pipeline)

#     separator = separators[0]
#     remaining_separators = separators[1:]

#     if separator:
# <<<<<<< HEAD
#         parts = text.split(separator)
#     else:
#         parts = list(text)
# =======
#         splits = text.split(separator)
#     else:
#         splits = list(text)
# >>>>>>> 35eb7e7 (pipeline)

#     chunks = []
#     current_chunk = ""

# <<<<<<< HEAD
#     for part in parts:
#         if not part:
# =======
#     for part in splits:
#         if not part.strip():
# >>>>>>> 35eb7e7 (pipeline)
#             continue

#         candidate = (
#             current_chunk + separator + part
#             if current_chunk else part
#         )

#         if len(candidate) <= chunk_size:
#             current_chunk = candidate
# <<<<<<< HEAD
# =======

# >>>>>>> 35eb7e7 (pipeline)
#         else:
#             if current_chunk:
#                 chunks.append(current_chunk.strip())

#             if len(part) > chunk_size:
# <<<<<<< HEAD
#                 if remaining_separators:
#                     chunks.extend(
#                         chunk_text(
#                             part,
#                             chunk_size,
#                             remaining_separators
#                         )
#                     )
#                 else:
#                     chunks.extend(
#                         part[i:i + chunk_size]
#                         for i in range(0, len(part), chunk_size)
#                     )
#                 current_chunk = ""
# =======
#                 sub_chunks = recursive_chunk(
#                     text=part,
#                     chunk_size=chunk_size,
#                     overlap=0,
#                     separators=remaining_separators
#                 )

#                 chunks.extend(sub_chunks)
#                 current_chunk = ""

# >>>>>>> 35eb7e7 (pipeline)
#             else:
#                 current_chunk = part

#     if current_chunk:
#         chunks.append(current_chunk.strip())

# <<<<<<< HEAD
#     return chunks



# # document = """
# # Trí tuệ nhân tạo đang phát triển nhanh chóng.
# # OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn.
# # Google phát triển các công nghệ AI mới.
# # NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu.
# # Microsoft mở rộng hệ thống điện toán đám mây.
# # """

# # chunks = chunk_text(document, chunk_size=100)

# # for index, chunk in enumerate(chunks):
# #     print(f"\nChunk {index + 1}:")
# #     print(chunk)


# # long_text = (
# #     "Trí tuệ nhân tạo đang phát triển nhanh chóng "
# #     "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn "
# #     "Google phát triển các công nghệ AI mới "
# #     "NVIDIA đầu tư vào chip GPU phục vụ trung tâm dữ liệu"
# # )

# # print("\n=== TEST LONG TEXT ===")

# # long_chunks = chunk_text(long_text, chunk_size=50)

# # for index, chunk in enumerate(long_chunks):
# #     print(f"\nChunk {index + 1}:")
# #     print("Character count:", len(chunk))
# #     print(chunk)


# # very_long_text = "A" * 120

# # print("\n=== TEST VERY LONG WORD ===")

# # very_long_chunks = chunk_text(
# #     very_long_text,
# #     chunk_size=50
# # )

# # for index, chunk in enumerate(very_long_chunks):
# #     print(f"\nChunk {index + 1}:")
# #     print("Character count:", len(chunk))
# #     print(chunk)



# def add_overlap(
#     chunks: list[str],
#     overlap: int = 2
# ) -> list[str]:

#     result = []

#     for index, chunk in enumerate(chunks):
#         if index == 0:
#             result.append(chunk)
#             continue

#         previous_words = chunks[index - 1].split()
#         current_words = chunk.split()

#         overlap_words = previous_words[-overlap:]

#         new_chunk = " ".join(
#             overlap_words + current_words
#         )

#         result.append(new_chunk)

#     return result


# # sample_chunks = [
# #     "Trí tuệ nhân tạo đang phát triển nhanh chóng",
# #     "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn",
# #     "Google phát triển các công nghệ AI mới"
# # ]

# # overlapped_chunks = add_overlap(sample_chunks, overlap=2)

# # print("\n=== OVERLAP TEST ===")

# # for index, chunk in enumerate(overlapped_chunks):
# #     print(f"\nChunk {index + 1}:")
# #     print(chunk)



# import tiktoken

# def add_token_overlap(
#     chunks: list[str],
#     overlap: int = 5
# ) -> list[str]:

#     encoding = tiktoken.encoding_for_model("gpt-4o")

#     result = []

#     for index, chunk in enumerate(chunks):
#         if index == 0:
#             result.append(chunk)
#             continue

#         previous_tokens = encoding.encode(chunks[index - 1])
#         current_tokens = encoding.encode(chunk)

#         overlap_tokens = previous_tokens[-overlap:]

#         new_tokens = overlap_tokens + current_tokens

#         overlap_text = encoding.decode(overlap_tokens)
#         new_chunk = overlap_text.rstrip() + " " + chunk.lstrip()

#         result.append(new_chunk)

#     return result


# sample_chunks = [
#     "Trí tuệ nhân tạo đang phát triển nhanh chóng",
#     "OpenAI liên tục cải tiến các mô hình ngôn ngữ lớn",
#     "Google phát triển các công nghệ AI mới"
# ]

# overlapped_chunks = add_token_overlap(
#     sample_chunks,
#     overlap=5
# )

# print("\n=== TOKEN OVERLAP TEST ===")

# for index, chunk in enumerate(overlapped_chunks):
#     print(f"\nChunk {index + 1}:")

#     token_count = len(
#         tiktoken.encoding_for_model("gpt-4o").encode(chunk)
#     )

#     print("Token count:", token_count)
#     print(chunk)
# =======
#     # Thêm overlap giữa các chunk
#     if overlap > 0 and len(chunks) > 1:
#         overlapped_chunks = [chunks[0]]

#         for i in range(1, len(chunks)):
#             previous_chunk = chunks[i - 1]
#             current_chunk = chunks[i]

#             overlap_text = get_overlap_text(
#                 previous_chunk,
#                 overlap
#             )

#             # Giữ chunk trong giới hạn chunk_size
#             separator_space = 1

#             available_space = chunk_size - len(current_chunk) - separator_space

#             if available_space > 0:
#                 overlap_text = get_overlap_text(
#                     previous_chunk,
#                     min(overlap, available_space)
#                 )

#                 new_chunk = overlap_text + " " + current_chunk
#                 new_chunk = new_chunk.strip()
#             else:
#                 new_chunk = current_chunk

#             overlapped_chunks.append(new_chunk)

#         chunks = overlapped_chunks

#     return chunks


# document = """
# OpenAI liên tục nghiên cứu và phát triển
# các mô hình trí tuệ nhân tạo có khả năng
# xử lý ngôn ngữ tự nhiên và phân tích dữ liệu.

# Google cũng đang đầu tư mạnh vào AI,
# đặc biệt là các mô hình ngôn ngữ lớn
# và công nghệ AI phục vụ doanh nghiệp.
# """

# chunks = recursive_chunk(
#     document,
#     chunk_size=50,
#     overlap=15
# )

# for index, chunk in enumerate(chunks):
#     print(f"\nChunk {index + 1}:")
#     print("Character count:", len(chunk))
#     print(chunk)


# # test_text = "OpenAI liên tục nghiên cứu và phát triển"

# # print("\n=== TEST OVERLAP ===")
# # print("Original:", test_text)
# # print("Overlap:", get_overlap_text(test_text, 15))


# previous_chunk = "OpenAI liên tục nghiên cứu và phát triển"
# current_chunk = "các mô hình trí tuệ nhân tạo có khả năng"

# overlap_text = get_overlap_text(previous_chunk, 15)

# new_chunk = overlap_text + " " + current_chunk

# print("\n=== TEST MERGE ===")
# print("Previous:", previous_chunk)
# print("Overlap:", overlap_text)
# print("Current:", current_chunk)
# print("Merged:", new_chunk)
# print("Character count:", len(new_chunk))
# >>>>>>> 35eb7e7 (pipeline)
