
document = """
OpenAI phát triển các mô hình trí tuệ nhân tạo mới.
Các mô hình này có khả năng xử lý ngôn ngữ tự nhiên.

Google nghiên cứu công nghệ AI phục vụ doanh nghiệp.
Google cũng phát triển các mô hình ngôn ngữ lớn.

NVIDIA sản xuất GPU phục vụ trung tâm dữ liệu AI.
Các GPU này hỗ trợ quá trình huấn luyện mô hình AI.
"""




def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:

    if chunk_size <= overlap or overlap < 0:
        raise ValueError("chunk_size phải lớn hơn overlap >= 0")

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

        # Đã xử lý hết tài liệu thì dừng
        if end >= len(text):
            break

        next_start = end - overlap

        # Lùi về đầu từ để không cắt ngang từ
        boundary = text.rfind(" ", 0, next_start)

        if boundary >= start:
            next_start = boundary + 1

        if next_start <= start:
            raise ValueError("Không thể tiến tới chunk tiếp theo")

        start = next_start

    return chunks



chunks = chunk_text(
    document,
    chunk_size=100,
    overlap=20
)

def index_documents(collection, chunk_records):
    ids = [record["id"] for record in chunk_records]
    documents = [record["text"] for record in chunk_records]
    metadatas = [record["metadata"] for record in chunk_records]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Đã index {len(chunk_records)} chunks.")

chunk_records = []

for index, chunk in enumerate(chunks):
    record = {
        "id": f"technology_news_{index}",
        "text": chunk,
        "metadata": {
            "source": "technology_news_demo",
            "chunk_index": index,
            "category": ["AI", "AI", "GPU", "GPU"][index]
        }
    }

    chunk_records.append(record)



def hybrid_search(collection, query, chunk_records, top_k=4):
    # 1. Semantic Search
    semantic_results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    semantic_documents = semantic_results["documents"][0]

    # 2. Keyword Search
    query_keywords = query.split()

    keyword_results = []

    for record in chunk_records:
        if any(
            keyword.lower() in record["text"].lower()
            for keyword in query_keywords
        ):
            keyword_results.append(record["text"])

    # 3. Merge và loại bỏ kết quả trùng
    hybrid_results = list(dict.fromkeys(
        semantic_documents + keyword_results
    ))

    # 4. Reranking
    ranked_results = []

    for document in hybrid_results:
        score = sum(
            keyword.lower() in document.lower()
            for keyword in query_keywords
        )

        ranked_results.append({
            "text": document,
            "score": score
        })

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_results[:top_k]

import chromadb

# Kết nối ChromaDB
client = chromadb.PersistentClient(
    path="./rag_chroma_db"
)

# Tạo Collection
collection = client.get_or_create_collection(
    name="rag_technology_news"
)

# Tách dữ liệu từ chunk_records
ids = [record["id"] for record in chunk_records]

documents = [
    record["text"] for record in chunk_records
]

metadatas = [
    record["metadata"] for record in chunk_records
]

# Lưu dữ liệu
index_documents(collection, chunk_records)




# Keyword Search
keyword = "NVIDIA"

keyword_results = []

for record in chunk_records:
    if keyword.lower() in record["text"].lower():
        keyword_results.append(record["text"])

print("\n=== KEYWORD SEARCH ===")

for result in keyword_results:
    print(result)

query = "Thông tin về NVIDIA và GPU"

results = collection.query(
    query_texts=[query],
    n_results=4
)


# Hybrid Search - Basic
semantic_results = results["documents"][0]

hybrid_results = list(dict.fromkeys(
    semantic_results + keyword_results
))

print("\n=== HYBRID SEARCH ===")

for index, result in enumerate(hybrid_results):
    print(f"\nResult {index + 1}:")
    print(result)




# Simple Reranking

query_keywords = ["NVIDIA", "GPU"]

ranked_results = []

for chunk in hybrid_results:
    score = sum(
        keyword.lower() in chunk.lower()
        for keyword in query_keywords
    )

    ranked_results.append({
        "text": chunk,
        "score": score
    })

# Sắp xếp score giảm dần
ranked_results.sort(
    key=lambda item: item["score"],
    reverse=True
)

print("\n=== RERANKING ===")

for index, result in enumerate(ranked_results):
    print(f"\nRank {index + 1}")
    print("Score:", result["score"])
    print("Document:", result["text"])


# print("\n=== CHUNK RECORDS ===")

# for record in chunk_records:
#     print(record)


# print("\n=== DOCUMENT CHUNKS ===")

# for index, chunk in enumerate(chunks):
#     print(f"\nChunk {index}:")
#     print(chunk)


# print("=== DOCUMENT ===")
# print(document)




# print("\n=== CHROMADB ===")
# print("Total chunks:", collection.count())



# # Semantic Search
# query = "Công ty nào sản xuất điện thoại Samsung?"

# results = collection.query(
#     query_texts=[query],
#     n_results=4
# )

# # print("\n=== SEMANTIC SEARCH ===")

# # for i, document in enumerate(results["documents"][0]):
# #     print(f"\nResult {i + 1}:")
# #     print("Document:", document)
# #     print("Metadata:", results["metadatas"][0][i])
# #     print("Distance:", results["distances"][0][i])


# # Build Context
# retrieved_documents = results["documents"][0]

# context = "\n\n".join(retrieved_documents)

# query = "Công ty nào sản xuất điện thoại Samsung?"

# print("\n=== BUILD CONTEXT ===")
# print(context)



# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv(override=True)

# client_openai = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# response = client_openai.chat.completions.create(
#     model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
#     messages=[
#         {
#             "role": "system",
#             "content": """
#             Bạn là trợ lý AI trả lời câu hỏi dựa trên context được cung cấp.

#             Quy tắc:
#             - Chỉ sử dụng thông tin trong context.
#             - Không tự suy diễn hoặc bịa thông tin.
#             - Nếu context không có câu trả lời, hãy nói không tìm thấy thông tin.
#             """
#         },
#         {
#             "role": "user",
#             "content": f"""
#             Context:
#             {context}

#             Question:
#             {query}
#             """
#         }
#     ]
# )

# print("\n=== GENERATION ===")
# print("Question:", query)
# print("Answer:", response.choices[0].message.content)



# # Similarity Threshold
# threshold = 0.6

# filtered_documents = []

# for document, distance in zip(
#     results["documents"][0],
#     results["distances"][0]
# ):
#     if distance <= threshold:
#         filtered_documents.append(document)

# print("\n=== FILTERED RESULTS ===")

# for document in filtered_documents:
#     print(document)



# Semantic Search
query = "Công ty nào sản xuất điện thoại Samsung?"

results = collection.query(
    query_texts=[query],
    n_results=4,
    where={"category": "AI"}
)

# Similarity Threshold
threshold = 1.0

filtered_documents = []

for document, distance in zip(
    results["documents"][0],
    results["distances"][0]
):
    if distance <= threshold:
        filtered_documents.append(document)

# print("\n=== FILTERED RESULTS ===")

# for document in filtered_documents:
#     print(document)

# Build Context
context = "\n\n".join(filtered_documents)

# print("\n=== BUILD CONTEXT ===")
# print(context)


