from textwrap import dedent

import streamlit as st

from config import APP_NAME


st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    dedent(
        """
        <style>
            [data-testid="stDeployButton"] {
                display: none;
            }

            #MainMenu {
                visibility: hidden;
            }

            footer {
                visibility: hidden;
            }

            .stApp {
                background: #ffffff;
            }

            .block-container {
                max-width: 1180px;
                padding-top: 4rem;
                padding-bottom: 4rem;
            }

            [data-testid="stSidebar"] {
                background: #f3f6fa;
                border-right: 1px solid #e5e7eb;
            }

            .hero {
                background: linear-gradient(135deg, #f8fafc 0%, #eef3f8 100%);
                border: 1px solid #e5e7eb;
                border-radius: 28px;
                padding: 64px;
                box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
                margin-bottom: 56px;
            }

            .eyebrow {
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: #475569;
                margin-bottom: 16px;
            }

            .hero-title {
                font-size: 3.4rem;
                line-height: 1.05;
                font-weight: 850;
                color: #0f172a;
                margin: 0 0 24px 0;
            }

            .hero-text {
                font-size: 1.18rem;
                line-height: 1.75;
                color: #475569;
                max-width: 830px;
                margin-bottom: 36px;
            }

            .button-row {
                display: flex;
                gap: 16px;
                flex-wrap: wrap;
            }

            .primary-button,
            .secondary-button {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                padding: 14px 22px;
                border-radius: 14px;
                text-decoration: none !important;
                font-weight: 750;
                transition: all 0.2s ease;
            }

            .primary-button {
                background: #0f172a;
                color: #ffffff !important;
                border: 1px solid #0f172a;
            }

            .primary-button:hover {
                background: #1e293b;
                border-color: #1e293b;
            }

            .secondary-button {
                background: #ffffff;
                color: #0f172a !important;
                border: 1px solid #cbd5e1;
            }

            .secondary-button:hover {
                background: #f8fafc;
                border-color: #94a3b8;
            }

            .section-title {
                font-size: 1.55rem;
                font-weight: 850;
                color: #0f172a;
                margin-bottom: 24px;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 22px;
                margin-bottom: 52px;
            }

            .card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 24px;
                padding: 30px;
                min-height: 245px;
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.05);
            }

            .icon-box {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                background: #f1f5f9;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 26px;
                color: #0f172a;
            }

            .card-title {
                font-size: 1.05rem;
                font-weight: 850;
                color: #0f172a;
                margin-bottom: 12px;
            }

            .card-text {
                color: #64748b;
                line-height: 1.65;
                font-size: 0.98rem;
            }

            .bottom-panel {
                background: #0f172a;
                color: #ffffff;
                border-radius: 26px;
                padding: 36px 42px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 24px;
                margin-top: 20px;
            }

            .bottom-panel-title {
                margin: 0 0 10px 0;
                font-size: 1.35rem;
                font-weight: 850;
            }

            .bottom-panel-text {
                margin: 0;
                color: #cbd5e1;
                line-height: 1.6;
                max-width: 760px;
            }

            .tech-badge {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 999px;
                padding: 13px 20px;
                font-weight: 800;
                white-space: nowrap;
                color: #ffffff;
            }

            svg {
                width: 22px;
                height: 22px;
            }

            @media (max-width: 900px) {
                .hero {
                    padding: 44px 30px;
                }

                .hero-title {
                    font-size: 2.4rem;
                }

                .cards {
                    grid-template-columns: 1fr;
                }

                .bottom-panel {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }
        </style>
        """
    ),
    unsafe_allow_html=True,
)


st.markdown(
    dedent(
        """
        <div class="hero">
            <div class="eyebrow">Sistema local de apoio operacional</div>
            <div class="hero-title">Local Warehouse GPT</div>
            <div class="hero-text">
                Assistente inteligente para consulta de procedimentos internos, localização de produtos
                e dados de stock. O sistema utiliza RAG local para responder com base em documentos
                internos e informação estruturada do armazém.
            </div>
            <div class="button-row">
                <a class="primary-button" href="/Chatbot">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h8M8 14h5" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 5.75h14a1.75 1.75 0 0 1 1.75 1.75v8.5A1.75 1.75 0 0 1 19 17.75h-7l-4.5 3v-3H5A1.75 1.75 0 0 1 3.25 16V7.5A1.75 1.75 0 0 1 5 5.75Z" />
                    </svg>
                    Abrir Chatbot
                </a>
                <a class="secondary-button" href="/Como_funciona_RAG">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75v10.5" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 9.25c1.7-.7 3.45-.7 5.25 0 1.8-.7 3.55-.7 5.25 0v8.5c-1.7-.7-3.45-.7-5.25 0-1.8-.7-3.55-.7-5.25 0v-8.5Z" />
                    </svg>
                    Ver explicação RAG
                </a>
            </div>
        </div>
        """
    ).strip(),
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="section-title">Capacidades principais</div>',
    unsafe_allow_html=True,
)


st.markdown(
    dedent(
        """
        <div class="cards">
            <div class="card">
                <div class="icon-box">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3.75 4.75 7.5 12 11.25l7.25-3.75L12 3.75Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.75 7.5v9L12 20.25l7.25-3.75v-9" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 11.25v9" />
                    </svg>
                </div>
                <div class="card-title">Consulta de procedimentos</div>
                <div class="card-text">
                    Pesquisa em documentos internos sobre picking, expedição, devoluções,
                    inventário, segurança e armazenamento.
                </div>
            </div>
            <div class="card">
                <div class="icon-box">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 6.75h14M5 12h14M5 17.25h14" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 4.75v14.5M16 4.75v14.5" />
                    </svg>
                </div>
                <div class="card-title">Dados estruturados de stock</div>
                <div class="card-text">
                    Permite consultar SKU, descrição, categoria, localização, stock atual
                    e stock mínimo com base no ficheiro CSV.
                </div>
            </div>
            <div class="card">
                <div class="icon-box">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.75 19.25 8v5.5c0 3.5-2.4 5.8-7.25 6.75-4.85-.95-7.25-3.25-7.25-6.75V8L12 4.75Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="m9.25 12.25 1.9 1.9 3.85-4.1" />
                    </svg>
                </div>
                <div class="card-title">Resposta controlada</div>
                <div class="card-text">
                    O modelo responde apenas com base no contexto recuperado e identifica
                    as fontes usadas para maior rastreabilidade.
                </div>
            </div>
        </div>
        """
    ).strip(),
    unsafe_allow_html=True,
)


st.markdown(
    dedent(
        """
        <div class="bottom-panel">
            <div>
                <div class="bottom-panel-title">Preparado para apoio operacional controlado</div>
                <div class="bottom-panel-text">
                    O sistema foi desenhado para reduzir dúvidas operacionais, apoiar novos colaboradores
                    e evitar respostas sem base documental.
                </div>
            </div>
            <div class="tech-badge">ChromaDB + Ollama + Streamlit</div>
        </div>
        """
    ).strip(),
    unsafe_allow_html=True,
)