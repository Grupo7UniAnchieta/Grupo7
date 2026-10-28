"""Ponto de entrada: python -m src.main --issue 1"""

from __future__ import annotations

import argparse
import json
import time

from .estado import estado_inicial
from .grafo import montar

ISSUE_FALSA = (
    "Frete grátis a partir de R$ 100",
    "A função calcular_frete deve devolver 0 quando o subtotal for maior ou igual a "
    "10000 centavos, e 1500 abaixo disso.",
)


def main() -> int:
    p = argparse.ArgumentParser(description="Resolve uma issue e abre um pull request.")
    p.add_argument("--issue", type=int, required=True)
    p.add_argument("--simular", action="store_true", help="Usa a issue local, sem GitHub.")
    p.add_argument("--teste", default="test_issue_01_no_limite_tem_frete_gratis")
    args = p.parse_args()

    if args.simular:
        titulo, corpo = ISSUE_FALSA
    else:
        from .github_api import ler_issue

        titulo, corpo = ler_issue(args.issue)

    estado = estado_inicial(args.issue, titulo, corpo)
    estado["inicio"] = time.monotonic()
    estado["teste_aceitacao"] = args.teste

    resultado = montar().invoke(estado)

    print(json.dumps(
        {
            "issue": args.issue,
            "aprovado": resultado.get("aprovado", False),
            "tentativas": resultado.get("tentativas", 0),
            "passos": resultado.get("passos", 0),
            "tokens": resultado.get("tokens_entrada", 0) + resultado.get("tokens_saida", 0),
            "motivo_parada": resultado.get("motivo_parada", ""),
            "parecer": resultado.get("parecer", ""),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0 if resultado.get("aprovado") else 1


if __name__ == "__main__":
    raise SystemExit(main())
