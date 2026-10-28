"""Política de parada: passos, tokens e tempo."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Limites:
    max_passos: int = 5
    max_tokens: int = 120_000
    max_segundos: int = 900
    reserva_saida: int = 1_500


PADRAO = Limites()


def estimar_tokens(texto: str) -> int:
    """Estimativa grosseira: cerca de 4 caracteres por token."""
    return max(1, len(texto) // 4)


def tokens_gastos(estado: dict) -> int:
    return int(estado.get("tokens_entrada", 0)) + int(estado.get("tokens_saida", 0))


def pode_chamar(estado: dict, entrada_estimada: int, lim: Limites = PADRAO) -> tuple[bool, str]:
    """Verifica o orçamento ANTES de cada chamada ao modelo.

    Reserva entrada + saída, porque o prompt inteiro é reenviado a cada tentativa.
    """
    if int(estado.get("passos", 0)) >= lim.max_passos:
        return False, "limite_passos"
    necessario = entrada_estimada + lim.reserva_saida
    if tokens_gastos(estado) + necessario > lim.max_tokens:
        return False, "limite_tokens"
    decorrido = time.monotonic() - float(estado.get("inicio") or time.monotonic())
    if decorrido > lim.max_segundos:
        return False, "limite_tempo"
    return True, ""


def registrar_custo(estado: dict, entrada: int, saida: int) -> None:
    estado["tokens_entrada"] = int(estado.get("tokens_entrada", 0)) + int(entrada)
    estado["tokens_saida"] = int(estado.get("tokens_saida", 0)) + int(saida)
    estado["passos"] = int(estado.get("passos", 0)) + 1


def repetiu(falhas: list, nova: str) -> bool:
    """Duas falhas seguidas com a mesma assinatura significam travamento."""
    if not falhas:
        return False
    if falhas[-1] != nova:
        return False
    return len(falhas) >= 2 and falhas[-2] == nova
