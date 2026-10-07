import json

from documents import load_documents, make_chunks
from evaluate import evaluate, precision_recall
from langchain_core.documents import Document
from pinecone_store import ensure_index
from retrieval import build_retriever


def test_loads_metadata_and_stable_chunk_ids(tmp_path):
    (tmp_path / "a.md").write_text("PostgreSQL guarda los pedidos.", encoding="utf-8")
    (tmp_path / "b.json").write_text(json.dumps([{"topic": "Redis"}]), encoding="utf-8")
    docs = load_documents(tmp_path)
    assert {d.metadata["doc_id"] for d in docs} == {"a", "b"}
    chunks, ids = make_chunks(docs)
    assert all(d.metadata["chunk_id"] for d in chunks)
    assert ids == make_chunks(docs)[1]


def test_precision_and_recall_count_unique_documents():
    assert precision_recall(["a", "a", "b"], {"a", "c"}, 3) == (1 / 3, 1 / 2)


def test_evaluate_retrieval_without_api():
    class Retriever:
        def invoke(self, question):
            return [Document(page_content="x", metadata={"doc_id": "a"})]

    result = evaluate([{"question": "q", "relevant_doc_ids": ["a"]}], Retriever(), k=2)
    assert result["mean_precision_at_k"] == .5
    assert result["mean_recall_at_k"] == 1


def test_hybrid_uses_both_retrievers(tmp_path):
    (tmp_path / "a.md").write_text("PostgreSQL mantiene pedidos.", encoding="utf-8")

    class Store:
        def as_retriever(self, search_kwargs):
            assert search_kwargs == {"k": 2}
            from langchain_core.runnables import RunnableLambda
            return RunnableLambda(lambda _: [])

    retriever = build_retriever(data_dir=tmp_path, store=Store(), k=2)
    assert len(retriever.retrievers) == 2
    assert retriever.invoke("PostgreSQL")


def test_pinecone_index_creation_and_dimension_check(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("PINECONE_API_KEY", "test")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "1536")

    class Indexes:
        def names(self):
            return []

    class Client:
        def list_indexes(self):
            return Indexes()

        def create_index(self, **kwargs):
            self.created = kwargs

        def describe_index(self, name):
            return type("Index", (), {"status": {"ready": True}, "dimension": 1536})()

    client = Client()
    assert ensure_index(client=client) == "preentrega-rag"
    assert client.created["dimension"] == 1536
