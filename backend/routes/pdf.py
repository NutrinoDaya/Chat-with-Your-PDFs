from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_processor import extract_text_chunks
from services.embedder import embed_chunks
from services.vector_store import VectorStore
from services.qdrant_store import QdrantVectorStore
from utils.config import get_config
import uuid
import os

router = APIRouter()

# Load config
config = get_config()
USE_QDRANT = config.get("use_qdrant", False)
EMBED_DIM = config.get("embed_dim", 384)
VECTOR_STORE_ROOT = config.get("vector_store_root", "vector_store_data")
QDRANT_HOST = config.get("qdrant", {}).get("host", "localhost")
QDRANT_PORT = config.get("qdrant", {}).get("port", 6333)
import hashlib

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        file_bytes = await file.read()

        # Calculate SHA256 hash of file bytes for deduplication
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Use file_hash as document_id to identify duplicates
        document_id = file_hash

        # If already saved locally (for FAISS) or known in Qdrant, skip re-upload
        if USE_QDRANT:
            # Check if collection already exists in Qdrant
            qdrant_store = QdrantVectorStore(
                collection_name=document_id,
                dim=EMBED_DIM,
                host=QDRANT_HOST,
                port=QDRANT_PORT,
            )
            # If collection exists and has points, return early
            if qdrant_store.client.collection_exists(document_id) and qdrant_store.has_points():
                return JSONResponse(
                    content={"message": "Document already uploaded", "document_id": document_id},
                    status_code=200
                )


            chunks = extract_text_chunks(file_bytes)
            if not chunks:
                raise ValueError("No text found in the PDF file.")

            embeddings = embed_chunks(chunks)

            qdrant_store.add(embeddings, chunks)

            # test search right after insert
            test_search_results = qdrant_store.search(embeddings[0], top_k=1)
            print(f"Test search results after insert: {test_search_results}")

            if not test_search_results:
                raise HTTPException(status_code=500, detail="Failed to verify inserted data in Qdrant.")

        else:
            # Local FAISS path
            save_path = os.path.join(VECTOR_STORE_ROOT, document_id)
            if os.path.exists(save_path):
                return JSONResponse(
                    content={"message": "Document already uploaded", "document_id": document_id},
                    status_code=200
                )

            chunks = extract_text_chunks(file_bytes)
            if not chunks:
                raise ValueError("No text found in the PDF file.")

            embeddings = embed_chunks(chunks)
            vector_store = VectorStore(dim=EMBED_DIM)
            vector_store.add(embeddings, chunks)
            vector_store.save(save_path)

        return JSONResponse(
            content={"message": "PDF uploaded and processed successfully", "document_id": document_id},
            status_code=201,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
