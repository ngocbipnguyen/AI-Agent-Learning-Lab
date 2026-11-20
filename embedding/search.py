import numpy as np

from embedding.embedding_service import create_embedding


def semantic_search(
    query: str,
    embeddings: list[list[float]],
    sentences: list[str],
    top_k: int = 3
) -> list[dict]:

    query_embedding = create_embedding(query)

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

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]