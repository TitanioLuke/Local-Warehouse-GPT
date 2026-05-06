from __future__ import annotations

import streamlit as st

from config import APP_NAME


st.set_page_config(
    page_title=f"{APP_NAME} - Como funciona o RAG",
    layout="centered",
    initial_sidebar_state="expanded",
)


def render_html(markup: str) -> None:
    """Renderiza HTML sem o Streamlit o apresentar como bloco de código."""
    clean_markup = " ".join(markup.split())
    st.markdown(clean_markup, unsafe_allow_html=True)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=DM+Mono:wght@400;500&display=swap');

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
            font-family: 'DM Sans', sans-serif;
            background: #f7f8fa !important;
        }

        .block-container {
            max-width: 1040px;
            padding-top: 2.8rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #e8eaed !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 2rem 1.4rem;
        }

        .hero {
            background: #ffffff;
            border: 1px solid #e8eaed;
            border-radius: 22px;
            padding: 42px 48px;
            margin-bottom: 26px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 18px 50px rgba(17, 24, 39, 0.04);
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 340px;
            height: 100%;
            background: radial-gradient(ellipse at 85% 20%, #eef6ff 0%, transparent 70%);
            pointer-events: none;
        }

        .eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            color: #64748b;
            margin-bottom: 18px;
        }

        .hero-title {
            font-size: 2.15rem;
            line-height: 1.12;
            font-weight: 750;
            color: #111827;
            letter-spacing: -0.03em;
            margin: 0 0 16px 0;
            max-width: 760px;
        }

        .hero-text {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.7;
            max-width: 760px;
            margin: 0;
        }

        .nav-row {
            display: flex;
            gap: 12px;
            margin-bottom: 26px;
            flex-wrap: wrap;
        }

        div[data-testid="stPageLink"] a {
            border-radius: 11px;
            border: 1px solid #e8eaed;
            background: #ffffff;
            padding: 0.65rem 1rem;
            font-weight: 600;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.9rem;
            color: #374151;
            text-decoration: none;
            display: inline-block;
            transition: all 0.15s ease;
        }

        div[data-testid="stPageLink"] a:hover {
            background: #f9fafb;
            border-color: #9ca3af;
            color: #111827;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 750;
            color: #111827;
            margin: 34px 0 14px 0;
            letter-spacing: -0.01em;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }

        .card {
            background: #ffffff;
            border: 1px solid #e8eaed;
            border-radius: 18px;
            padding: 24px;
            min-height: 170px;
            box-shadow: 0 12px 34px rgba(17, 24, 39, 0.035);
        }

        .card-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #f1f5f9;
            color: #111827;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 18px;
        }

        .card-icon svg {
            width: 21px;
            height: 21px;
        }

        .card-title {
            font-size: 1rem;
            font-weight: 750;
            color: #111827;
            margin-bottom: 10px;
        }

        .card-text {
            font-size: 0.94rem;
            line-height: 1.65;
            color: #64748b;
            margin: 0;
        }

        .flow {
            background: #ffffff;
            border: 1px solid #e8eaed;
            border-radius: 20px;
            padding: 26px;
            margin-bottom: 20px;
            box-shadow: 0 12px 34px rgba(17, 24, 39, 0.035);
        }

        .flow-step {
            display: grid;
            grid-template-columns: 44px 1fr;
            gap: 14px;
            padding: 14px 0;
            border-bottom: 1px solid #eef0f3;
        }

        .flow-step:last-child {
            border-bottom: none;
        }

        .step-number {
            width: 34px;
            height: 34px;
            border-radius: 10px;
            background: #111827;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'DM Mono', monospace;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .step-title {
            font-size: 0.98rem;
            font-weight: 750;
            color: #111827;
            margin-bottom: 4px;
        }

        .step-text {
            font-size: 0.92rem;
            color: #64748b;
            line-height: 1.6;
            margin: 0;
        }

        .code-box {
            background: #0f172a;
            color: #e5e7eb;
            border-radius: 18px;
            padding: 22px 24px;
            font-family: 'DM Mono', monospace;
            font-size: 0.86rem;
            line-height: 1.75;
            margin: 18px 0 26px 0;
            overflow-x: auto;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }

        .pill {
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #334155;
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 0.82rem;
            font-weight: 600;
            font-family: 'DM Mono', monospace;
        }

        .warning-card {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 18px;
            padding: 22px 24px;
            color: #7c2d12;
            margin-top: 20px;
        }

        .warning-title {
            font-size: 0.98rem;
            font-weight: 750;
            margin-bottom: 8px;
            color: #7c2d12;
        }

        .warning-text {
            font-size: 0.92rem;
            line-height: 1.65;
            margin: 0;
        }

        @media (max-width: 800px) {
            .hero {
                padding: 30px 26px;
            }

            .hero-title {
                font-size: 1.65rem;
            }

            .card-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def icon_database() -> str:
    return """
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <ellipse cx="12" cy="5" rx="7" ry="3"></ellipse>
        <path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"></path>
        <path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"></path>
    </svg>
    """


def icon_search() -> str:
    return """
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="7"></circle>
        <path d="M20 20l-3.5-3.5"></path>
    </svg>
    """


def icon_file() -> str:
    return """
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"></path>
        <path d="M14 3v5h5"></path>
        <path d="M9 13h6"></path>
        <path d="M9 17h4"></path>
    </svg>
    """


def icon_cpu() -> str:
    return """
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <rect x="7" y="7" width="10" height="10" rx="2"></rect>
        <path d="M9 1v3"></path>
        <path d="M15 1v3"></path>
        <path d="M9 20v3"></path>
        <path d="M15 20v3"></path>
        <path d="M20 9h3"></path>
        <path d="M20 15h3"></path>
        <path d="M1 9h3"></path>
        <path d="M1 15h3"></path>
    </svg>
    """


render_html(
    """
    <div class="hero">
        <div class="eyebrow">Funcionamento interno do chatbot</div>
        <h1 class="hero-title">Como o RAG é usado neste chatbot de armazém</h1>
        <p class="hero-text">
            Esta página descreve o percurso real da pergunta dentro da aplicação:
            desde a entrada do utilizador, passando pela pesquisa em ChromaDB e no ficheiro de stock,
            até à resposta final gerada localmente com indicação das fontes usadas.
        </p>
    </div>
    """
)

st.page_link("pages/1_Chatbot.py", label="Voltar ao Chatbot")

render_html('<div class="section-title">Componentes usados no projeto</div>')

render_html(
    f"""
    <div class="card-grid">
        <div class="card">
            <div class="card-icon">{icon_file()}</div>
            <div class="card-title">Ficheiros internos</div>
            <p class="card-text">
                Os procedimentos do armazém estão guardados em ficheiros de texto,
                como picking, expedição, devoluções, inventário, segurança e armazenamento.
            </p>
            <div class="pill-row">
                <span class="pill">documents/*.txt</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">{icon_database()}</div>
            <div class="card-title">Base vetorial ChromaDB</div>
            <p class="card-text">
                Depois do ingest, os textos são transformados em embeddings e guardados na ChromaDB.
                O chatbot pesquisa nesta base para encontrar os procedimentos mais relevantes.
            </p>
            <div class="pill-row">
                <span class="pill">chroma_db</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">{icon_search()}</div>
            <div class="card-title">Pesquisa estruturada de stock</div>
            <p class="card-text">
                Para perguntas sobre SKU, localização ou stock, o sistema tenta primeiro responder
                diretamente com base no ficheiro CSV de stock.
            </p>
            <div class="pill-row">
                <span class="pill">data/stock.csv</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">{icon_cpu()}</div>
            <div class="card-title">LLM local via Ollama</div>
            <p class="card-text">
                Quando a pergunta exige interpretação, o contexto recuperado é enviado ao modelo local.
                O modelo só deve responder com base nessa informação.
            </p>
            <div class="pill-row">
                <span class="pill">Ollama</span>
                <span class="pill">LLM local</span>
            </div>
        </div>
    </div>
    """
)

render_html('<div class="section-title">Fluxo real da pergunta no chatbot</div>')

render_html(
    """
    <div class="flow">
        <div class="flow-step">
            <div class="step-number">01</div>
            <div>
                <div class="step-title">O utilizador escreve uma pergunta</div>
                <p class="step-text">
                    A pergunta é introduzida no campo de chat. Pode ser sobre procedimentos,
                    stock, localização de produtos, devoluções, expedição ou inventário.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">02</div>
            <div>
                <div class="step-title">O sistema verifica primeiro se é uma pergunta de stock</div>
                <p class="step-text">
                    A função find_stock_answer(question) tenta identificar se a pergunta está relacionada
                    com um SKU, stock atual, localização ou stock mínimo. Se encontrar resposta no CSV,
                    responde diretamente sem recorrer ao LLM.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">03</div>
            <div>
                <div class="step-title">Se não for stock direto, é criado o embedding da pergunta</div>
                <p class="step-text">
                    A pergunta é convertida num vetor numérico através da função create_embedding(question).
                    Esse vetor representa semanticamente o conteúdo da pergunta.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">04</div>
            <div>
                <div class="step-title">A pergunta é pesquisada na ChromaDB</div>
                <p class="step-text">
                    O sistema compara o embedding da pergunta com os embeddings guardados na ChromaDB
                    e recupera os documentos internos mais próximos do tema perguntado.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">05</div>
            <div>
                <div class="step-title">O contexto é montado com fontes</div>
                <p class="step-text">
                    Os excertos encontrados são reunidos num contexto. Ao mesmo tempo, são guardadas
                    as fontes usadas, como picking.txt, expedicao.txt, devolucoes.txt ou stock.csv.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">06</div>
            <div>
                <div class="step-title">O prompt é enviado ao modelo local</div>
                <p class="step-text">
                    A função build_prompt junta a pergunta, o contexto e regras obrigatórias.
                    O modelo é instruído a responder apenas com base nos procedimentos internos.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">07</div>
            <div>
                <div class="step-title">A resposta é apresentada com fontes</div>
                <p class="step-text">
                    O chatbot mostra a resposta final ao utilizador e apresenta uma secção com as fontes
                    usadas para justificar a resposta.
                </p>
            </div>
        </div>
    </div>
    """
)

render_html('<div class="section-title">Ordem de decisão usada no código</div>')

render_html(
    """
    <div class="code-box">
        1. Receber pergunta do utilizador<br>
        2. Tentar responder com pesquisa estruturada no stock.csv<br>
        3. Se houver resposta de stock, devolver imediatamente<br>
        4. Se não houver, pesquisar contexto na ChromaDB<br>
        5. Recuperar documentos relevantes<br>
        6. Construir prompt com contexto e regras<br>
        7. Enviar para o modelo local via Ollama<br>
        8. Mostrar resposta e fontes usadas
    </div>
    """
)

render_html('<div class="section-title">O que acontece no ingest</div>')

render_html(
    """
    <div class="flow">
        <div class="flow-step">
            <div class="step-number">A</div>
            <div>
                <div class="step-title">Leitura dos ficheiros</div>
                <p class="step-text">
                    O script de ingest lê os ficheiros da pasta documents e os dados estruturados
                    da pasta data.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">B</div>
            <div>
                <div class="step-title">Criação dos embeddings</div>
                <p class="step-text">
                    Cada bloco de texto é transformado num embedding. É isto que permite fazer
                    pesquisa semântica, mesmo quando a pergunta não usa exatamente as mesmas palavras
                    do ficheiro original.
                </p>
            </div>
        </div>

        <div class="flow-step">
            <div class="step-number">C</div>
            <div>
                <div class="step-title">Gravação na ChromaDB</div>
                <p class="step-text">
                    Os embeddings, o texto original e os metadados das fontes são guardados na base vetorial.
                    Depois disso, o chatbot pesquisa na ChromaDB e não diretamente nos ficheiros txt.
                </p>
            </div>
        </div>
    </div>
    """
)

render_html('<div class="section-title">Regras de segurança aplicadas nas respostas</div>')

render_html(
    """
    <div class="card-grid">
        <div class="card">
            <div class="card-title">Sem invenção de procedimentos</div>
            <p class="card-text">
                O prompt obriga o modelo a usar apenas a informação disponível no contexto recuperado.
                Se não houver informação suficiente, deve responder que não consegue responder com segurança.
            </p>
        </div>

        <div class="card">
            <div class="card-title">Validação em situações de risco</div>
            <p class="card-text">
                Quando existe divergência de stock, produto danificado, dúvida na expedição ou risco operacional,
                o chatbot deve recomendar validação com o responsável do armazém.
            </p>
        </div>
    </div>
    """
)

render_html(
    """
    <div class="warning-card">
        <div class="warning-title">Nota importante sobre atualização dos ficheiros</div>
        <p class="warning-text">
            Quando um ficheiro txt ou csv é alterado, é necessário correr novamente o script de ingest.
            Só assim a ChromaDB fica atualizada com a nova informação. Se o ingest não for executado,
            o chatbot pode continuar a responder com base na versão antiga dos dados.
        </p>
    </div>
    """
)