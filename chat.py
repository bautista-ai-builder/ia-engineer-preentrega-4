"""Consulta RAG con recuperación híbrida y citas."""

import argparse
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from retrieval import build_retriever

load_dotenv()
PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Responde en español sólo con los fragmentos recuperados. "
     "Si faltan datos, dilo claramente. Cita el nombre de cada fuente usada."),
    ("human", "Pregunta: {question}\n\nFragmentos:\n{context}"),
])


def answer(question: str, retriever=None, model=None) -> dict:
    if not question.strip():
        raise ValueError("Pregunta vacía")
    selected = retriever if retriever is not None else build_retriever()
    docs = selected.invoke(question)
    if not docs:
        return {"answer": "No encuentro información suficiente en los documentos.", "sources": []}
    context = "\n\n".join(f"Fuente: {d.metadata.get('source')}\n{d.page_content}" for d in docs)
    if model is None:
        from langchain_openai import ChatOpenAI

        model = ChatOpenAI(model=os.getenv("CHAT_MODEL", "gpt-4o-mini"), temperature=0)
    reply = model.invoke(PROMPT.invoke({"question": question, "context": context}))
    sources = sorted({d.metadata.get("source", "") for d in docs})
    return {"answer": reply.content, "sources": sources}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="+")
    args = parser.parse_args()
    result = answer(" ".join(args.question))
    print(result["answer"])
    print("Fuentes:", ", ".join(result["sources"]))
