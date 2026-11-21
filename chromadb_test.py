import chromadb
from embedding.embedding_service import create_embeddings
from embedding.embedding_service import create_embedding
# Khởi tạo ChromaDB Client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

print("ChromaDB kết nối thành công!")

# Tạo Collection
openai_collection = client.get_or_create_collection(
    name="technology_news_openai"
)

# print("Collection:", openai_collection.name)

# openai_collection.add(
#     ids=[
#         "news_001",
#         "news_002",
#         "news_003",
#         "news_004",
#         "news_005"
#     ],
#     documents=[
#         "OpenAI ra mắt mô hình AI mới với khả năng suy luận tốt hơn.",
#         "Google phát triển công nghệ trí tuệ nhân tạo thế hệ mới.",
#         "NVIDIA giới thiệu chip GPU mới dành cho trung tâm dữ liệu AI.",
#         "Apple chuẩn bị ra mắt mẫu iPhone mới.",
#         "Microsoft đầu tư phát triển hệ thống điện toán đám mây."
#     ],
#     metadatas=[
#         {"category": "AI", "source": "OpenAI"},
#         {"category": "AI", "source": "Google"},
#         {"category": "Hardware", "source": "NVIDIA"},
#         {"category": "Mobile", "source": "Apple"},
#         {"category": "Cloud", "source": "Microsoft"}
#     ]
# )

# print("Đã thêm dữ liệu thành công!")
# print("Tổng số documents:", openai_collection.count())

# results = openai_collection.query(
#     query_texts=[
#         "Những tin tức liên quan đến trí tuệ nhân tạo?"
#     ],
#     n_results=3
# )

# for document in results["documents"][0]:
#     print(document)

# results = openai_collection.query(
#     query_texts=[
#         "Những tin tức liên quan đến công nghệ?"
#     ],
#     n_results=3,
#     where={
#         "category": "AI"
#     }
# )

# for document in results["documents"][0]:
#     print(document)

# results = openai_collection.get(
#     ids=["news_001", "news_003"]
# )

# for document, metadata in zip(
#     results["documents"],
#     results["metadatas"]
# ):
#     print("Document:", document)
#     print("Metadata:", metadata)
#     print("-" * 40)


# openai_collection.update(
#     ids=["news_001"],
#     documents=[
#         "OpenAI ra mắt mô hình AI mới với khả năng suy luận và lập trình tốt hơn."
#     ],
#     metadatas=[
#         {
#             "category": "AI",
#             "source": "OpenAI",
#             "status": "updated"
#         }
#     ]
# )

# print("Đã cập nhật dữ liệu!")

# result = openai_collection.get(
#     ids=["news_001"]
# )

# print("Document:", result["documents"][0])
# print("Metadata:", result["metadatas"][0])

# openai_collection.delete(
#     ids=["news_001"]
# )

# print("Đã xóa dữ liệu!")

# print("Số documents còn lại:", openai_collection.count())


# sentences = [
#     "OpenAI ra mắt mô hình AI mới.",
#     "Google phát triển công nghệ trí tuệ nhân tạo.",
#     "NVIDIA giới thiệu GPU mới cho AI."
# ]

# embeddings = create_embeddings(sentences)

# print("Số Embeddings:", len(embeddings))

# collection.add(
#     ids=[
#         "openai_001",
#         "google_001",
#         "nvidia_001"
#     ],
#     documents=sentences,
#     embeddings=embeddings,
#     metadatas=[
#         {"category": "AI", "source": "OpenAI"},
#         {"category": "AI", "source": "Google"},
#         {"category": "Hardware", "source": "NVIDIA"}
#     ]
# )

# print("Đã lưu Embeddings vào ChromaDB!")
# print("Tổng số documents:", collection.count())

# query = "Những tin tức liên quan đến trí tuệ nhân tạo?"

# query_embedding = create_embedding(query)

# results = openai_collection.query(
#     query_embeddings=[query_embedding],
#     n_results=3
# )

# for document in results["documents"][0]:
#     print(document)

print("Số documents:", openai_collection.count())

results = openai_collection.get()

for document in results["documents"]:
    print(document)