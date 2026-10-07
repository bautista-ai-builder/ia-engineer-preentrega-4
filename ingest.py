"""Ingesta idempotente de documentos en Pinecone."""

import argparse
from pathlib import Path

from documents import load_documents, make_chunks
from pinecone_store import vector_store

ROOT = Path(__file__).resolve().parent


def ingest(data_dir: Path, store=None) -> int:
    chunks, ids = make_chunks(load_documents(data_dir))
    target = store if store is not None else vector_store()
    target.add_documents(chunks, ids=ids)
    return len(chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    print(f"Indexados {ingest(args.data)} fragmentos en Pinecone")
