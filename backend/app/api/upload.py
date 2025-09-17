from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.document import Document
from app.utils.file_loader import (
    extract_text_from_pdf_bytes,
    upload_file
)
from app.services.chunking import chunk_text
from app.services.vector_store import upsert_texts
from fastapi import HTTPException
from app.services.vector_store import delete_document_vectors
from app.utils.file_loader import delete_file


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 1️⃣ Read file into memory
    file_bytes = file.file.read()

    # 2️⃣ Upload to Supabase Storage
    storage_path = upload_file(
        file_bytes=file_bytes,
        filename=file.filename
    )

    # 3️⃣ Extract text from bytes (NO local disk)
    text = extract_text_from_pdf_bytes(file_bytes)

    # 4️⃣ Chunk text
    chunks = chunk_text(
        text=text,
        doc_type="general",
        purpose="qa"
    )

    # 5️⃣ Store document metadata in DB
    doc = Document(
        filename=file.filename,
        owner_id=user.id,
        storage_path=storage_path
    )
    db.add(doc)
    db.commit()
    # db.refresh(doc)

    # 6️⃣ Pinecone namespace (per-user isolation)
    namespace = f"user_{user.id}"

    metadatas = [
        {
            "document_id": doc.id,
            "chunk_index": idx,
            "filename": file.filename,
        }
        for idx in range(len(chunks))
    ]

    # 7️⃣ Upsert chunks to Pinecone
    upsert_texts(
        texts=chunks,
        metadatas=metadatas,
        namespace=namespace
    )

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "num_chunks": len(chunks),
        "sample_chunk": chunks[0][:300] if chunks else "",
        "storage_path": storage_path
    }
    
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 1️⃣ Fetch document
    doc = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2️⃣ Ownership check (RBAC)
    if doc.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    namespace = f"user_{user.id}"

    try:
        # 3️⃣ Delete vectors from Pinecone
        delete_document_vectors(
            document_id=doc.id,
            namespace=namespace
        )

        # 4️⃣ Delete file from Supabase Storage
        delete_file(doc.storage_path)

        # 5️⃣ Delete DB row
        db.delete(doc)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }
