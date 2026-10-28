"""Executa o código gerado dentro do contêiner, sem rede e sem privilégios."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

IMAGEM = os.environ.get("SANDBOX_IMAGE", "laboratorio-testes:latest")
RAIZ = Path(__file__).resolve().parent.parent
ACEITACAO = RAIZ / "aceitacao"


def rodar(arquivos: dict, teste: str, timeout: int = 180) -> tuple[str, tuple[str, ...]]:
    """Copia o código para uma pasta temporária e roda um teste de aceitação."""
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
        for nome, conteudo in arquivos.items():
            destino = pasta / nome
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(conteudo, encoding="utf-8")

        comando = [
            "docker", "run", "--rm",
            "--network", "none",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--memory", "512m",
            "--cpus", "1",
            "-v", f"{pasta}:/trabalho",
            "-v", f"{ACEITACAO}:/testes:ro",
            IMAGEM,
            "python", "-m", "pytest", "-q", f"/testes/testes_aceitacao.py::{teste}",
        ]
        try:
            r = subprocess.run(comando, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return "Tempo esgotado na execução dos testes.", ("timeout",)

        saida = ((r.stdout or "") + (r.stderr or ""))[-4000:]
        falhas = []
        for linha in saida.splitlines():
            if linha.startswith("FAILED "):
                falhas.append(linha.split()[1].split("::")[-1])
        return saida, tuple(sorted(set(falhas)))
