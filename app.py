import streamlit as st

from src.chunking import chunk_documents
from src.config import CHUNK_OVERLAP, CHUNK_SIZE, DOCUMENTS_DIR, TOP_K, VECTORSTORE_DIR
from src.document_loader import load_documents
from src.llm import generate_answer
from src.retriever import retrieve
from src.vector_store import build_vector_store, collection_count


st.set_page_config(
    page_title="Asistente RAG Academico",
    page_icon=":material/school:",
    layout="wide",
)


def index_documents() -> tuple[int, int]:
    documents = load_documents(DOCUMENTS_DIR)
    chunks = chunk_documents(documents, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    indexed = build_vector_store(chunks, VECTORSTORE_DIR, reset=True)
    return len(documents), indexed


st.title("Asistente RAG Academico")
st.caption("Respuestas basadas en documentos institucionales de asistencia, evaluacion, practicas y titulacion.")

with st.sidebar:
    st.header("Corpus documental")
    st.write(f"Carpeta: `{DOCUMENTS_DIR.name}/`")
    st.write(f"Chunks indexados: **{collection_count(VECTORSTORE_DIR)}**")

    if st.button("Procesar documentos", use_container_width=True):
        with st.spinner("Generando embeddings e indexando documentos..."):
            docs_count, chunks_count = index_documents()
        st.success(f"Procesados {docs_count} documentos y {chunks_count} chunks.")

    st.divider()
    st.write("Modelo de embeddings:")
    st.code("all-MiniLM-L6-v2", language="text")
    st.write("LLM local esperado:")
    st.code("mistral:7b via Ollama", language="text")

question = st.text_input(
    "Pregunta academica",
    placeholder="Ejemplo: Cual es el porcentaje minimo de asistencia?",
)

left, right = st.columns([1.05, 0.95])

with left:
    if st.button("Responder", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Escribe una pregunta para consultar el corpus.")
        else:
            with st.spinner("Recuperando contexto y generando respuesta..."):
                chunks = retrieve(question, VECTORSTORE_DIR, top_k=TOP_K)
                answer = generate_answer(question, chunks)

            st.subheader("Respuesta")
            st.write(answer)
            st.session_state["last_chunks"] = chunks

with right:
    st.subheader("Fuentes utilizadas")
    chunks = st.session_state.get("last_chunks", [])
    if not chunks:
        st.info("Las fuentes apareceran despues de realizar una consulta.")
    for chunk in chunks:
        with st.expander(
            f"{chunk.source} | fragmento {chunk.chunk} | relevancia {chunk.score:.2f}"
        ):
            st.write(chunk.text)
