from dataclasses import dataclass

from src.document_loader import Document


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    metadata: dict


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and lower than chunk_size")

    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)

        while len(paragraph) > chunk_size:
            chunks.append(paragraph[:chunk_size].strip())
            paragraph = paragraph[chunk_size - overlap :]

        current = paragraph.strip()

    if current:
        chunks.append(current)

    if overlap == 0 or len(chunks) <= 1:
        return chunks

    overlapped: list[str] = []
    previous_tail = ""
    for chunk in chunks:
        combined = f"{previous_tail}\n{chunk}".strip() if previous_tail else chunk
        overlapped.append(combined[: chunk_size + overlap].strip())
        previous_tail = chunk[-overlap:]

    return overlapped


def chunk_documents(documents: list[Document], chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        parts = _split_text(document.text, chunk_size=chunk_size, overlap=overlap)
        for index, text in enumerate(parts, start=1):
            chunks.append(
                Chunk(
                    id=f"{document.source}::chunk-{index}",
                    text=text,
                    metadata={"source": document.source, "chunk": index},
                )
            )
    return chunks
