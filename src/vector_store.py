from pathlib import Path

import chromadb
from chromadb.config import Settings

from src.chunking import Chunk
from src.config import COLLECTION_NAME
from src.embeddings import embed_texts


def get_client(persist_dir: Path) -> chromadb.PersistentClient:
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(persist_dir),
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection(persist_dir: Path):
    client = get_client(persist_dir)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def build_vector_store(chunks: list[Chunk], persist_dir: Path, reset: bool = True) -> int:
    client = get_client(persist_dir)

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    if not chunks:
        return 0

    texts = [chunk.text for chunk in chunks]
    collection.add(
        ids=[chunk.id for chunk in chunks],
        documents=texts,
        metadatas=[chunk.metadata for chunk in chunks],
        embeddings=embed_texts(texts),
    )
    return len(chunks)


def collection_count(persist_dir: Path) -> int:
    collection = get_collection(persist_dir)
    return collection.count()
