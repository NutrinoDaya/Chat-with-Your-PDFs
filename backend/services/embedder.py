from typing import List 
from sentence_transformers import SentenceTransformer
import numpy as np 

# Load model globally once
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Embed a list of text chunks using a pretrained SentenceTransformer
    
    Args: 
        chunks (List[str]): A list of text chunks to embed.
    
    Returns:
        List[List[float]]: A list of embeddings (as lists of floats).
    """
    if not chunks: 
        return [] 
    
    try:
        # FIXED: Typo in argument name 'convert_to_numpy' (was 'convert_to_numby')
        embeddings = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()
    except Exception as e:
        raise RuntimeError(f"Failed to embed chunks: {str(e)}")
