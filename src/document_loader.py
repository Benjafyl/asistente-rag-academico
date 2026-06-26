from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}


@dataclass(frozen=True)
class Document:
    source: str
    text: str


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"[Pagina {index}]\n{text}")
    return "\n\n".join(pages)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(documents_dir: Path) -> list[Document]:
    documents_dir.mkdir(parents=True, exist_ok=True)
    documents: list[Document] = []

    for path in sorted(documents_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = _read_pdf(path) if path.suffix.lower() == ".pdf" else _read_text(path)
        clean_text = text.strip()
        if clean_text:
            documents.append(Document(source=path.name, text=clean_text))

    return documents
