"""Nó programador: gera o conteúdo completo de src/frete.py."""

from __future__ import annotations

from ..limites import estimar_tokens, pode_chamar, registrar_custo
from ..ollama_cliente import gerar, limpar_cerca

ARQUIVO = "src/frete.py"

SISTEMA = (
    "Você é um programador Python. Responda SOMENTE com o conteúdo completo do arquivo "
    "frete.py, sem explicações e sem blocos de markdown. "
    "A função principal deve se chamar calcular_frete e receber subtotal_centavos "
    "em centavos inteiros. Não use bibliotecas externas."
)


def executar(estado: dict) -> dict:
    novo = dict(estado)
    falha = ""
    if estado.get("saida_testes"):
        falha = (
            "\n\nA tentativa anterior falhou. Corrija apenas o necessário:\n"
            f"{estado['saida_testes'][-2000:]}"
        )
    prompt = (
        f"Plano aprovado:\n{estado['plano']}\n\n"
        f"Código atual:\n{estado.get('arquivos', {}).get(ARQUIVO, '(vazio)')}"
        f"{falha}"
    )
    ok, motivo = pode_chamar(novo, estimar_tokens(prompt + SISTEMA))
    if not ok:
        novo["motivo_parada"] = motivo
        return novo

    resposta = gerar(prompt, SISTEMA)
    registrar_custo(novo, resposta.tokens_entrada, resposta.tokens_saida)

    arquivos = dict(estado.get("arquivos") or {})
    arquivos[ARQUIVO] = limpar_cerca(resposta.texto)
    novo["arquivos"] = arquivos
    novo["tentativas"] = int(estado.get("tentativas", 0)) + 1
    return novo
