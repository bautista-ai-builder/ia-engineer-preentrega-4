# Pre-entrega 4: RAG híbrido en Pinecone

Ingesta PDF, Markdown, texto y JSON; guarda vectores y metadatos en Pinecone Serverless; combina recuperación densa con BM25 mediante `EnsembleRetriever`; calcula Precision@k y Recall@k sobre cinco consultas de referencia.

## Instalación

Requiere Python 3.12+. Crear un entorno virtual e instalar `requirements.txt`. Copiar `.env.example` a `.env`, completar `OPENAI_API_KEY` y `PINECONE_API_KEY` y escoger índice, región y namespace. **Nunca subir `.env`**. El índice debe usar la misma dimensión que el modelo de embeddings; el valor inicial es 1536 para `text-embedding-3-small`. El script crea el índice si falta y verifica su dimensión si ya existe. Pinecone y OpenAI pueden generar consumo o cargos según las cuentas utilizadas.

## Ejecución

```bash
python ingest.py
python chat.py "¿Cuándo se hacen los respaldos?"
python evaluate.py --k 4
pytest -q
```

`data/` contiene un corpus de ejemplo. `documents.py` conserva fuente, página, categoría e identificadores estables; `ingest.py` sube los fragmentos al namespace configurado. `retrieval.py` reconstruye BM25 desde el mismo corpus local y combina sus resultados con Pinecone. Para usar otro corpus, reemplazar `data/`, volver a ingerir y actualizar `golden_set.json`. Los IDs deterministas evitan duplicados al reingerir el mismo contenido; si se elimina un documento del corpus, se debe eliminar manualmente del índice.

El reporte metodológico está en `report/README.md`. `evaluate.py` genera resultados reales en `report/results.json` al conectarse a Pinecone. Los tests verifican carga, metadatos, construcción híbrida y métricas sin llamar a servicios externos.
