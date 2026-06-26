from src.chunking import chunk_documents
from src.config import CHUNK_OVERLAP, CHUNK_SIZE, DOCUMENTS_DIR, VECTORSTORE_DIR
from src.document_loader import load_documents
from src.vector_store import build_vector_store


def main() -> None:
    documents = load_documents(DOCUMENTS_DIR)
    chunks = chunk_documents(documents, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    indexed = build_vector_store(chunks, VECTORSTORE_DIR, reset=True)

    print(f"Documentos procesados: {len(documents)}")
    print(f"Chunks indexados: {indexed}")


if __name__ == "__main__":
    main()
