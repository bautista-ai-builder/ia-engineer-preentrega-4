# Reporte de evaluación

`python evaluate.py --k 4` genera `results.json` con los identificadores recuperados por pregunta y los valores de Precision@k y Recall@k, además de sus promedios. Las cinco preguntas, respuestas de referencia y documentos relevantes están en `golden_set.json`. Las respuestas de referencia son documentación para inspección humana; estas métricas evalúan recuperación, no calidad de generación.

**Estado:** pendiente de ejecución real contra Pinecone. No se consignan métricas ficticias. Antes de entregar en GitHub se debe ejecutar la ingesta y la evaluación con claves válidas, inspeccionar el resultado y decidir si se adjunta el JSON generado sin datos sensibles.

La relevancia se mide a nivel de documento (`doc_id`), aunque el buscador retorna fragmentos. Un documento repetido entre fragmentos cuenta una sola vez como acierto. Precision@k divide los documentos relevantes distintos recuperados por `k`; Recall@k divide por la cantidad de documentos relevantes del conjunto de referencia.
