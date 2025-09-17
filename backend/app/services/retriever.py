from pinecone import Pinecone
from app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

# ---- Dense index (required) ----
dense_index = pc.Index(host=settings.pinecone_index_host)

# ---- Sparse index (optional) ----
sparse_index = None
if hasattr(settings, "pinecone_sparse_index_host") and settings.pinecone_sparse_index_host:
    sparse_index = pc.Index(host=settings.pinecone_sparse_index_host)

# ---- Toggle (semantic-only by default) ----
USE_HYBRID = True


def retrieve_chunks(
    query: str,
    namespace: str,
    top_k: int = 5
):
    """
    Returns:
      contexts: List[str]
      sources: List[{filename, chunk_index, score}]
    """

    # ---------- SEMANTIC SEARCH (always runs) ----------
    dense_response = dense_index.search(
        namespace=namespace,
        query={
            "inputs": {"text": query},
            "top_k": top_k if not USE_HYBRID else top_k * 4
        },
        fields=["text", "filename", "chunk_index"]
    )

    dense_hits = dense_response.get("result", {}).get("hits", [])

    all_hits = dense_hits

    # ---------- SPARSE SEARCH (only if enabled & exists) ----------
    if USE_HYBRID and sparse_index is not None:
        sparse_response = sparse_index.search(
            namespace=namespace,
            query={
                "inputs": {"text": query},
                "top_k": top_k * 4
            },
            fields=["text", "filename", "chunk_index"]
        )

        sparse_hits = sparse_response.get("result", {}).get("hits", [])
        all_hits = dense_hits + sparse_hits

    # ---------- MERGE & DEDUPLICATE ----------
    merged = {}

    for hit in all_hits:
        _id = hit["_id"]
        score = hit.get("_score", 0.0)
        fields = hit.get("fields", {})

        if "text" not in fields:
            continue

        if _id not in merged or merged[_id]["score"] < score:
            merged[_id] = {
                "text": fields["text"],
                "filename": fields.get("filename", "unknown"),
                "chunk_index": fields.get("chunk_index", -1),
                "score": score,
            }

    # ---------- SORT & TRIM ----------
    ranked = sorted(
        merged.values(),
        key=lambda x: x["score"],
        reverse=True
    )[:top_k]

    # ---------- FINAL OUTPUT (UNCHANGED FORMAT) ----------
    contexts = [r["text"] for r in ranked]

    sources = [
        {
            "filename": r["filename"],
            "chunk_index": r["chunk_index"],
            "score": r["score"],
        }
        for r in ranked
    ]

    return contexts, sources
