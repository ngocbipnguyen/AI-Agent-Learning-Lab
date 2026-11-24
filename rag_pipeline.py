import os
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from pathlib import Path
import hashlib
import json
# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_PATH = "./rag_pipeline_chroma_db"
COLLECTION_NAME = "rag_pipeline_openai"
MANIFEST_PATH = "document_manifest.json"

if not OPENAI_API_KEY:
    raise ValueError("Không tìm thấy OPENAI_API_KEY trong file .env")

client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

encoding = tiktoken.encoding_for_model("gpt-4o")


# ============================================================
# 1. CHUNKING
# ============================================================

def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
) -> list[str]:
    """Chia văn bản thành các chunks theo token, có overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size phải lớn hơn 0.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap phải >= 0 và nhỏ hơn chunk_size.")

    tokens = encoding.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk = encoding.decode(tokens[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(tokens):
            break

        start = end - overlap

    return chunks


def create_chunk_records(
    documents: list[dict[str, Any]],
    chunk_size: int = 100,
    overlap: int = 20
) -> list[dict[str, Any]]:
    """Chia nhiều tài liệu và tạo records gồm id, text, metadata."""
    chunk_records = []

    for document_index, document in enumerate(documents):
        chunks = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk_index, chunk in enumerate(chunks):
            chunk_records.append({
                "id": f"{document['id']}_{chunk_index}",
                "text": chunk,
                "metadata": {
                    "source": document["id"],
                    "category": document.get("category", "general"),
                    "chunk_index": chunk_index
                }
            })

    return chunk_records


# ============================================================
# 2. EMBEDDINGS
# ============================================================

def create_embeddings(texts: list[str]) -> list[list[float]]:
    """Tạo embeddings cho nhiều đoạn văn bản trong một API request."""
    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]


def create_embedding(text: str) -> list[float]:
    """Tạo embedding cho một câu truy vấn."""
    return create_embeddings([text])[0]


# ============================================================
# 3. INDEXING
# ============================================================

def index_documents(
    target_collection,
    chunk_records: list[dict[str, Any]]
) -> None:
    """Tạo embeddings và lưu chunks vào ChromaDB."""
    if not chunk_records:
        print("Không có chunks để index.")
        return

    texts = [record["text"] for record in chunk_records]
    embeddings = create_embeddings(texts)

    target_collection.upsert(
        ids=[record["id"] for record in chunk_records],
        documents=texts,
        embeddings=embeddings,
        metadatas=[record["metadata"] for record in chunk_records]
    )

    print(f"Đã index {len(chunk_records)} chunks.")



def sync_documents(
    target_collection,
    documents,
    chunk_size=100,
    overlap=20
):
    """Đồng bộ dữ liệu tài liệu vào ChromaDB."""

    # 1. Tạo chunks từ tài liệu hiện tại
    chunk_records = create_chunk_records(
        documents,
        chunk_size=chunk_size,
        overlap=overlap
    )

    # Không xóa dữ liệu cũ nếu không có nội dung mới hợp lệ
    if not chunk_records:
        print("Không có dữ liệu hợp lệ. Giữ nguyên ChromaDB.")
        return []

    # 2. Lấy danh sách ID hiện có
    existing_data = target_collection.get(
        include=["metadatas"]
    )

    existing_ids = existing_data["ids"]

    # 3. Xóa dữ liệu cũ
    if existing_ids:
        target_collection.delete(ids=existing_ids)
        print(f"Đã xóa {len(existing_ids)} chunks cũ.")

    # 4. Index dữ liệu mới
    index_documents(target_collection, chunk_records)

    print("Đồng bộ tài liệu hoàn tất.")

    return chunk_records
# ============================================================
# 4. SEMANTIC SEARCH
# ============================================================


def semantic_search(
    target_collection,
    query: str,
    top_k: int = 4,
    where: dict | None = None,
    threshold: float | None = None
) -> list[dict[str, Any]]:
    """Tìm chunks gần nghĩa và lọc theo similarity threshold."""

    query_embedding = create_embedding(query)

    search_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if where:
        search_args["where"] = where

    response = target_collection.query(**search_args)

    results = []

    for index, document in enumerate(response["documents"][0]):
        distance = response["distances"][0][index]

        if threshold is not None and distance > threshold:
            continue

        results.append({
            "text": document,
            "id": response["ids"][0][index],
            "metadata": response["metadatas"][0][index],
            "distance": distance
        })

    return results



# ============================================================
# 5. KEYWORD SEARCH
# ============================================================

def keyword_search(
    chunk_records: list[dict[str, Any]],
    query: str
) -> list[str]:
    """Tìm chunks có chứa ít nhất một từ trong query."""
    keywords = [
        word.lower()
        for word in query.split()
        if len(word.strip()) > 1
    ]

    results = []

    for record in chunk_records:
        text = record["text"]

        if any(keyword in text.lower() for keyword in keywords):
            results.append(text)

    return results


# ============================================================
# 6. HYBRID SEARCH
# ============================================================

def hybrid_search(
    target_collection,
    query: str,
    chunk_records: list[dict[str, Any]],
    top_k: int = 4,
    where: dict | None = None
) -> list[dict[str, Any]]:
    """Kết hợp semantic search và keyword search, loại bỏ trùng lặp."""
    semantic_results = semantic_search(
        target_collection,
        query,
        top_k=top_k,
        where=where
    )

    keyword_results = keyword_search(chunk_records, query)

    combined_texts = list(dict.fromkeys(
        [item["text"] for item in semantic_results] + keyword_results
    ))

    return rerank_results(combined_texts, query, top_k=top_k)


# ============================================================
# 7. RERANKING
# ============================================================

def rerank_results(
    documents: list[str],
    query: str,
    top_k: int = 4
) -> list[dict[str, Any]]:
    """Xếp hạng đơn giản dựa trên số từ khóa xuất hiện trong chunk."""
    keywords = [
        word.lower()
        for word in query.split()
        if len(word.strip()) > 1
    ]

    ranked_results = []

    for document in documents:
        score = sum(
            keyword in document.lower()
            for keyword in keywords
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


# ============================================================
# 8. CONTEXT BUILDING
# ============================================================

def build_context(
    search_results: list[dict[str, Any]]
) -> str:
    """Ghép kết quả tìm kiếm thành context cho LLM."""
    return "\n\n".join(
        result["text"] for result in search_results
    )


# ============================================================
# 9. GENERATION
# ============================================================

def generate_answer(question: str, context: str) -> str:
    """Yêu cầu LLM trả lời dựa trên context được truy xuất."""
    if not context.strip():
        return "Không tìm thấy thông tin phù hợp trong dữ liệu đã index."

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Bạn là trợ lý hỏi đáp về công nghệ. "
                    "Chỉ sử dụng thông tin trong CONTEXT để trả lời. "
                    "Nếu context không đủ thông tin, hãy nói rõ "
                    "rằng chưa tìm thấy thông tin trong dữ liệu. "
                    "Không tự bịa dữ kiện."
                )
            },
            {
                "role": "user",
                "content": (
                    f"CONTEXT:\n{context}\n\n"
                    f"QUESTION:\n{question}"
                )
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content or ""


# ============================================================
# 10. COMPLETE RAG PIPELINE
# ============================================================

def rag_pipeline(
    question: str,
    chunk_records: list[dict[str, Any]],
    top_k: int = 4,
    where: dict | None = None
) -> str:
    """Chạy toàn bộ quy trình: search -> rerank -> context -> answer."""
    search_results = hybrid_search(
        target_collection=collection,
        query=question,
        chunk_records=chunk_records,
        top_k=top_k,
        where=where
    )

    context = build_context(search_results)

    return generate_answer(question, context)


def calculate_file_hash(content: str) -> str:
    """Tạo SHA-256 hash từ nội dung tài liệu."""

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

def load_txt_document(file_path: str) -> dict:
    """Đọc nội dung file TXT và tạo SHA-256 hash."""

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return {
        "id": os.path.basename(file_path),
        "category": "technology",
        "text": content,
        "file_hash": calculate_file_hash(content)
    }


def load_txt_directory(directory_path: str) -> list[dict]:
    """Đọc tất cả file TXT trong một thư mục."""

    documents = []

    directory = Path(directory_path)

    for file_path in directory.glob("*.txt"):
        document = load_txt_document(str(file_path))
        documents.append(document)

    print(f"Đã load {len(documents)} tài liệu.")

    return documents


def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return {}

    with open(MANIFEST_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_manifest(manifest):
    temp_path = MANIFEST_PATH + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4, ensure_ascii=False)

    os.replace(temp_path, MANIFEST_PATH)

def detect_document_changes(documents, old_manifest):
    new_files = []
    changed_files = []
    unchanged_files = []

    for document in documents:
        filename = document["id"]
        current_hash = document["file_hash"]

        old_hash = old_manifest.get(filename)

        if old_hash is None:
            new_files.append(document)

        elif old_hash != current_hash:
            changed_files.append(document)

        else:
            unchanged_files.append(document)

    return new_files, changed_files, unchanged_files

def delete_document_chunks(target_collection, filename):
    results = target_collection.get(
        where={"source": filename},
        include=["metadatas"]
    )

    chunk_ids = results["ids"]

    if chunk_ids:
        target_collection.delete(ids=chunk_ids)
        print(f"Đã xóa {len(chunk_ids)} chunks của {filename}.")


def incremental_sync(target_collection, documents, chunk_size=35, overlap=5):
    old_manifest = load_manifest()

    new_files, changed_files, unchanged_files = detect_document_changes(
        documents, old_manifest
    )

    current_files = {document["id"] for document in documents}
    deleted_files = set(old_manifest.keys()) - current_files

    print("\n=== SYNC REPORT ===")
    print("New:", [doc["id"] for doc in new_files])
    print("Changed:", [doc["id"] for doc in changed_files])
    print("Unchanged:", [doc["id"] for doc in unchanged_files])
    print("Deleted:", list(deleted_files))

    # 1. Xóa chunks của những file đã bị xóa
    for filename in deleted_files:
        delete_document_chunks(target_collection, filename)
        del old_manifest[filename]

    # 2. Chỉ index file mới hoặc file đã thay đổi
    files_to_index = new_files + changed_files

    for document in files_to_index:
        filename = document["id"]

        # Xóa chunks cũ trước khi index lại
        delete_document_chunks(target_collection, filename)

        chunk_records = create_chunk_records(
            [document],
            chunk_size=chunk_size,
            overlap=overlap
        )

        if chunk_records:
            index_documents(target_collection, chunk_records)

        old_manifest[filename] = document["file_hash"]

    # 3. Lưu Manifest
    save_manifest(old_manifest)

    # 4. Lấy toàn bộ chunks hiện có để phục vụ RAG
    stored_data = target_collection.get(
        include=["documents", "metadatas"]
    )

    all_chunk_records = []

    for index, chunk_id in enumerate(stored_data["ids"]):
        all_chunk_records.append({
            "id": chunk_id,
            "text": stored_data["documents"][index],
            "metadata": stored_data["metadatas"][index]
        })

    print("\nĐồng bộ hoàn tất.")
    print(f"Tổng số chunks hiện tại: {len(all_chunk_records)}")

    return all_chunk_records



# EVALUATION_DATASET = [
#     {
#         "question": "OpenAI phát triển công nghệ gì?",
#         "expected_sources": ["ai_news.txt"]
#     },
#     {
#         "question": "NVIDIA sản xuất sản phẩm gì?",
#         "expected_sources": ["gpu_news.txt"]
#     },
#     {
#         "question": "Google phát triển công nghệ gì?",
#         "expected_sources": ["google_news.txt"]
#     }
# ]


EVALUATION_DATASET = [
    {
        "question": "OpenAI phát triển công nghệ gì?",
        "relevant_sources": ["ai_news.txt"]
    },
    {
        "question": "NVIDIA sản xuất sản phẩm gì?",
        "relevant_sources": ["gpu_news.txt"]
    },
    {
        "question": "Google phát triển công nghệ gì?",
        "relevant_sources": ["google_news.txt"]
    }
]



def evaluate_retrieval_metrics(
    collection,
    evaluation_dataset,
    top_k=4
):
    total_precision = 0
    total_recall = 0
    total_f1 = 0

    for item in evaluation_dataset:
        question = item["question"]
        relevant_sources = set(item["relevant_sources"])

        results = semantic_search(
            collection,
            question,
            top_k=top_k
        )

        retrieved_sources = {
            result["metadata"]["source"]
            for result in results
        }

        true_positive = len(
            relevant_sources & retrieved_sources
        )

        precision = (
            true_positive / len(retrieved_sources)
            if retrieved_sources else 0
        )

        recall = (
            true_positive / len(relevant_sources)
            if relevant_sources else 0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0
        )

        total_precision += precision
        total_recall += recall
        total_f1 += f1

        print(f"\nQuestion: {question}")
        print(f"Relevant: {relevant_sources}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Precision: {precision:.2%}")
        print(f"Recall: {recall:.2%}")
        print(f"F1-score: {f1:.2%}")

    count = len(evaluation_dataset)

    if count:
        print("\n=== AVERAGE METRICS ===")
        print(f"Precision: {total_precision / count:.2%}")
        print(f"Recall: {total_recall / count:.2%}")
        print(f"F1-score: {total_f1 / count:.2%}")


def evaluate_retrieval(collection, evaluation_dataset, top_k=4):
    total = len(evaluation_dataset)
    successful = 0

    for item in evaluation_dataset:
        question = item["question"]
        expected_sources = item["expected_sources"]

        results = semantic_search(
            collection,
            question,
            top_k=top_k
        )

        retrieved_sources = {
            result["metadata"]["source"]
            for result in results
        }

        is_correct = bool(
            set(expected_sources) & retrieved_sources
        )

        if is_correct:
            successful += 1

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_sources}")
        print(f"Retrieved: {list(retrieved_sources)}")
        print(f"Result: {'PASS' if is_correct else 'FAIL'}")

    accuracy = successful / total if total else 0

    print(f"\nRetrieval Accuracy: {accuracy:.2%}")


# ============================================================
# 11. DEMO
# ============================================================

# if __name__ == "__main__":

#     # 1. Load documents
#     documents = load_txt_directory("documents")

#     print("\n=== FILE HASHES ===")

#     for document in documents:
#         print(f"File: {document['id']}")
#         print(f"Hash: {document['file_hash']}")

#     # 2. Synchronize documents
#     chunk_records = sync_documents(
#         collection,
#         documents,
#         chunk_size=35,
#         overlap=5
#     )

#     print(f"Tổng số chunks hiện tại: {len(chunk_records)}")

#     # 3. RAG Pipeline
#     question = "NVIDIA sản xuất sản phẩm gì và dùng để làm gì?"

#     print("\n=== QUESTION ===")
#     print(question)

#     answer = rag_pipeline(
#         question=question,
#         chunk_records=chunk_records,
#         top_k=4
#     )

#     print("\n=== ANSWER ===")
#     print(answer)


# if __name__ == "__main__":
#     manifest = load_manifest()
#     print("Manifest hiện tại:", manifest)

#     test_manifest = {
#         "ai_news.txt": "abc123",
#         "gpu_news.txt": "def456"
#     }

#     save_manifest(test_manifest)
#     print("Đã lưu manifest.")

#     print("Đọc lại:", load_manifest())

# if __name__ == "__main__":
#     documents = load_txt_directory("documents")
#     old_manifest = load_manifest()

#     new_files, changed_files, unchanged_files = detect_document_changes(
#         documents, old_manifest
#     )

#     print("New files:", [doc["id"] for doc in new_files])
#     print("Changed files:", [doc["id"] for doc in changed_files])
#     print("Unchanged files:", [doc["id"] for doc in unchanged_files])


# if __name__ == "__main__":
#     documents = load_txt_directory("documents")

#     manifest = {
#         document["id"]: document["file_hash"]
#         for document in documents
#     }

#     save_manifest(manifest)

#     print("Đã khởi tạo Manifest:")
#     print(load_manifest())


if __name__ == "__main__":
    # 1. Load tài liệu
    # documents = load_txt_directory("documents")

    # # 2. Incremental Sync
    # chunk_records = incremental_sync(
    #     collection,
    #     documents,
    #     chunk_size=35,
    #     overlap=5
    # )

    # # 3. Đặt câu hỏi
    # question = "NVIDIA sản xuất sản phẩm gì và dùng để làm gì?"

    # # 4. Chạy RAG Pipeline
    # answer = rag_pipeline(
    #     question=question,
    #     chunk_records=chunk_records,
    #     top_k=4
    # )

    # print("\n=== FINAL ANSWER ===")
    # print(answer)
    # evaluate_retrieval(
    # collection=collection,
    # evaluation_dataset=EVALUATION_DATASET,
    # top_k=4
    # )


    # evaluate_retrieval_metrics(
    #     collection=collection,
    #     evaluation_dataset=EVALUATION_DATASET,
    #     top_k=4
    # )



    # for k in [1, 2, 3, 4]:
    #     print(f"\n{'=' * 15} TOP K = {k} {'=' * 15}")

    #     evaluate_retrieval_metrics(
    #         collection=collection,
    #         evaluation_dataset=EVALUATION_DATASET,
    #         top_k=k
    #     )



    
    for threshold in [0.3, 0.5, 0.7, 1.0]:
        print(f"\n{'=' * 15} THRESHOLD = {threshold} {'=' * 15}")

        for item in EVALUATION_DATASET:
            results = semantic_search(
                collection,
                item["question"],
                top_k=4,
                threshold=threshold
            )

            print(f"\nQuestion: {item['question']}")
            print(f"Retrieved chunks: {len(results)}")

            for result in results:
                print(
                    f"Source: {result['metadata']['source']} | "
                    f"Distance: {result['distance']:.4f}"
                )

