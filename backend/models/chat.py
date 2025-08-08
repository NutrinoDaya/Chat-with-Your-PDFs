from pydantic import BaseModel

# Request body schema
class ChatRequest(BaseModel):
    question: str
    document_id: str