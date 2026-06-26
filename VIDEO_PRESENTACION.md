# Guia para grabar el video de presentacion

Duracion objetivo: 6 minutos. Maximo permitido: 7 minutos.

## Antes de grabar

Abrir una terminal en la raiz del proyecto:

```powershell
cd C:\Users\benja\Desktop\rag-assistant\rag-assistant
.\.venv\Scripts\activate
python ingest.py
streamlit run app.py
```

Abrir la app en:

```text
http://localhost:8501
```

Tener listo el repositorio GitHub:

```text
https://github.com/Benjafyl/asistente-rag-academico
```

## Reparto recomendado

Persona 1: problema, arquitectura e ingesta.

Persona 2: demostracion funcional, fuentes y conclusion.

## Guion por minuto

### 0:00 - 0:30 | Presentacion del proyecto

Persona 1:

Este proyecto implementa un asistente RAG academico. El objetivo es responder preguntas de estudiantes usando documentos institucionales cargados en el sistema, como reglamentos de asistencia, evaluaciones, practicas y titulacion.

Mostrar en pantalla:

- README del repositorio.
- Carpeta `documents/`.

### 0:30 - 1:20 | Problema abordado

Persona 1:

El problema es que la informacion academica suele estar distribuida en varios documentos. Un estudiante puede necesitar saber requisitos de asistencia o titulacion, pero revisar manualmente todos los reglamentos toma tiempo y puede llevar a errores.

Este asistente busca recuperar los fragmentos relevantes y generar una respuesta con fuentes visibles. Si la respuesta no esta en los documentos, el sistema debe reconocerlo.

Mostrar en pantalla:

- `documents/reglamento_asistencia.md`
- `documents/reglamento_titulacion.md`

### 1:20 - 2:40 | Arquitectura RAG

Persona 1:

La arquitectura sigue el flujo RAG: primero se cargan documentos desde archivos, luego se dividen en chunks, despues se generan embeddings y se guardan en ChromaDB. Cuando el usuario hace una pregunta, el sistema genera el embedding de la consulta, recupera los fragmentos mas parecidos y entrega ese contexto al modelo `mistral:7b` usando Ollama.

Mencionar obligatoriamente:

- Ingesta documental desde `documents/`.
- Chunking de 900 caracteres con 180 de overlap.
- Embeddings con `all-MiniLM-L6-v2`.
- Base vectorial ChromaDB en `chroma_db/`.
- LLM local `mistral:7b` via Ollama.
- Fuentes visibles en la interfaz.

Mostrar en pantalla:

- `src/config.py`
- `src/vector_store.py`
- `src/retriever.py`
- `src/llm.py`

### 2:40 - 3:10 | Ingesta

Persona 1:

Ejecutar o mostrar:

```powershell
python ingest.py
```

Decir:

La ingesta procesa los documentos academicos y genera la base vectorial. En esta prueba se procesan 5 documentos y se indexan 9 chunks.

### 3:10 - 5:40 | Demostracion funcional

Persona 2:

Abrir Streamlit:

```powershell
streamlit run app.py
```

Mostrar la app y probar estas tres preguntas.

Consulta simple:

```text
Cual es el porcentaje minimo de asistencia?
```

Explicar:

La respuesta debe indicar 75% y mostrar como fuente el reglamento de asistencia.

Consulta compleja:

```text
Que requisitos debo cumplir para titularme y que sucede si no los cumplo?
```

Explicar:

La respuesta debe combinar requisitos de titulacion y practica profesional, mostrando los documentos recuperados como fuentes.

Consulta sin respuesta:

```text
Cual es la capital de Japon?
```

Explicar:

Esta pregunta no pertenece al corpus academico, por eso el sistema responde que no encontro informacion suficiente. Esto demuestra que no inventa respuestas externas a los documentos.

Mostrar en pantalla:

- Respuesta generada.
- Panel de fuentes utilizadas.
- Score de relevancia.
- Fragmentos recuperados abriendo al menos un expander de fuentes.

### 5:40 - 6:30 | Ventajas y limitaciones

Persona 2:

RAG permite usar documentos propios sin reentrenar un modelo. La ventaja principal es que las respuestas son trazables, porque se pueden mostrar fuentes. La limitacion es que depende de la calidad del corpus y de la recuperacion: si el documento no existe o esta mal escrito, el asistente no puede responder bien.

Tambien es importante aclarar que el sistema es un apoyo para orientar al estudiante, pero no reemplaza la validacion formal de coordinacion academica.

### 6:30 - 7:00 | Cierre

Persona 2:

Cerrar mostrando el repositorio GitHub y decir:

El repositorio incluye codigo fuente, dependencias, documentos, README, informe breve, evidencia de pruebas y capturas de la app funcionando.

## Checklist del video

- [ ] Mostrar repositorio GitHub.
- [ ] Mostrar carpeta `documents/`.
- [ ] Mostrar `python ingest.py`.
- [ ] Mostrar `streamlit run app.py`.
- [ ] Probar pregunta simple.
- [ ] Probar pregunta compleja.
- [ ] Probar pregunta sin respuesta documental.
- [ ] Mostrar fuentes recuperadas.
- [ ] Mencionar embeddings.
- [ ] Mencionar ChromaDB.
- [ ] Mencionar Ollama y `mistral:7b`.
- [ ] Mencionar ventajas y limitaciones de RAG.

## Recomendaciones practicas

- Grabar pantalla completa con audio de ambos.
- No leer todo el codigo, solo mostrar los archivos clave.
- No gastar mas de 30 segundos en instalacion.
- Tener la app abierta antes de grabar por si el modelo demora en responder.
- Si una respuesta tarda, explicar brevemente que Ollama ejecuta el modelo localmente.
- Revisar que el video final dure menos de 7 minutos antes de subirlo a Canvas.
