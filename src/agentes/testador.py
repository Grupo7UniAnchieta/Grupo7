"""Nó testador: executa o teste de aceitação e decide se continua ou para."""

from __future__ import annotations

from ..estado import resumo_falha
from ..limites import repetiu
from ..sandbox import rodar

MAX_TENTATIVAS = 5


def executar(estado: dict) -> dict:
    novo = dict(estado)
    teste = estado.get("teste_aceitacao") or "test_issue_01_no_limite_tem_frete_gratis"
    saida, falhas = rodar(estado.get("arquivos") or {}, teste)

    novo["saida_testes"] = saida
    novo["testes_falhando"] = list(falhas)

    if not falhas:
        novo["aprovado"] = True
        return novo

    assinatura = resumo_falha(novo)
    anteriores = list(estado.get("falhas_anteriores") or [])
    if repetiu(anteriores, assinatura):
        novo["motivo_parada"] = "repeticao"
        return novo

    anteriores.append(assinatura)
    novo["falhas_anteriores"] = anteriores

    if int(estado.get("tentativas", 0)) >= MAX_TENTATIVAS:
        novo["motivo_parada"] = "limite_passos"

    return novo
