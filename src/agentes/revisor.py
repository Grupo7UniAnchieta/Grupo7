"""Nó revisor: confere escopo e estilo. Só depois o pull request é aberto."""

from __future__ import annotations

from ..limites import estimar_tokens, pode_chamar, registrar_custo
from ..ollama_cliente import gerar

SISTEMA = (
    "Você é um revisor de código. Leia o plano e o código e responda em duas linhas, "
    "começando por APROVADO ou AJUSTAR. Aponte só problemas de escopo, ou seja, "
    "coisas que o plano não pedia."
)


def executar(estado: dict) -> dict:
    novo = dict(estado)
    codigo = (estado.get("arquivos") or {}).get("frete.py", "")
    prompt = f"Plano:\n{estado['plano']}\n\nCódigo:\n{codigo}"

    ok, motivo = pode_chamar(novo, estimar_tokens(prompt + SISTEMA))
    if not ok:
        novo["motivo_parada"] = motivo
        return novo

    resposta = gerar(prompt, SISTEMA, temperatura=0.0)
    registrar_custo(novo, resposta.tokens_entrada, resposta.tokens_saida)
    novo["parecer"] = resposta.texto.strip()
    novo["aprovado"] = novo["parecer"].upper().startswith("APROVADO")
    return novo
