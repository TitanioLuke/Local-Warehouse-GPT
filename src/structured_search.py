import re

import pandas as pd

from config import STOCK_FILE


def _format_stock_row(row: pd.Series) -> str:
    stock = int(row["Stock"])
    stock_min = int(row["Stock_Minimo"])
    alerta = (
        "⚠️ **Atenção:** stock no limite ou abaixo do mínimo. Validar com o responsável do armazém."
        if stock <= stock_min
        else "✅ Stock acima do mínimo."
    )

    return (
        f"### Resultado de stock\n"
        f"- **SKU:** {row['SKU']}\n"
        f"- **Produto:** {row['Produto']}\n"
        f"- **Categoria:** {row['Categoria']}\n"
        f"- **Localização:** {row['Localizacao']}\n"
        f"- **Stock atual:** {stock}\n"
        f"- **Stock mínimo:** {stock_min}\n\n"
        f"{alerta}"
    )


def find_stock_answer(question: str) -> str | None:
    """Procura resposta direta no CSV por SKU ou nome de produto."""
    try:
        df = pd.read_csv(STOCK_FILE)
    except Exception:
        return None

    question_clean = question.strip()
    question_lower = question_clean.lower()

    sku_match = re.search(r"\b[A-Z0-9]+(?:-[A-Z0-9]+)+\b", question_clean.upper())
    if sku_match:
        sku = sku_match.group(0)
        rows = df[df["SKU"].str.upper() == sku]
        if not rows.empty:
            return _format_stock_row(rows.iloc[0])

    produto_match = df[
        df["Produto"].str.lower().apply(lambda p: p in question_lower or question_lower in p)
    ]
    if not produto_match.empty:
        return _format_stock_row(produto_match.iloc[0])

    tokens = [t for t in re.findall(r"[a-zA-ZÀ-ÿ0-9]+", question_lower) if len(t) >= 3]
    if tokens:
        regex = "|".join(re.escape(token) for token in tokens)
        partial = df[df["Produto"].str.lower().str.contains(regex, regex=True, na=False)]
        if not partial.empty:
            return _format_stock_row(partial.iloc[0])

    return None
