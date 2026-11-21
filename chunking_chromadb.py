
import chromadb

# Tạo Persistent Client
client = chromadb.PersistentClient(
    path="./chunking_db"
)

# Tạo Collection riêng cho các chunks
collection = client.get_or_create_collection(
    name="technology_chunks"
)

# Dữ liệu mẫu
chunks = [
    "OpenAI phát triển mô hình AI mới.",
    "Mô hình AI có khả năng phân tích dữ liệu.",
    "Google phát triển công nghệ AI mới."
]

# # Lưu chunks vào ChromaDB
# collection.add(
#     ids=["chunk_1", "chunk_2", "chunk_3"],
#     documents=chunks,
#     metadatas=[
#         {"source": "technology_news.txt", "chunk_index": 0},
#         {"source": "technology_news.txt", "chunk_index": 1},
#         {"source": "technology_news.txt", "chunk_index": 2}
#     ]
# )

# print("Đã lưu chunks vào ChromaDB!")
# print("Total chunks:", collection.count())


# print("\n=== CHECK STORED CHUNKS ===")

# results = collection.get(
#     include=["documents", "metadatas"]
# )

# for index, chunk_id in enumerate(results["ids"]):
#     print(f"\nID: {chunk_id}")
#     print("Document:", results["documents"][index])
#     print("Metadata:", results["metadatas"][index])



metadatas=[
    {
        "source": "technology_news.txt",
        "chunk_index": 0,
        "category": "AI"
    },
    {
        "source": "technology_news.txt",
        "chunk_index": 1,
        "category": "AI"
    },
    {
        "source": "technology_news.txt",
        "chunk_index": 2,
        "category": "AI"
    }
]

# collection.upsert(
#     ids=["chunk_1", "chunk_2", "chunk_3"],
#     documents=chunks,
#     metadatas=[
#         {
#             "source": "technology_news.txt",
#             "chunk_index": 0,
#             "category": "AI"
#         },
#         {
#             "source": "technology_news.txt",
#             "chunk_index": 1,
#             "category": "AI"
#         },
#         {
#             "source": "technology_news.txt",
#             "chunk_index": 2,
#             "category": "AI"
#         }
#     ]
# )

print("\n=== SEMANTIC SEARCH ===")

query = "Công ty nào phát triển mô hình AI?"

results = collection.query(
    query_texts=[query],
    n_results=3,
    where={
        "$and": [
            {"category": "AI"},
            {"source": "technology_news.txt"}
        ]
    }
)

# print("Results:", results)
# print("Documents:", results["documents"])

for index, document in enumerate(results["documents"][0]):
    print(f"\nResult {index + 1}:")
    print("Document:", document)
    print("Distance:", results["distances"][0][index])
    print("Metadata:", results["metadatas"][0][index])

