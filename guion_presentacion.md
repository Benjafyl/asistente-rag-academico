# Guion de presentacion: maximo 7 minutos

## 1. Problema abordado: 1 minuto

En este proyecto implemente un asistente RAG academico. El problema es que los estudiantes suelen consultar reglamentos distintos para resolver dudas sobre asistencia, evaluaciones, practicas o titulacion. Si la informacion esta distribuida en varios documentos, responder una consulta puede tomar mas tiempo y es facil omitir un requisito.

## 2. Arquitectura implementada: 2 minutos

La arquitectura sigue el flujo RAG: ingesta documental, fragmentacion, embeddings, base vectorial, recuperacion de contexto y generacion de respuesta. El sistema carga documentos desde `documents/`, soporta PDF, TXT y Markdown, y divide el contenido en chunks de 900 caracteres con 180 de overlap.

Cada chunk se transforma en embedding con Sentence Transformers y se almacena en ChromaDB. Cuando el usuario pregunta algo, el sistema genera el embedding de la consulta, busca los fragmentos mas parecidos y entrega ese contexto al LLM local mediante Ollama, usando `mistral:7b`.

## 3. Demostracion funcional: 3 minutos

Primero muestro la estructura del proyecto. Luego ejecuto `python ingest.py` y despues `streamlit run app.py`.

Consulta simple: `Cual es el porcentaje minimo de asistencia?`

Consulta compleja: `Que requisitos debo cumplir para titularme y que sucede si no los cumplo?`

Consulta sin respuesta documental: `Cual es la capital de Japon?`

En la tercera consulta, el asistente debe decir que no encontro informacion suficiente en los documentos, demostrando que no responde con conocimiento externo al corpus.

## 4. Reflexion y conclusiones: 1 minuto

RAG es util porque permite que un modelo responda usando informacion especifica sin reentrenarlo y mostrando fuentes. La principal limitacion es que la calidad depende del corpus y de la recuperacion. Para un asistente academico, funciona bien como apoyo inicial, pero las decisiones administrativas importantes igual deben validarse con la unidad correspondiente.
