# Informe breve: Asistente RAG Academico

## 1. Descripcion del problema

Los estudiantes suelen consultar informacion academica en reglamentos, calendarios y documentos de carrera. Cuando esos documentos estan separados, una respuesta simple puede requerir revisar varias fuentes. El problema abordado es construir un asistente que responda preguntas academicas usando solamente documentos institucionales cargados en el sistema.

El asistente se enfoca en consultas sobre asistencia, evaluaciones, practicas profesionales, titulacion y calendario academico. La solucion busca entregar respuestas trazables: no solo responde, tambien muestra los fragmentos recuperados y el documento de origen.

## 2. Tecnologias utilizadas

La interfaz fue desarrollada con Streamlit. Para generar embeddings se uso Sentence Transformers con el modelo `all-MiniLM-L6-v2`. Los vectores se almacenan en ChromaDB, una base vectorial persistente. La generacion de respuestas se integra con Ollama usando el modelo local `mistral:7b`.

## 3. Flujo de funcionamiento

Primero, el sistema lee los archivos de la carpeta `documents/`. Luego divide cada documento en fragmentos de 900 caracteres con 180 caracteres de solapamiento. Cada fragmento se transforma en un embedding y se guarda en ChromaDB dentro de `chroma_db/`.

Cuando el usuario escribe una pregunta, el sistema genera el embedding de esa consulta y recupera los fragmentos mas parecidos. Esos fragmentos se envian al LLM junto con la pregunta. El prompt obliga al modelo a responder solo con el contexto recuperado. Si no hay resultados relevantes, la app responde que no encontro informacion suficiente en los documentos.

## 4. Capturas de pantalla

Las capturas reales generadas para la evidencia quedaron en `output/playwright/`:

- Pantalla principal: `output/playwright/01_inicio.png`
- Consulta simple de asistencia: `output/playwright/02_consulta_asistencia.png`
- Consulta compleja de titulacion: `output/playwright/03_consulta_titulacion.png`
- Consulta sin respuesta documental: `output/playwright/04_consulta_sin_respuesta.png`

Si el informe debe entregarse en PDF o Word, insertar esas imagenes en esta seccion antes de exportar.

## 5. Dificultades encontradas

La principal dificultad fue equilibrar el tamano de los chunks. Un fragmento demasiado pequeno puede separar reglas que se necesitan juntas; uno demasiado grande puede reducir la precision de la recuperacion. Se eligio un tamano intermedio para conservar secciones completas de reglamento.

Otra dificultad fue controlar preguntas fuera del corpus. Un LLM puede intentar contestar con conocimiento general, por eso se agrego un umbral de relevancia y un mensaje fijo cuando no hay contexto suficiente. Tambien fue necesario considerar compatibilidad en Windows, especialmente con ChromaDB y Python 3.13.

## 6. Reflexion sobre ventajas y limitaciones de RAG

RAG es util porque permite usar documentos propios sin entrenar un modelo desde cero. En este proyecto, eso ayuda a responder preguntas academicas con respaldo y fuentes visibles. La respuesta es mas facil de revisar porque el usuario puede ver que documento se recupero.

La limitacion es que la calidad depende directamente del corpus y de la recuperacion. Si un reglamento no esta cargado, esta mal escrito o queda dividido de forma poco clara, el asistente puede no encontrar la respuesta. RAG tampoco reemplaza la validacion humana en temas administrativos importantes; funciona mejor como apoyo inicial para orientar al estudiante.
