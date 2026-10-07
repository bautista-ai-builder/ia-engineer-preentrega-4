"""Inicialización de índice Serverless y vector store de LangChain."""

import os
import time

from config import embeddings, index_name, namespace, require_cloud_keys


def ensure_index(*, client=None, timeout_seconds: int = 120) -> str:
    from pinecone import Pinecone, ServerlessSpec

    require_cloud_keys()
    pc = client if client is not None else Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    name = index_name()
    dimension = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
    if dimension < 1:
        raise ValueError("EMBEDDING_DIMENSION debe ser positiva")
    if name not in pc.list_indexes().names():
        pc.create_index(name=name, dimension=dimension, metric="cosine",
                        spec=ServerlessSpec(cloud=os.getenv("PINECONE_CLOUD", "aws"),
                                            region=os.getenv("PINECONE_REGION", "us-east-1")))
    deadline = time.monotonic() + timeout_seconds
    while not pc.describe_index(name).status["ready"]:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"El índice {name} no quedó listo a tiempo")
        time.sleep(2)
    actual_dimension = pc.describe_index(name).dimension
    if actual_dimension != dimension:
        raise ValueError(f"Dimensión de índice {actual_dimension} != embeddings {dimension}")
    return name


def vector_store():
    from langchain_pinecone import PineconeVectorStore

    name = ensure_index()
    return PineconeVectorStore(index_name=name, embedding=embeddings(), namespace=namespace())
