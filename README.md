
# PDF-QA Chatbot with Local LLM (llama3)  
A web application to upload PDFs, embed their content into vector stores (Qdrant), and interactively ask questions answered by a local LLM (Ollama) based on PDF content.

---

## Features
- Upload PDF documents and extract text chunks
- Generate embeddings with a pre-trained embedder
- Store embeddings in a Qdrant vector database per document
- Query vector store to retrieve relevant chunks
- Context-aware question answering via local llama3 model using Ollama API
- React frontend with live chat interface
- FastAPI backend serving API endpoints with CORS support

---

## Tech Stack
- **Backend:** FastAPI, Qdrant, Python
- **Frontend:** React, Vite, Axios
- **Embedding:** Sentence Transformers 
- **LLM:** Local Ollama server running llama3
- **Storage:** Qdrant vector DB + pickled text chunks on disk

---

## Prerequisites

### Hardware
- NVIDIA GPU recommended (RTX 3060 and higher)
- At least 16 GB RAM, 32 GB+ recommended

### Software
- Python 3.8+
- Node.js 16+
- Ollama installed and running locally with llama3 model
- NVIDIA CUDA drivers (for GPU acceleration)
# Start Qdrant locally if installed natively (check their repo)
- Qdrant (install with `pip install qdrant-client` or run via Docker)

---

## Setup

### 1. Clone the repo  
```bash
git clone https://github.com/NutrinoDaya/chat-with-your-pdf.git
cd chat-with-your-pdf
```

### 2. Backend Setup  
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup  
```bash
cd ../frontend
npm install
```

### 4. Run Ollama (Locally)  
Make sure Ollama is installed and the llama3 model is pulled.  
```bash
ollama pull llama3
ollama run llama3
```

### 5. Run Qdrant Locally

#### Option 1: Using Docker
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

#### Option 2: Native Python (No Docker)
```bash
pip install qdrant-client
# Start Qdrant locally if installed natively (check their docs)
```

---

## Running the Project

### Start Backend  
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend  
```bash
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173`

---

## Usage

1. Upload a PDF via the frontend UI  
2. Wait for the PDF to be processed and embedded (a document ID is generated)  
3. Ask questions about the PDF content in the chatbox  
4. Answers are generated based on retrieved vector chunks using your local LLM  

---

## Project Structure

```
/
├── backend/
│   ├── main.py           # FastAPI app entrypoint
│   ├── routes/
│   │   ├── pdf.py        # PDF upload & processing endpoints
│   │   └── chat.py       # Chat endpoint querying LLM
│   ├── services/
│   │   ├── embedder.py   # Embedding model wrapper
│   │   ├── qdrant_store.py # Qdrant vector store wrapper
│   │   ├── llm.py        # Ollama LLM API interface
│   │   └── pdf_processor.py # PDF text extraction & chunking
│   └── vector_store_data/  # Stored chunks per doc
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   └── FileUploader.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── vite.config.js
└── README.md
```

---

## Error Handling & Debugging

- **Ollama connection issues:**  
  Backend returns error if Ollama is unreachable or model not running.  
  Make sure Ollama service is running on `http://localhost:11434`.

- **Missing document vector store:**  
  Occurs if chat requested for unprocessed or deleted document ID.

- **Empty or no relevant chunks:**  
  Happens when PDF content is too sparse or question unrelated.

---

## License

MIT License © Mohammad Dayarneh

---
