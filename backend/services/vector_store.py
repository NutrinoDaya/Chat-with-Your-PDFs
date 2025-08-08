import faiss
import numpy as np 
import os 
import pickle
from typing import List 


class VectorStore:
    
    """
    Wrapper class for managing FAISS vector index and ssociated text chunks.

    """
    def __init__(self, dim: int):
        """
        Initialize a FAISS index with given embedding dimension
        
        Args:
            dim(int): The dimensionality of the embeddings
        
        """

        self.index = faiss.IndexFlatL2(dim) # L2 distance Index
        self.text_chunks: List[str] = []

    def add(self, embeddings: List[List[float]], chunks: List[str]):
        """
        Add embeddings and their corresponding text chunks to the store

        Args: 
            embeddings (List[List[float]]): List of embeddings to add
            chunks (List[str]): List of text chunks corresponding to the embeddings
        """

        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)
        self.text_chunks.extend(chunks)


    def search(self, query_embedding: List[float], top_k: int = 5):
        query_vec = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue  # Skip invalid index from FAISS
            if idx < len(self.text_chunks):
                results.append((self.text_chunks[idx], dist))

        return results
    
    
    def save(self, path: str) -> None: 
        """
        Persist the FAISS index and text data.

        Args:
            path (str): Directory path to save the index and metadata.
        """

        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "chunks.pkl"), "wb") as f:
            pickle.dump(self.text_chunks, f)
    
    def load(self, path: str) -> None:
        """
        Load FAISS index and text data from disk.

        Args:
            path (str): Directory from which to load data.
        """
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "chunks.pkl"), "rb") as f:
            self.text_chunks = pickle.load(f)