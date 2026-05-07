"""
Knowledge base ingestion script.
Run once before first use:  python rag/ingest.py
"""

import sys
from pathlib import Path

# Allow running directly: python rag/ingest.py
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from rag.vectorstore import get_vectorstore

KB_DIR = Path(__file__).parent / "knowledge_base"


def _load_markdown(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)
    return [
        Document(page_content=chunk, metadata={"source": path.name, "type": "owasp"})
        for chunk in chunks
    ]


def _load_cwe_json(path: Path) -> list[Document]:
    entries: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    docs = []
    for entry in entries:
        content = (
            f"CWE ID: {entry['cwe_id']}\n"
            f"Name: {entry['name']}\n"
            f"Severity: {entry['severity']}\n"
            f"Description: {entry['description']}\n"
            f"Detection patterns: {', '.join(entry['detection_patterns'])}\n"
            f"Fix: {entry['fix']}\n"
            f"Languages: {', '.join(entry['languages'])}"
        )
        docs.append(Document(
            page_content=content,
            metadata={"cwe_id": entry["cwe_id"], "source": path.name, "type": "cwe"},
        ))
    return docs


def ingest() -> None:
    print("Loading knowledge base files...")
    documents: list[Document] = []

    for md_file in KB_DIR.glob("*.md"):
        docs = _load_markdown(md_file)
        documents.extend(docs)
        print(f"  {md_file.name}: {len(docs)} chunks")

    for json_file in KB_DIR.glob("*.json"):
        docs = _load_cwe_json(json_file)
        documents.extend(docs)
        print(f"  {json_file.name}: {len(docs)} documents")

    print(f"\nIngesting {len(documents)} total documents into ChromaDB...")
    vs = get_vectorstore()
    vs.add_documents(documents)
    print("Knowledge base ready.")


if __name__ == "__main__":
    ingest()
