from __future__ import annotations

import os
import unicodedata
from typing import Any

import chromadb
import ollama

from config import CHROMA_DIR, COLLECTION_NAME, LLM_MODEL, N_RESULTS
from src.embeddings import create_embedding
from src.structured_search import find_stock_answer


NO_INFO_MESSAGE = (
    "Não tenho informação suficiente nos procedimentos internos para responder com segurança."
)


PROCEDURE_ROUTES: list[tuple[list[str], list[str]]] = [
    (
        [
            "dhl",
            "etiqueta",
            "expedir",
            "expedicao",
            "transportadora",
            "goods out",
            "morada",
            "envio",
            "enviar",
            "reemitir",
        ],
        ["expedicao.txt"],
    ),
    (
        [
            "devolucao",
            "devolver",
            "devolvida",
            "devolvido",
            "voltar a colocar",
            "regressar ao stock",
            "stock imediatamente",
            "artigo devolvido",
        ],
        ["devolucoes.txt"],
    ),
    (
        [
            "produto nao esta",
            "nao esta na localizacao",
            "localizacao indicada",
            "localizacao errada",
            "divergencia",
            "stock fisico",
            "recontar",
            "nao encontro",
            "produto em falta",
            "localizacao alternativa",
        ],
        ["picking.txt", "inventario.txt"],
    ),
    (
        [
            "picking",
            "recolha",
            "preparar encomenda",
            "sku semelhante",
            "quantidade errada",
        ],
        ["picking.txt"],
    ),
    (
        [
            "inventario",
            "contagem",
            "diferenca de stock",
            "correcao de stock",
            "corrigir stock",
            "ajuste de stock",
        ],
        ["inventario.txt"],
    ),
    (
        [
            "seguranca",
            "acidente",
            "emergencia",
            "carga",
            "derrame",
            "obstaculo",
            "saida de emergencia",
            "caixas no chao",
        ],
        ["seguranca.txt"],
    ),
    (
        [
            "armazenar",
            "armazenamento",
            "arrumar",
            "guardar",
            "rotacao",
            "corredor",
            "localizacao de armazenamento",
            "produtos danificados",
        ],
        ["armazenamento.txt"],
    ),
]


def normalise_text(text: str) -> str:
    """
    Normaliza texto para facilitar comparação:
    - remove acentos
    - converte para minúsculas
    - remove espaços excessivos
    """
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return " ".join(text.split())


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(name=COLLECTION_NAME)


def check_system_status() -> dict[str, Any]:
    status = {"chromadb_ready": False, "ollama_ready": False, "message": ""}

    try:
        _ = get_collection()
        status["chromadb_ready"] = True
    except Exception:
        status["message"] += (
            "Base vetorial não encontrada. Corre primeiro: python scripts/ingest.py. "
        )

    try:
        ollama.list()
        status["ollama_ready"] = True
    except Exception:
        status["message"] += "Ollama não disponível. Verifica se o serviço está ativo."

    return status


def get_source_filename(meta: dict[str, Any]) -> str:
    source = str(meta.get("source", "fonte_desconhecida"))
    return os.path.basename(source)


def format_source(meta: dict[str, Any]) -> str:
    source = meta.get("source", "fonte_desconhecida")
    data_type = meta.get("data_type", "não identificado")
    sku = meta.get("sku")

    label = f"{source} ({data_type})"

    if sku:
        label += f" - SKU: {sku}"

    return label


def get_preferred_sources(question: str) -> list[str]:
    """
    Escolhe documentos prioritários de acordo com palavras-chave da pergunta.
    Isto melhora o RAG em perguntas operacionais específicas.
    """
    q = normalise_text(question)

    preferred: list[str] = []

    for keywords, sources in PROCEDURE_ROUTES:
        for keyword in keywords:
            if normalise_text(keyword) in q:
                preferred.extend(sources)
                break

    return list(dict.fromkeys(preferred))


def is_unstructured(meta: dict[str, Any]) -> bool:
    data_type = normalise_text(str(meta.get("data_type", "")))
    return data_type == "nao estruturado"


def query_semantic_context(
    collection,
    question: str,
    n_results: int,
    only_unstructured: bool = True,
) -> tuple[list[str], list[dict[str, Any]]]:
    """
    Pesquisa semântica na ChromaDB.
    Para perguntas de procedimento, filtra documentos não estruturados.
    """
    question_embedding = create_embedding(question)

    query_kwargs: dict[str, Any] = {
        "query_embeddings": [question_embedding],
        "n_results": n_results,
        "include": ["documents", "metadatas"],
    }

    if only_unstructured:
        query_kwargs["where"] = {"data_type": "não estruturado"}

    try:
        results = collection.query(**query_kwargs)
    except Exception:
        # Fallback caso a versão/configuração da ChromaDB não aceite o filtro where
        query_kwargs.pop("where", None)
        results = collection.query(**query_kwargs)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if only_unstructured:
        filtered_docs: list[str] = []
        filtered_metas: list[dict[str, Any]] = []

        for doc, meta in zip(documents, metadatas):
            if is_unstructured(meta):
                filtered_docs.append(doc)
                filtered_metas.append(meta)

        return filtered_docs, filtered_metas

    return documents, metadatas


def get_all_unstructured_documents(collection) -> tuple[list[str], list[dict[str, Any]]]:
    """
    Obtém todos os documentos não estruturados.
    Útil para forçar prioridade em ficheiros como expedicao.txt ou devolucoes.txt.
    """
    try:
        results = collection.get(
            where={"data_type": "não estruturado"},
            include=["documents", "metadatas"],
        )
    except Exception:
        results = collection.get(include=["documents", "metadatas"])

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    filtered_docs: list[str] = []
    filtered_metas: list[dict[str, Any]] = []

    for doc, meta in zip(documents, metadatas):
        if is_unstructured(meta):
            filtered_docs.append(doc)
            filtered_metas.append(meta)

    return filtered_docs, filtered_metas


def retrieve_context(question: str) -> tuple[str, list[str]]:
    collection = get_collection()
    preferred_sources = get_preferred_sources(question)

    selected_docs: list[str] = []
    selected_metas: list[dict[str, Any]] = []

    # 1. Se a pergunta encaixa num procedimento específico,
    #    carregar primeiro os ficheiros certos.
    if preferred_sources:
        all_docs, all_metas = get_all_unstructured_documents(collection)

        for preferred_source in preferred_sources:
            for doc, meta in zip(all_docs, all_metas):
                if get_source_filename(meta) == preferred_source:
                    selected_docs.append(doc)
                    selected_metas.append(meta)

    # 2. Complementar com pesquisa semântica em documentos não estruturados.
    semantic_docs, semantic_metas = query_semantic_context(
        collection=collection,
        question=question,
        n_results=max(N_RESULTS, 8),
        only_unstructured=True,
    )

    selected_docs.extend(semantic_docs)
    selected_metas.extend(semantic_metas)

    # 3. Remover documentos e fontes duplicadas.
    final_docs: list[str] = []
    final_sources: list[str] = []
    seen_docs: set[str] = set()
    seen_sources: set[str] = set()

    for doc, meta in zip(selected_docs, selected_metas):
        clean_doc = doc.strip()

        if not clean_doc:
            continue

        if clean_doc not in seen_docs:
            final_docs.append(clean_doc)
            seen_docs.add(clean_doc)

        source_label = format_source(meta)
        if source_label not in seen_sources:
            final_sources.append(source_label)
            seen_sources.add(source_label)

    # 4. Limitar contexto para evitar excesso de ruído.
    final_docs = final_docs[: max(N_RESULTS, 6)]

    context = "\n\n---\n\n".join(final_docs)

    return context, final_sources


def build_prompt(question: str, context: str) -> str:
    return f"""
És um assistente local para operações de armazém e logística.

Regras obrigatórias:
- Responde sempre em português europeu.
- Usa apenas a informação disponível no CONTEXTO.
- Não inventes procedimentos, regras, nomes, salários ou dados que não estejam no CONTEXTO.
- Se o CONTEXTO tiver uma regra diretamente aplicável à pergunta, deves responder com essa regra.
- Só podes responder "{NO_INFO_MESSAGE}" se o CONTEXTO não tiver nenhuma informação relevante para a pergunta.
- Se existir risco operacional, produto danificado, divergência de stock, etiqueta errada, morada errada, dúvida na expedição ou diferença entre sistema e stock físico, recomenda validação com o responsável do armazém.
- Responde de forma prática, clara e por passos quando fizer sentido.
- Não digas que pesquisaste na ChromaDB.
- Não menciones informação técnica sobre embeddings ou RAG na resposta ao operador.

CONTEXTO:
{context}

PERGUNTA:
{question}

RESPOSTA:
""".strip()


def ask_llm(prompt: str) -> str:
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1},
    )

    return response["message"]["content"].strip()


def answer_question(question: str) -> dict[str, Any]:
    """
    Fluxo principal:
    1. Primeiro tenta responder a perguntas estruturadas sobre stock/SKU.
    2. Se não for pergunta de stock, usa RAG com documentos internos não estruturados.
    """

    stock_answer = find_stock_answer(question)

    if stock_answer:
        return {
            "answer": stock_answer,
            "sources": ["data/stock.csv (estruturado)"],
        }

    context, sources = retrieve_context(question)

    if not context.strip():
        return {
            "answer": NO_INFO_MESSAGE,
            "sources": [],
        }

    prompt = build_prompt(question, context)
    llm_answer = ask_llm(prompt)

    return {
        "answer": llm_answer,
        "sources": sources,
    }