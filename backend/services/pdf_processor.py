import fitz # PyMUPDF
from typing import List 


def extract_text_chunks(pdf_bytes: bytes, max_chunk_size: int = 500) -> List[str]:
    """
    Extract text frp, PDF and splits it into manageable chunks
    
    Args: 
        pdf_bytes (bytes): The bytes of the PDF file.
        max_chunk_size (int): The maximum size of each text chunk.
    
    Returns: 
        List[str]: A list of text chunks extracted from the PDF.
    """

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc: 
            full_text += page.get_text()
        doc.close()

        # Split text into cleaned paragraphs (non-empty lines)
        paragraphs = [p.strip() for p in full_text.split("\n") if len(p.strip()) > 0]

        chunks = []
        current_chunk = ""

        # Merge paragraphs into chunks while respecting the max_chunk_size
        for para in paragraphs: 
            if len(current_chunk) + len(para) < max_chunk_size:
                current_chunk += " " + para 
            else: 
                chunks.append(current_chunk.strip())
                current_chunk = para 

        # Add the last chunk if it exists to the final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    except:
        raise ValueError("Failed to extract text from PDF")