"""Parámetros del índice Pinecone y de los modelos."""

import os

from dotenv import load_dotenv

load_dotenv()


def require_cloud_keys() -> None:
    missing = [name for name in ("OPENAI_API_KEY", "PINECONE_API_KEY") if not os.getenv(name)]
    if missing:
        raise RuntimeError("Faltan variables: " + ", ".join(missing))


def index_name() -> str:
    return os.getenv("PINECONE_INDEX", "preentrega-rag")


def namespace() -> str:
    return os.getenv("PINECONE_NAMESPACE", "curso-ia")


def embeddings():
    from langchain_openai import OpenAIEmbeddings

    require_cloud_keys()
    return OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
                            dimensions=int(os.getenv("EMBEDDING_DIMENSION", "1536")))
