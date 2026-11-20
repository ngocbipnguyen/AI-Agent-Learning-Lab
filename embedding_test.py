from embedding.embedding_service import create_embeddings
from embedding.search import semantic_search


sentences = [
    "OpenAI ra mắt mô hình AI mới với khả năng suy luận tốt hơn.",
    "Google phát triển công nghệ trí tuệ nhân tạo thế hệ mới.",
    "NVIDIA giới thiệu chip GPU mới dành cho trung tâm dữ liệu AI.",
    "Apple chuẩn bị ra mắt mẫu iPhone mới.",
    "Microsoft đầu tư phát triển hệ thống điện toán đám mây."
]

# Tạo Embeddings
embeddings = create_embeddings(sentences)

# Semantic Search
results = semantic_search(
    query="Những tin tức liên quan đến trí tuệ nhân tạo?",
    embeddings=embeddings,
    sentences=sentences,
    top_k=3
)

# In kết quả
for item in results:
    print(
        f"{item['similarity']:.4f} - {item['title']}"
    )