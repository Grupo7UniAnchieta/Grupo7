"""Testes da política de limites. Não dependem de Ollama nem de Docker."""

import time

from src.limites import Limites, estimar_tokens, pode_chamar, registrar_custo, repetiu

LIM = Limites(max_passos=5, max_tokens=10_000, max_segundos=900, reserva_saida=1_000)


def _estado(**extra):
    base = {"passos": 0, "tokens_entrada": 0, "tokens_saida": 0, "inicio": time.monotonic()}
    base.update(extra)
    return base


def test_permite_chamada_dentro_do_orcamento():
    ok, motivo = pode_chamar(_estado(), 500, LIM)
    assert ok and motivo == ""


def test_bloqueia_ao_atingir_maximo_de_passos():
    ok, motivo = pode_chamar(_estado(passos=5), 500, LIM)
    assert not ok and motivo == "limite_passos"


def test_bloqueia_quando_a_entrada_mais_a_reserva_estoura():
    estado = _estado(tokens_entrada=9_000, tokens_saida=500)
    ok, motivo = pode_chamar(estado, 1_000, LIM)
    assert not ok and motivo == "limite_tokens"


def test_bloqueia_por_tempo():
    ok, motivo = pode_chamar(_estado(inicio=time.monotonic() - 1_000), 100, LIM)
    assert not ok and motivo == "limite_tempo"


def test_registrar_custo_soma_tokens_e_conta_passo():
    estado = _estado()
    registrar_custo(estado, 100, 50)
    assert estado["tokens_entrada"] == 100
    assert estado["tokens_saida"] == 50
    assert estado["passos"] == 1


def test_estimativa_de_tokens_cresce_com_o_texto():
    assert estimar_tokens("a" * 400) == 100


def test_repeticao_exige_duas_falhas_iguais():
    assert not repetiu([], "x")
    assert not repetiu(["x"], "x")
    assert repetiu(["x", "x"], "x")
    assert not repetiu(["x", "y"], "x")
