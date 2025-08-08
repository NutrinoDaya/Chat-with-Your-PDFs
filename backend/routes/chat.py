from fastapi import APIRouter, HTTPException
from services.embedder import model
from services.vector_store import VectorStore
from services.qdrant_store import QdrantVectorStore
from services.llm import ask_llm
from utils.config import get_config
from models.chat import ChatRequest
import os

router = APIRouter()

# Load configuration
config = get_config()
USE_QDRANT = config.get("use_qdrant", False)
EMBED_DIM = config.get("embed_dim", 384)
VECTOR_STORE_ROOT = config.get("vector_store_root", "vector_store_data")
QDRANT_HOST = config.get("qdrant", {}).get("host")
QDRANT_PORT = config.get("qdrant", {}).get("port")
@router.post("/")
def chat(request: ChatRequest):
    question = request.question.strip()
    doc_id = request.document_id

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        if USE_QDRANT:
            vector_store = QdrantVectorStore(
                collection_name=doc_id,
                dim=EMBED_DIM,
                host=QDRANT_HOST,
                port=QDRANT_PORT
            )
            query_embedding = model.encode([question], convert_to_numpy=True, normalize_embeddings=True)[0]
            top_chunks = vector_store.search(query_embedding=query_embedding, top_k=5)
        else:
            vector_store_path = os.path.join(VECTOR_STORE_ROOT, doc_id)
            if not os.path.exists(vector_store_path):
                raise HTTPException(status_code=404, detail="Document vector store not found.")

            vector_store = VectorStore(dim=EMBED_DIM)
            vector_store.load(vector_store_path)
            query_embedding = model.encode([question], convert_to_numpy=True, normalize_embeddings=True)[0]
            top_chunks = vector_store.search(query_embedding, top_k=5)

        if not top_chunks:
            raise HTTPException(status_code=404, detail="No relevant context found.")

        context = "\n".join([chunk for chunk, _ in top_chunks])
        answer = ask_llm(context=context, question=question)

        return {
            "question": question,
            "answer": answer,
            "context": [
                {"text": chunk, "score": float(score)} for chunk, score in top_chunks
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")
