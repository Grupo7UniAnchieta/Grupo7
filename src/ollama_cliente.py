"""Cliente mínimo para o Ollama rodando na máquina."""

from __future__ import annotations

import os

import requests

URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODELO = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:3b")


class Resposta:
    def __init__(self, texto: str, tokens_entrada: int, tokens_saida: int):
        self.texto = texto
        self.tokens_entrada = tokens_entrada
        self.tokens_saida = tokens_saida


def gerar(prompt: str, sistema: str = "", temperatura: float = 0.2) -> Resposta:
    corpo = {
        "model": MODELO,
        "prompt": prompt,
        "system": sistema,
        "stream": False,
        "options": {"temperature": temperatura, "num_predict": 1500},
    }
    resposta = requests.post(f"{URL}/api/generate", json=corpo, timeout=600)
    resposta.raise_for_status()
    dados = resposta.json()
    return Resposta(
        texto=dados.get("response", ""),
        tokens_entrada=int(dados.get("prompt_eval_count", 0)),
        tokens_saida=int(dados.get("eval_count", 0)),
    )


def limpar_cerca(texto: str) -> str:
    """Remove blocos de markdown que o modelo insiste em colocar."""
    linhas = texto.strip().splitlines()
    if linhas and linhas[0].startswith("```"):
        linhas = linhas[1:]
    if linhas and linhas[-1].startswith("```"):
        linhas = linhas[:-1]
    return "\n".join(linhas).strip() + "\n"
