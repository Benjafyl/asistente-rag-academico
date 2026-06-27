import requests

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.retriever import RetrievedChunk


NO_CONTEXT_MESSAGE = (
    "No encontre informacion suficiente en los documentos proporcionados "
    "para responder esta pregunta."
)


def fallback_answer(chunks: list[RetrievedChunk]) -> str:
    context_preview = " ".join(chunk.text.replace("\n", " ") for chunk in chunks[:2])
    sentences = [part.strip() for part in context_preview.split(".") if part.strip()]
    summary = ". ".join(sentences[:3]).strip()
    if not summary:
        return NO_CONTEXT_MESSAGE
    return (
        "Ollama tardo demasiado en generar la respuesta. "
        f"Segun los fragmentos recuperados: {summary}."
    )


def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context = "\n\n".join(
        f"Fuente: {chunk.source} | Fragmento: {chunk.chunk}\n{chunk.text}"
        for chunk in chunks
    )
    return f"""
Eres un asistente academico universitario.
Responde exclusivamente con la informacion del CONTEXTO.
Responde en maximo 6 lineas, de forma directa y sin agregar informacion externa.
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
        "options": {"temperature": 0.1, "num_ctx": 2048, "num_predict": 180},
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=35,
        )
        response.raise_for_status()
    except requests.Timeout:
        return fallback_answer(chunks)
    except requests.RequestException as exc:
        return (
            "No fue posible conectar con Ollama. Verifica que el servicio este "
            f"activo y que el modelo '{OLLAMA_MODEL}' este descargado. Detalle: {exc}"
        )

    answer = response.json().get("response", "").strip()
    return answer or NO_CONTEXT_MESSAGE
