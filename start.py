"""Startup script for the Local Warehouse GPT Docker container."""

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = "llama3.2:3b"


def setup_example_data():
    """Copy example data into runtime directories if they are empty."""
    data_dir = Path("data")
    docs_dir = Path("documents")
    data_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)

    stock_file = data_dir / "stock.csv"
    if not stock_file.exists():
        example = Path("data_example/stock_demo.csv")
        if example.exists():
            shutil.copy(example, stock_file)
            print("[setup] Dados de exemplo carregados em data/stock.csv", flush=True)

    if not list(docs_dir.glob("*.txt")):
        example_docs = list(Path("documents_example").glob("*.txt"))
        for f in example_docs:
            shutil.copy(f, docs_dir / f.name)
        if example_docs:
            print(f"[setup] {len(example_docs)} documento(s) de exemplo carregados em documents/", flush=True)


def wait_for_ollama(max_wait_seconds: int = 300) -> bool:
    """Block until the Ollama HTTP endpoint responds or the timeout is reached."""
    url = f"{OLLAMA_HOST}/api/tags"
    print(f"[ollama] A aguardar serviço em {OLLAMA_HOST}...", flush=True)

    deadline = time.time() + max_wait_seconds
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        try:
            urllib.request.urlopen(url, timeout=5)
            print(f"[ollama] Serviço disponível (tentativa {attempt}).", flush=True)
            return True
        except Exception:
            print(f"[ollama] Tentativa {attempt} — a aguardar 5 s...", flush=True)
            time.sleep(5)

    print("[ollama] Timeout: serviço Ollama não ficou disponível.", flush=True)
    return False


def pull_model_if_needed():
    """Pull the LLM model into Ollama if it is not already present."""
    url = f"{OLLAMA_HOST}/api/tags"
    try:
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read())
        existing = [m["name"] for m in data.get("models", [])]
        if any(LLM_MODEL in m for m in existing):
            print(f"[ollama] Modelo {LLM_MODEL} já disponível.", flush=True)
            return
    except Exception:
        pass

    print(f"[ollama] A descarregar modelo {LLM_MODEL} (pode demorar alguns minutos)...", flush=True)
    payload = json.dumps({"name": LLM_MODEL}).encode()
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/pull", data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            for raw_line in resp:
                try:
                    line_data = json.loads(raw_line.decode())
                    status = line_data.get("status", "")
                    if status:
                        print(f"  {status}", flush=True)
                except Exception:
                    pass
        print(f"[ollama] Modelo {LLM_MODEL} pronto!", flush=True)
    except Exception as exc:
        print(f"[ollama] Aviso: não foi possível descarregar o modelo: {exc}", flush=True)


def run_ingest():
    """Run the data ingestion pipeline."""
    print("[ingest] A processar documentos e dados de stock...", flush=True)
    result = subprocess.run([sys.executable, "scripts/ingest.py"])
    if result.returncode != 0:
        print("[ingest] Erro durante a ingestão de dados.", flush=True)
        sys.exit(1)


def start_streamlit():
    """Replace the current process with Streamlit."""
    print("[app] A iniciar Local Warehouse GPT em http://localhost:8501", flush=True)
    os.execvp(
        sys.executable,
        [
            sys.executable,
            "-m", "streamlit", "run", "Home.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true",
        ],
    )


if __name__ == "__main__":
    setup_example_data()
    if not wait_for_ollama():
        sys.exit(1)
    pull_model_if_needed()
    run_ingest()
    start_streamlit()
