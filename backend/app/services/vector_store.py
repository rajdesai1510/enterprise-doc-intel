from pinecone import Pinecone
from app.core.config import settings
import uuid

pc = Pinecone(api_key=settings.pinecone_api_key)

# ---- Dense index (existing, required) ----
dense_index = pc.Index(
    host=settings.pinecone_index_host
)

# ---- Sparse index (optional, hybrid-ready) ----
sparse_index = None
if hasattr(settings, "pinecone_sparse_index_host") and settings.pinecone_sparse_index_host:
    sparse_index = pc.Index(
        host=settings.pinecone_sparse_index_host
    )

def upsert_texts(
    texts: list[str],
    metadatas: list[dict],
    namespace: str
):
    """
    Upserts texts into dense index (and sparse index if configured).
    Compatible with Pinecone integrated embedding.
    """

    records = []

    for text, metadata in zip(texts, metadatas):
        record = {
            "_id": str(uuid.uuid4()),
            "text": text,   # MUST match Pinecone field_map
            **metadata
        }
        records.append(record)

    # ---- Dense upsert (existing behavior) ----
    dense_index.upsert_records(
        namespace,
        records
    )

    # ---- Sparse upsert (only if index exists) ----
    if sparse_index is not None:
        sparse_index.upsert_records(
            namespace,
            records
        )
def delete_document_vectors(document_id: int, namespace: str):
    """
    Delete all vectors related to a document using metadata filter
    """
    dense_index.delete(
        namespace=namespace,
        filter={
            "document_id": document_id
        }
    )
    if sparse_index is not None:
        sparse_index.delete(
            namespace=namespace,
            filter={
                "document_id": document_id
            }
        )
