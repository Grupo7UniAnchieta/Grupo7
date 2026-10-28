"""Estado que atravessa todos os nós do grafo."""

from __future__ import annotations

from typing import TypedDict

MOTIVOS = (
    "aprovado",
    "limite_passos",
    "limite_tokens",
    "limite_tempo",
    "repeticao",
    "erro_execucao",
)


class Estado(TypedDict, total=False):
    numero_issue: int
    titulo_issue: str
    corpo_issue: str
    plano: str
    arquivos: dict
    saida_testes: str
    testes_falhando: list
    parecer: str
    aprovado: bool
    tentativas: int
    passos: int
    inicio: float
    tokens_entrada: int
    tokens_saida: int
    motivo_parada: str
    falhas_anteriores: list
    pr_url: str


def estado_inicial(numero_issue: int, titulo: str, corpo: str) -> Estado:
    return Estado(
        numero_issue=numero_issue,
        titulo_issue=titulo,
        corpo_issue=corpo,
        plano="",
        arquivos={},
        saida_testes="",
        testes_falhando=[],
        parecer="",
        aprovado=False,
        tentativas=0,
        passos=0,
        tokens_entrada=0,
        tokens_saida=0,
        motivo_parada="",
        falhas_anteriores=[],
        pr_url="",
    )


def resumo_falha(estado: Estado) -> str:
    """Assinatura curta da falha, usada para detectar repetição sem progresso."""
    nomes = ",".join(sorted(estado.get("testes_falhando") or []))
    linhas = (estado.get("saida_testes") or "").strip().splitlines()
    erro = linhas[-1][:120] if linhas else "sem_saida"
    return f"{nomes}|{erro}"
