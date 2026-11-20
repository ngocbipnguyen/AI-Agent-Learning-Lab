from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def semantic_search(
    query: str,
    embeddings: list,
    sentences: list,
    top_k: int = 3
):
    # Chuyển câu hỏi thành Embedding
    query_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = query_response.data[0].embedding

    # Tính Cosine Similarity
    results = []

    for sentence, embedding in zip(sentences, embeddings):
        similarity = np.dot(query_embedding, embedding) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(embedding)
        )

        results.append({
            "title": sentence,
            "similarity": float(similarity)
        })

    # Sắp xếp kết quả
    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    # Trả về Top K
    return results[:top_k]

sentences = [
    "OpenAI ra mắt mô hình AI mới với khả năng suy luận tốt hơn.",
    "Google phát triển công nghệ trí tuệ nhân tạo thế hệ mới.",
    "NVIDIA giới thiệu chip GPU mới dành cho trung tâm dữ liệu AI.",
    "Apple chuẩn bị ra mắt mẫu iPhone mới.",
    "Microsoft đầu tư phát triển hệ thống điện toán đám mây."
]




response = client.embeddings.create(
    model="text-embedding-3-small",
    input=sentences
)
embeddings = [
    item.embedding
    for item in response.data
]

results = semantic_search(
    query="Những tin tức liên quan đến trí tuệ nhân tạo?",
    embeddings=embeddings,
    sentences=sentences,
    top_k=3
)

for item in results:
    print(f"{item['similarity']:.4f} - {item['title']}")

# print("Số tin tức:", len(embeddings))
# print("Số chiều mỗi vector:", len(embeddings[0]))

# for item in response.data:
#     print(f"Index: {item.index}")
#     print(f"Số chiều: {len(item.embedding)}")
#     print("-" * 30)

# import numpy as np

# embeddings = [
#     item.embedding
#     for item in response.data
# ]

# similarity_01 = np.dot(
#     embeddings[0], embeddings[1]
# ) / (
#     np.linalg.norm(embeddings[0])
#     * np.linalg.norm(embeddings[1])
# )

# similarity_02 = np.dot(
#     embeddings[0], embeddings[2]
# ) / (
#     np.linalg.norm(embeddings[0])
#     * np.linalg.norm(embeddings[2])
# )

# print("Câu 1 và câu 2:", similarity_01)
# print("Câu 1 và câu 3:", similarity_02)

# Câu hỏi của người dùng
# query = "Những tin tức liên quan đến trí tuệ nhân tạo?"

# # Chuyển câu hỏi thành Embedding
# query_response = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=query
# )

# query_embedding = query_response.data[0].embedding

# # Tính độ tương đồng
# results = []

# for sentence, embedding in zip(sentences, embeddings):
#     similarity = np.dot(query_embedding, embedding) / (
#         np.linalg.norm(query_embedding)
#         * np.linalg.norm(embedding)
#     )

#     results.append({
#         "title": sentence,
#         "similarity": similarity
#     })

# # Sắp xếp theo độ tương đồng giảm dần
# results.sort(
#     key=lambda item: item["similarity"],
#     reverse=True
# )

# # Hiển thị kết quả
# for item in results[:3]:
#     print(
#         f"{item['similarity']:.4f} - {item['title']}"
#     )