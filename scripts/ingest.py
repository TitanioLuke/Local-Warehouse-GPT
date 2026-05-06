from __future__ import annotations

import os
import uuid
from pathlib import Path

import chromadb
import pandas as pd

from config import CHROMA_DIR, COLLECTION_NAME, DOCUMENTS_DIR, STOCK_FILE
from src.embeddings import create_embedding

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = start + chunk_size
        chunks.append(cleaned[start:end])
        if end >= len(cleaned):
            break
        start = end - overlap
    return chunks


def load_unstructured_documents() -> tuple[list[str], list[dict], list[str]]:
    docs: list[str] = []
    metas: list[dict] = []
    ids: list[str] = []

    docs_path = Path(DOCUMENTS_DIR)
    for file_path in sorted(docs_path.glob("*.txt")):
        content = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            metas.append(
                {
                    "source": file_path.name,
                    "data_type": "não estruturado",
                }
            )
            ids.append(f"{file_path.stem}-{i}-{uuid.uuid4().hex[:8]}")

    return docs, metas, ids


def load_structured_rows() -> tuple[list[str], list[dict], list[str]]:
    docs: list[str] = []
    metas: list[dict] = []
    ids: list[str] = []

    df = pd.read_csv(STOCK_FILE)
    for _, row in df.iterrows():
        row_text = (
            f"SKU {row['SKU']}. Produto: {row['Produto']}. Categoria: {row['Categoria']}. "
            f"Localização: {row['Localizacao']}. Stock atual: {row['Stock']}. "
            f"Stock mínimo: {row['Stock_Minimo']}."
        )
        docs.append(row_text)
        metas.append(
            {
                "source": "stock.csv",
                "data_type": "estruturado",
                "sku": str(row["SKU"]),
            }
        )
        ids.append(f"stock-{row['SKU']}-{uuid.uuid4().hex[:8]}")

    return docs, metas, ids


def main():
    print("A iniciar ingestão de dados...")
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    docs_u, metas_u, ids_u = load_unstructured_documents()
    docs_s, metas_s, ids_s = load_structured_rows()

    all_docs = docs_u + docs_s
    all_metas = metas_u + metas_s
    all_ids = ids_u + ids_s

    embeddings = [create_embedding(doc) for doc in all_docs]

    collection.add(
        ids=all_ids,
        documents=all_docs,
        embeddings=embeddings,
        metadatas=all_metas,
    )

    print(f"Ingestão concluída. Total de blocos carregados: {len(all_docs)}")


if __name__ == "__main__":
    main()
