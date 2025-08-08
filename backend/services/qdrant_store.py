from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from typing import List, Tuple
import uuid
import os
import pickle


class QdrantVectorStore:
    def __init__(self, collection_name: str, dim: int, host="localhost", port=6333):
        self.collection_name = collection_name
        self.dim = dim
        self.client = QdrantClient(host=host, port=port)

        self._ensure_collection()

    def _ensure_collection(self):
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE),
            )

    def has_points(self) -> bool:
        points, _ = self.client.scroll(collection_name=self.collection_name, limit=1)
        return len(points) > 0



    def add(self, embeddings: List[List[float]], chunks: List[str]):
        """
        Add embeddings and their corresponding text chunks to Qdrant collection.

        Args:
            embeddings (List[List[float]]): List of embedding vectors.
            chunks (List[str]): Corresponding text for each vector.
        """
        points = []
        for emb, chunk in zip(embeddings, chunks):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"text": chunk}
            ))

        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search top-k similar text chunks using the query embedding.

        Args:
            query_embedding (List[float]): Query vector.
            top_k (int): Number of top results to return.

        Returns:
            List of tuples (chunk text, similarity score).
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
        )

        return [(hit.payload["text"], hit.score) for hit in results]

    def delete_collection(self):
        """
        Deletes the entire Qdrant collection.
        """
        self.client.delete_collection(collection_name=self.collection_name)

    def save_chunks(self, document_id: str, chunks: List[str]):
        """
        Persist chunks to disk (optional backup).
        """
        os.makedirs("vector_store_data", exist_ok=True)
        path = os.path.join("vector_store_data", f"{document_id}_chunks.pkl")
        with open(path, "wb") as f:
            pickle.dump(chunks, f)

    def load_chunks(self, document_id: str) -> List[str]:
        """
        Load stored chunks for a document (if needed).
        """
        path = os.path.join("vector_store_data", f"{document_id}_chunks.pkl")
        with open(path, "rb") as f:
            return pickle.load(f)
