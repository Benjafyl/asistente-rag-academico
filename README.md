# Asistente RAG Academico

Proyecto universitario para el laboratorio evaluado "Implementacion de un Asistente RAG". La aplicacion responde consultas academicas usando documentos institucionales ubicados en `documents/`.

## Caso de uso

El caso elegido es un asistente academico universitario. Su objetivo es responder preguntas frecuentes de estudiantes sobre asistencia, evaluaciones, practicas, titulacion y calendario academico. Si la respuesta no esta respaldada por los documentos cargados, el asistente debe reconocer que no tiene informacion suficiente.

## Arquitectura implementada

1. Ingesta documental: carga archivos PDF, TXT, MD y Markdown desde `documents/`.
2. Fragmentacion: divide cada documento en chunks con solapamiento.
3. Embeddings: convierte cada chunk en un vector con Sentence Transformers.
4. Base vectorial: almacena los vectores en ChromaDB dentro de `chroma_db/`.
5. Recuperacion: calcula el embedding de la pregunta y recupera los fragmentos mas similares.
6. Generacion: envia pregunta y contexto recuperado a `mistral:7b` mediante Ollama.
7. Fuentes: muestra documento, fragmento y score de relevancia en Streamlit.
8. Control fuera de contexto: si no hay fragmentos relevantes, responde que no existe informacion suficiente.

## Tecnologias

- Python 3.11 recomendado en Windows.
- Streamlit para la interfaz.
- Sentence Transformers con `all-MiniLM-L6-v2` para embeddings locales.
- ChromaDB como base vectorial persistente.
- PyPDF para lectura de documentos PDF.
- Ollama con `mistral:7b` como LLM local.

## Instalacion en Windows

Crear entorno:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Instalar modelo:

```powershell
ollama pull mistral:7b
```

Ejecutar ingesta:

```powershell
python ingest.py
```

Ejecutar app:

```powershell
streamlit run app.py
```

## Uso esperado

1. Ejecutar `python ingest.py` para indexar los documentos.
2. Ejecutar `streamlit run app.py`.
3. Hacer una pregunta academica.
4. Revisar la respuesta y las fuentes recuperadas en la columna derecha.

Preguntas de demostracion:

- Cual es el porcentaje minimo de asistencia?
- Que requisitos debo cumplir para titularme y que sucede si no los cumplo?
- Cual es la capital de Japon?

La tercera pregunta debe responder que no hay informacion suficiente en los documentos proporcionados.

## Chunk size y overlap

Se usa `CHUNK_SIZE = 900` caracteres y `CHUNK_OVERLAP = 180`. Este tamano permite conservar secciones completas de reglamentos o procedimientos, mientras que el overlap reduce el riesgo de cortar informacion importante entre fragmentos.

## Solucion de problemas

**Error con ChromaDB o `chroma-hnswlib`**

Usar Python 3.11. En Windows, Python 3.12 o 3.13 puede intentar compilar `chroma-hnswlib` y pedir Microsoft C++ Build Tools. Si ya existe un entorno creado con otra version, eliminar `.venv/` y crearlo nuevamente con `py -3.11 -m venv .venv`.

**Python 3.13 incompatible**

Este proyecto esta preparado para Python 3.11. Si `python --version` muestra 3.13, instalar Python 3.11 y crear el entorno con `py -3.11 -m venv .venv`.

**Ollama no encontrado**

Instalar Ollama desde su sitio oficial y abrir una terminal nueva. Validar con:

```powershell
ollama --version
```

**`mistral:7b` no descargado**

Validar modelos instalados con:

```powershell
ollama list
```

Si no aparece `mistral:7b`, descargarlo con:

```powershell
ollama pull mistral:7b
```

**No hay documentos cargados**

Verificar que existan archivos en `documents/` con extension `.md`, `.txt`, `.markdown` o `.pdf`. Luego ejecutar nuevamente:

```powershell
python ingest.py
```

**No aparecen fuentes**

Reindexar con `python ingest.py` o usar el boton "Procesar documentos" en la barra lateral de la app.
