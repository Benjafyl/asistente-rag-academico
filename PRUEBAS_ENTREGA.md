# Pruebas de entrega

Fecha de validacion: 26-06-2026

## Entorno

- Sistema: Windows
- Python global detectado con `python --version`: `Python 3.13.7`
- Python recomendado disponible con `py -3.11 --version`: `Python 3.11.9`
- Entorno usado para pruebas: `.venv` creado con Python 3.11

## Comandos ejecutados

| Comando | Resultado | Estado |
|---|---|---|
| `python --version` | `Python 3.13.7` | OK, pero no recomendado para este proyecto |
| `py -3.11 --version` | `Python 3.11.9` | OK |
| `py -3.11 -m venv .venv` | Entorno creado correctamente | OK |
| `python -m pip install --upgrade pip setuptools wheel` | Herramientas de instalacion actualizadas; `torch` requiere `setuptools<82`, luego `pip install -r requirements.txt` deja `setuptools==81.0.0` | OK |
| `pip install -r requirements.txt` | Dependencias instaladas con Python 3.11 | OK |
| `python -m pip check` | `No broken requirements found.` | OK |
| `python -m compileall app.py ingest.py src` | Codigo del proyecto compila sin errores | OK |
| `ollama --version` | El comando `ollama` no esta en el PATH | Error CLI |
| `ollama list` | El comando `ollama` no esta en el PATH | Error CLI |
| `GET http://localhost:11434/api/tags` | API local responde y muestra `mistral:7b` instalado | OK API |
| `python ingest.py` | `Documentos procesados: 5`, `Chunks indexados: 9` | OK |
| `streamlit run app.py --server.headless true --server.port 8501` | Streamlit inicia y muestra `Local URL: http://localhost:8501` | OK |
| `Invoke-WebRequest http://localhost:8501` | HTTP 200 | OK |

## Validacion de Ollama

El ejecutable `ollama` no esta disponible desde PowerShell, por lo que los comandos `ollama --version` y `ollama list` fallan. Sin embargo, la API local de Ollama responde en `http://localhost:11434/api/tags` y reporta el modelo `mistral:7b`.

Si el equipo donde se presente no tiene ese modelo, ejecutar:

```powershell
ollama pull mistral:7b
```

## Consultas funcionales probadas

### Consulta simple

Pregunta: `Cual es el porcentaje minimo de asistencia?`

Resultado observado: recupera fragmentos de `reglamento_asistencia.md` y responde que la asistencia minima requerida es 75%.

Estado: OK

### Consulta compleja

Pregunta: `Que requisitos debo cumplir para titularme y que sucede si no los cumplo?`

Resultado observado: recupera `reglamento_titulacion.md` y documentos relacionados. La respuesta menciona plan de estudios completo, asignaturas pendientes, practica profesional, deudas documentales y que no se puede rendir la actividad final ni cerrar expediente si faltan requisitos.

Estado: OK

### Consulta sin respuesta documental

Pregunta: `Cual es la capital de Japon?`

Resultado observado: no recupera chunks relevantes y responde: `No encontre informacion suficiente en los documentos proporcionados para responder esta pregunta.`

Estado: OK

## Capturas generadas

Las capturas reales quedaron en:

- `output/playwright/01_inicio.png`
- `output/playwright/02_consulta_asistencia.png`
- `output/playwright/03_consulta_titulacion.png`
- `output/playwright/04_consulta_sin_respuesta.png`

## Capturas que debe revisar el estudiante

- Pantalla principal con chunks indexados.
- Consulta simple con respuesta de asistencia y fuentes.
- Consulta compleja con respuesta de titulacion y fuentes.
- Consulta fuera del contexto con mensaje de informacion insuficiente.

## Checklist final

- [x] `app.py` existe y levanta con Streamlit.
- [x] `ingest.py` existe y genera la base vectorial.
- [x] `requirements.txt` instala con Python 3.11.
- [x] Documentos fuente existen en `documents/`.
- [x] ChromaDB usa carpeta persistente `chroma_db/`.
- [x] La app muestra fuentes, fragmentos y score de relevancia.
- [x] La app maneja preguntas fuera del contexto documental.
- [x] `README.md` tiene instrucciones para Windows.
- [x] `informe_breve.md` esta actualizado con el proyecto real.
- [x] Capturas de evidencia generadas.
- [ ] Verificar manualmente que el comando `ollama` quede disponible en PATH antes de presentar, aunque la API local ya respondio.
