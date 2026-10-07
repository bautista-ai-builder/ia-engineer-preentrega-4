"""Carga de PDF, Markdown, texto y JSON con metadatos trazables."""

import hashlib
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext not in {".pdf", ".md", ".txt", ".json"}:
            continue
        source = str(path.relative_to(data_dir))
        category = path.parent.name if path.parent != data_dir else "general"
        base = {"source": source, "doc_id": path.stem, "category": category}
        if ext == ".pdf":
            from pypdf import PdfReader

            for page_number, page in enumerate(PdfReader(str(path)).pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    documents.append(Document(
                        page_content=text, metadata={**base, "page": page_number}
                    ))
        elif ext == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            records = data if isinstance(data, list) else [data]
            for position, record in enumerate(records, start=1):
                text = record if isinstance(record, str) else json.dumps(record, ensure_ascii=False)
                if text.strip():
                    documents.append(Document(
                        page_content=text, metadata={**base, "page": position}
                    ))
        else:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                documents.append(Document(page_content=text, metadata={**base, "page": 1}))
    if not documents:
        raise ValueError(f"No hay documentos válidos en {data_dir}")
    return documents


def make_chunks(documents: list[Document]) -> tuple[list[Document], list[str]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    ids = []
    for position, chunk in enumerate(chunks):
        raw = f"{chunk.metadata['source']}:{chunk.metadata['page']}:{position}:{chunk.page_content}"
        chunk_id = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        chunk.metadata["chunk_id"] = chunk_id
        ids.append(chunk_id)
    return chunks, ids
