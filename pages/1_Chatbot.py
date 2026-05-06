from __future__ import annotations

from html import escape
from textwrap import dedent

import streamlit as st

from config import APP_NAME
from src.rag_engine import answer_question, check_system_status


st.set_page_config(
    page_title=f"{APP_NAME} - Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_html(markup: str) -> None:
    """Renderiza HTML sem ser interpretado como bloco de código Markdown."""
    clean_markup = " ".join(dedent(markup).strip().split())
    st.markdown(clean_markup, unsafe_allow_html=True)


st.markdown(
    dedent(
        """
        <style>
            *, *::before, *::after {
                box-sizing: border-box;
            }

            [data-testid="stDeployButton"] {
                display: none;
            }

            #MainMenu {
                visibility: hidden;
            }

            footer {
                visibility: hidden;
            }

            html, body, .stApp, [data-testid="stAppViewContainer"] {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                background: #f7f8fa !important;
            }

            .block-container {
                max-width: 1120px;
                padding-top: 2.8rem;
                padding-bottom: 7rem;
            }

            [data-testid="stSidebar"] {
                background: #ffffff !important;
                border-right: 1px solid #e5e7eb !important;
            }

            [data-testid="stSidebar"] > div:first-child {
                padding: 2rem 1.4rem;
            }

            .hero {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 24px;
                padding: 42px 48px;
                margin-bottom: 24px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 20px 48px rgba(15, 23, 42, 0.06);
            }

            .hero::before {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                width: 360px;
                height: 100%;
                background: radial-gradient(ellipse at 80% 15%, #eef6ff 0%, transparent 70%);
                pointer-events: none;
            }

            .hero-content {
                position: relative;
                z-index: 1;
            }

            .hero-eyebrow {
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: #64748b;
                margin-bottom: 18px;
                display: flex;
                align-items: center;
                gap: 9px;
            }

            .hero-eyebrow::before {
                content: "";
                display: inline-block;
                width: 24px;
                height: 2px;
                background: #64748b;
                border-radius: 2px;
            }

            .hero-row {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 16px;
            }

            .hero-icon {
                width: 54px;
                height: 54px;
                border-radius: 16px;
                background: #111827;
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                box-shadow: 0 8px 20px rgba(17, 24, 39, 0.18);
            }

            .hero-icon svg {
                width: 25px;
                height: 25px;
            }

            .hero-title {
                font-size: 2.3rem;
                line-height: 1.08;
                font-weight: 800;
                color: #111827;
                letter-spacing: -0.03em;
                margin: 0;
            }

            .hero-text {
                color: #64748b;
                font-size: 1.02rem;
                line-height: 1.7;
                max-width: 720px;
                margin: 0;
            }

            .status-panel {
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 20px 24px;
                background: #ffffff;
                margin-bottom: 28px;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
            }

            .status-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                flex-wrap: wrap;
            }

            .status-title {
                font-size: 0.95rem;
                font-weight: 750;
                color: #111827;
                margin-bottom: 4px;
            }

            .status-text {
                color: #64748b;
                font-size: 0.9rem;
                margin: 0;
            }

            .status-badges {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }

            .badge-ok,
            .badge-warning,
            .badge-error {
                border-radius: 999px;
                padding: 7px 13px;
                font-size: 0.78rem;
                font-weight: 700;
                border: 1px solid;
                white-space: nowrap;
                letter-spacing: 0.01em;
            }

            .badge-ok {
                background: #f0fdf4;
                border-color: #bbf7d0;
                color: #15803d;
            }

            .badge-warning {
                background: #fffbeb;
                border-color: #fde68a;
                color: #b45309;
            }

            .badge-error {
                background: #fef2f2;
                border-color: #fecaca;
                color: #dc2626;
            }

            .sidebar-card {
                background: #f8fafc;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 17px 18px;
                margin-bottom: 16px;
            }

            .sidebar-title {
                font-size: 0.82rem;
                font-weight: 800;
                color: #111827;
                margin-bottom: 7px;
                text-transform: uppercase;
                letter-spacing: 0.07em;
            }

            .sidebar-text {
                color: #64748b;
                font-size: 0.86rem;
                line-height: 1.55;
                margin: 0;
            }

            .sources-title {
                font-weight: 700;
                color: #374151;
                font-size: 0.9rem;
                margin-bottom: 8px;
            }

            [data-testid="stChatMessage"] {
                border-radius: 18px;
                padding: 8px 4px;
            }

            [data-testid="stChatMessageContent"] {
                font-size: 0.98rem;
                line-height: 1.7;
                color: #1f2937;
            }

            /* ── Chat Input ───────────────────────────────── */
            [data-testid="stChatInput"] {
                max-width: 1000px;
                margin: 0 auto;
                background: #ffffff !important;
                border: 1px solid #dbe1ea !important;
                border-radius: 24px !important;
                padding: 14px 16px !important;
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.10);
            }

            /* Remove caixas internas criadas pelo Streamlit */
            [data-testid="stChatInput"] > div,
            [data-testid="stChatInput"] form,
            [data-testid="stChatInput"] div[data-baseweb="textarea"] {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
            }

            /* Campo de texto limpo, sem quadrado interior */
            [data-testid="stChatInput"] textarea {
                min-height: 52px !important;
                border: none !important;
                border-radius: 0 !important;
                background: transparent !important;
                color: #111827 !important;
                font-family: inherit !important;
                font-size: 1rem !important;
                line-height: 1.5 !important;
                padding: 14px 16px !important;
                box-shadow: none !important;
                outline: none !important;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: #94a3b8 !important;
                opacity: 1 !important;
            }

            [data-testid="stChatInput"] textarea:focus {
                background: transparent !important;
                box-shadow: none !important;
                outline: none !important;
            }

            /* Botão de envio */
            [data-testid="stChatInputSubmitButton"] {
                background: #111827 !important;
                color: #ffffff !important;
                border-radius: 18px !important;
                width: 54px !important;
                height: 54px !important;
                transition: all 0.15s ease !important;
            }

            [data-testid="stChatInputSubmitButton"]:hover {
                background: #020617 !important;
                transform: translateY(-1px);
            }

            .stButton > button {
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                background: #ffffff;
                color: #334155;
                font-weight: 600;
                font-family: inherit;
                font-size: 0.9rem;
                padding: 0.65rem 1rem;
                transition: all 0.15s ease;
            }

            .stButton > button:hover {
                border-color: #94a3b8;
                background: #f8fafc;
                color: #111827;
            }

            div[data-testid="stPageLink"] a {
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                background: #ffffff;
                padding: 0.65rem 1rem;
                font-weight: 600;
                font-family: inherit;
                font-size: 0.9rem;
                color: #334155;
                text-decoration: none;
                display: inline-block;
                transition: all 0.15s ease;
            }

            div[data-testid="stPageLink"] a:hover {
                background: #f8fafc;
                border-color: #94a3b8;
                color: #111827;
            }

            hr {
                border-color: #e5e7eb !important;
            }

            @media (max-width: 900px) {
                .hero {
                    padding: 30px 26px;
                }

                .hero-title {
                    font-size: 1.8rem;
                }

                .hero-row {
                    align-items: flex-start;
                }
            }
        </style>
        """
    ),
    unsafe_allow_html=True,
)


def icon_chat() -> str:
    return """
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h8M8 14h5" />
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 5.75h14a1.75 1.75 0 0 1 1.75 1.75v8.5A1.75 1.75 0 0 1 19 17.75h-7l-4.5 3v-3H5A1.75 1.75 0 0 1 3.25 16V7.5A1.75 1.75 0 0 1 5 5.75Z" />
    </svg>
    """


def render_sources(sources: list[str]) -> None:
    if not sources:
        return

    with st.expander("Fontes usadas"):
        st.markdown(
            '<div class="sources-title">Documentos consultados</div>',
            unsafe_allow_html=True,
        )
        for src in sources:
            st.markdown(f"- {src}")


def process_question(question: str, status: dict) -> dict:
    if not (status["chromadb_ready"] and status["ollama_ready"]):
        return {
            "answer": "Sistema não preparado. Valida ChromaDB e Ollama antes de continuar.",
            "sources": [],
        }

    with st.spinner("A consultar procedimentos internos e dados locais..."):
        return answer_question(question)


render_html(
    f"""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-eyebrow">Consulta operacional com RAG local</div>
            <div class="hero-row">
                <div class="hero-icon">{icon_chat()}</div>
                <h1 class="hero-title">Chatbot de Armazém e Logística</h1>
            </div>
            <p class="hero-text">
                Pesquisa procedimentos internos, dados de stock e localização de produtos.
                As respostas são geradas com base em documentos locais e informação estruturada.
            </p>
        </div>
    </div>
    """
)


nav_col_1, nav_col_2, nav_col_3 = st.columns([1.2, 1.6, 4])

with nav_col_1:
    st.page_link("Home.py", label="Voltar à Home")

with nav_col_2:
    st.page_link("pages/2_Como_funciona_RAG.py", label="Como funciona o RAG")


status = check_system_status()

chromadb_badge_class = "badge-ok" if status["chromadb_ready"] else "badge-warning"
chromadb_badge_text = "ChromaDB pronto" if status["chromadb_ready"] else "ChromaDB não preparado"

ollama_badge_class = "badge-ok" if status["ollama_ready"] else "badge-error"
ollama_badge_text = "Ollama disponível" if status["ollama_ready"] else "Ollama indisponível"

status_text = status["message"] if status["message"] else "Sistema pronto para consulta."

render_html(
    f"""
    <div class="status-panel">
        <div class="status-row">
            <div>
                <div class="status-title">Estado do sistema</div>
                <p class="status-text">{escape(status_text)}</p>
            </div>
            <div class="status-badges">
                <span class="{chromadb_badge_class}">{chromadb_badge_text}</span>
                <span class="{ollama_badge_class}">{ollama_badge_text}</span>
            </div>
        </div>
    </div>
    """
)


if not status["chromadb_ready"]:
    st.warning("A base vetorial não está pronta. Corre `python scripts/ingest.py` antes de usar o chatbot.")

if not status["ollama_ready"]:
    st.error("Ollama não está disponível. Inicia o serviço e confirma se o modelo está instalado.")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:
    render_html(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Exemplos de perguntas</div>
            <p class="sidebar-text">
                Usa estes exemplos para testar procedimentos, stock e localização.
            </p>
        </div>
        """
    )

    examples = [
        "Como faço picking de uma encomenda?",
        "O que faço se encontrar uma divergência de stock?",
        "Posso expedir se a etiqueta DHL estiver errada?",
        "Onde está o SKU TSHIRT-BRANCA-S?",
    ]

    for index, example in enumerate(examples):
        if st.button(example, key=f"example_{index}", use_container_width=True):
            st.session_state.pending_question = example
            st.rerun()

    st.divider()

    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            render_sources(msg.get("sources", []))


typed_question = st.chat_input("Faz uma pergunta sobre procedimentos, stock ou localização...")

question = typed_question

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "sources": [],
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        answer_data = process_question(question, status)

        answer = answer_data.get("answer", "")
        sources = answer_data.get("sources", [])

        st.markdown(answer)
        render_sources(sources)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )