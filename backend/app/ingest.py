import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embeddings import get_vector_store

SUPPORTED = {".pdf": PyPDFLoader, ".txt": TextLoader, ".md": TextLoader}

def ingest_directory(path: str) -> dict:
    """
    Recursively load all supported files from a directory,
    split them, embed, and upsert into the vector store.
    """
    docs = []
    root = Path(path)

    for ext, loader_cls in SUPPORTED.items():
        for file in root.rglob(f"*{ext}"):
            try:
                loader = loader_cls(str(file))
                loaded = loader.load()
                for doc in loaded:
                    doc.metadata["source"] = file.name
                docs.extend(loaded)
            except Exception as e:
                print(f"Failed to load {file}: {e}")

    if not docs:
        return {"ingested": 0, "chunks": 0}

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    store = get_vector_store()
    store.add_documents(chunks)

    return {"ingested": len(docs), "chunks": len(chunks)}