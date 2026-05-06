# Local Warehouse GPT

## 1) Objetivo do projeto
O `warehouse_gpt_local` é uma plataforma local com chatbot para apoio a operações de armazém e logística.
Combina dados estruturados (stock e localização) com dados não estruturados (procedimentos internos) usando RAG.

## 2) Arquitetura
- **Interface:** Streamlit (`Home`, `Chatbot`, `Como funciona o RAG`)
- **LLM local:** Ollama com `llama3.1:8b` (opcional `llama3.2:3b`)
- **Embeddings:** SentenceTransformers (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Base vetorial:** ChromaDB (`chroma_db`, coleção `warehouse_knowledge`)
- **Pesquisa estruturada:** leitura direta de `data/stock.csv` com Pandas

## 3) Tecnologias usadas
- Python
- Streamlit
- ChromaDB
- Ollama
- SentenceTransformers
- Pandas

## 4) Dados estruturados e não estruturados
- **Não estruturados (`documents/*.txt`):**
  - picking
  - expedição
  - devoluções
  - armazenamento
  - segurança
  - inventário
- **Estruturados (`data/stock.csv`):**
  - SKU
  - Produto
  - Categoria
  - Localização
  - Stock
  - Stock mínimo

## 5) Instalação passo a passo
Criar ambiente virtual:
```bash
python -m venv venv
```

Ativar no Windows:
```bash
venv\Scripts\activate
```

Ativar no Mac/Linux:
```bash
source venv/bin/activate
```

Instalar dependências:
```bash
pip install -r requirements.txt
```

Instalar modelo Ollama:
```bash
ollama pull llama3.1:8b
```

Criar base vetorial:
```bash
python scripts/ingest.py
```

Executar app:
```bash
streamlit run Home.py
```

## 6) Comandos para executar
```bash
python scripts/ingest.py
streamlit run Home.py
```

## 7) Perguntas de teste
- Como faço picking de uma encomenda?
- O que faço se encontrar uma divergência de stock?
- Como processo uma devolução?
- Onde está o SKU TSHIRT-BRANCA-S?
- Qual é o stock do Hoodie Preto?
- O que verificar antes de expedir uma encomenda?
- O que devo fazer se a etiqueta DHL estiver errada?
- Onde guardar produtos danificados?

## 8) Limitações
- A resposta depende da qualidade e atualização dos documentos carregados.
- Sem ingestão prévia (`scripts/ingest.py`), o chatbot não terá base vetorial disponível.
- Em casos críticos, a ferramenta recomenda validação humana e não substitui decisão operacional.

