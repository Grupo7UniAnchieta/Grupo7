"""Nó planejador: lê a issue e escreve o plano. Não altera arquivos."""

from __future__ import annotations

from ..limites import estimar_tokens, pode_chamar, registrar_custo
from ..ollama_cliente import gerar

SISTEMA = (
    "Você é um engenheiro planejador. Leia a issue e escreva um plano curto em português, "
    "com três itens: arquivos a alterar, regra de negócio e testes que devem passar. "
    "Não escreva código. Seja breve."
)


def executar(estado: dict) -> dict:
    novo = dict(estado)
    prompt = (
        f"Issue #{estado['numero_issue']}: {estado['titulo_issue']}\n\n"
        f"{estado['corpo_issue']}"
    )
    ok, motivo = pode_chamar(novo, estimar_tokens(prompt + SISTEMA))
    if not ok:
        novo["motivo_parada"] = motivo
        return novo
    resposta = gerar(prompt, SISTEMA)
    registrar_custo(novo, resposta.tokens_entrada, resposta.tokens_saida)
    novo["plano"] = resposta.texto
    return novo
