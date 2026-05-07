from langchain_chroma import Chroma

from config.settings import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR
from rag.embeddings import get_embeddings

_vectorstore_instance: Chroma | None = None


def get_vectorstore() -> Chroma:
    """Return a cached ChromaDB vectorstore backed by local HuggingFace embeddings."""
    global _vectorstore_instance
    if _vectorstore_instance is None:
        _vectorstore_instance = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=get_embeddings(),
            persist_directory=CHROMA_PERSIST_DIR,
        )
    return _vectorstore_instance


def get_retriever(k: int = 4):
    """Return a retriever that fetches the top-k most relevant KB chunks."""
    return get_vectorstore().as_retriever(search_kwargs={"k": k})
