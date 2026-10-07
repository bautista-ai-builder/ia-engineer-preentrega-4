"""Precision@k y Recall@k sobre documentos esperados."""

import argparse
import json
from pathlib import Path

from retrieval import build_retriever

ROOT = Path(__file__).resolve().parent


def precision_recall(retrieved: list[str], relevant: set[str], k: int) -> tuple[float, float]:
    if k < 1 or not relevant:
        raise ValueError("k debe ser positivo y relevant no puede estar vacío")
    hits = len(set(retrieved[:k]) & relevant)
    return hits / k, hits / len(relevant)


def evaluate(golden_set: list[dict], retriever, k: int = 4) -> dict:
    rows = []
    for item in golden_set:
        docs = retriever.invoke(item["question"])[:k]
        retrieved = [doc.metadata["doc_id"] for doc in docs]
        relevant = set(item["relevant_doc_ids"])
        precision, recall = precision_recall(retrieved, relevant, k)
        rows.append({"question": item["question"],
                     "reference_answer": item.get("reference_answer", ""),
                     "retrieved_doc_ids": retrieved,
                     "relevant_doc_ids": sorted(relevant), "precision_at_k": precision,
                     "recall_at_k": recall})
    if not rows:
        raise ValueError("El conjunto de evaluación está vacío")
    return {"k": k, "questions": rows,
            "mean_precision_at_k": sum(x["precision_at_k"] for x in rows) / len(rows),
            "mean_recall_at_k": sum(x["recall_at_k"] for x in rows) / len(rows)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--golden", type=Path, default=ROOT / "golden_set.json")
    parser.add_argument("--output", type=Path, default=ROOT / "report" / "results.json")
    args = parser.parse_args()
    golden = json.loads(args.golden.read_text(encoding="utf-8"))
    results = evaluate(golden, build_retriever(k=args.k), args.k)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
