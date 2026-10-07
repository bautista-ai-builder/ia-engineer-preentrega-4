"""Ensamble de búsqueda vectorial Pinecone y búsqueda léxica BM25."""

from pathlib import Path

from documents import load_documents, make_chunks
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from pinecone_store import vector_store

ROOT = Path(__file__).resolve().parent


def build_retriever(*, data_dir: Path = ROOT / "data", store=None, k: int = 4):
    if k < 1:
        raise ValueError("k debe ser >= 1")
    chunks, _ = make_chunks(load_documents(data_dir))
    lexical = BM25Retriever.from_documents(chunks)
    lexical.k = k
    dense_store = store if store is not None else vector_store()
    dense = dense_store.as_retriever(search_kwargs={"k": k})
    return EnsembleRetriever(retrievers=[dense, lexical], weights=[0.6, 0.4], id_key="chunk_id")
