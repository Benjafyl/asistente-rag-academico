from dataclasses import dataclass
from pathlib import Path

from src.config import MIN_RELEVANCE_SCORE, TOP_K
from src.embeddings import embed_query
from src.vector_store import get_collection


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    source: str
    chunk: int
    score: float


def retrieve(
    question: str,
    persist_dir: Path,
    top_k: int = TOP_K,
    min_score: float = MIN_RELEVANCE_SCORE,
) -> list[RetrievedChunk]:
    collection = get_collection(persist_dir)
    if collection.count() == 0:
        return []

    result = collection.query(
        query_embeddings=[embed_query(question)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[RetrievedChunk] = []
    for text, metadata, distance in zip(
        result.get("documents", [[]])[0],
        result.get("metadatas", [[]])[0],
        result.get("distances", [[]])[0],
    ):
        score = max(0.0, 1.0 - float(distance))
        if score >= min_score:
            chunks.append(
                RetrievedChunk(
                    text=text,
                    source=str(metadata.get("source", "desconocido")),
                    chunk=int(metadata.get("chunk", 0)),
                    score=score,
                )
            )
    return chunks
