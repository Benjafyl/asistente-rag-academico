import requests

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.retriever import RetrievedChunk


NO_CONTEXT_MESSAGE = (
    "No encontre informacion suficiente en los documentos proporcionados "
    "para responder esta pregunta."
)


def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context = "\n\n".join(
        f"Fuente: {chunk.source} | Fragmento: {chunk.chunk}\n{chunk.text}"
        for chunk in chunks
    )
    return f"""
Eres un asistente academico universitario.
Responde exclusivamente con la informacion del CONTEXTO.
Si el CONTEXTO no contiene la respuesta, responde exactamente:
"{NO_CONTEXT_MESSAGE}"

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
""".strip()


def generate_answer(question: str, chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return NO_CONTEXT_MESSAGE

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": build_prompt(question, chunks),
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 4096},
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return (
            "No fue posible conectar con Ollama. Verifica que el servicio este "
            f"activo y que el modelo '{OLLAMA_MODEL}' este descargado. Detalle: {exc}"
        )

    answer = response.json().get("response", "").strip()
    return answer or NO_CONTEXT_MESSAGE
