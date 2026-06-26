from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
VECTORSTORE_DIR = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "academic_docs"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180

TOP_K = 4
MIN_RELEVANCE_SCORE = 0.42

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral:7b"
