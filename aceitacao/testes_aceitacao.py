"""Testes de aceitação das 20 issues. Escritos antes da execução dos agentes."""

import pytest

from frete import calcular_frete


def test_issue_01_no_limite_tem_frete_gratis():
    assert calcular_frete(10000) == 0


def test_issue_02_abaixo_do_limite_paga_frete():
    assert calcular_frete(9999) == 1500


def test_issue_03_valor_negativo_levanta_erro():
    with pytest.raises(ValueError):
        calcular_frete(-1)


def test_issue_04_valor_fracionario_e_truncado():
    assert calcular_frete(9999.9) == 1500


def test_issue_05_cupom_frete_gratis_zera():
    assert calcular_frete(5000, cupom="FRETEGRATIS") == 0


def test_issue_06_cupom_dez_por_cento_desconta():
    assert calcular_frete(5000, cupom="FRETE10") == 1350


def test_issue_07_retirada_na_loja_zera():
    assert calcular_frete(5000, retirada=True) == 0


def test_issue_08_expresso_adiciona_dois_mil():
    assert calcular_frete(5000, expresso=True) == 3500


def test_issue_09_expresso_cobra_mesmo_com_frete_gratis():
    assert calcular_frete(10000, expresso=True) == 2000


def test_issue_10_centro_oeste_adiciona_mil():
    assert calcular_frete(5000, regiao="Centro-Oeste") == 2500


def test_issue_11_nordeste_adiciona_dois_mil():
    assert calcular_frete(5000, regiao="Nordeste") == 3500


def test_issue_12_norte_adiciona_dois_mil():
    assert calcular_frete(5000, regiao="Norte") == 3500


def test_issue_13_regiao_invalida_levanta_erro():
    with pytest.raises(ValueError):
        calcular_frete(5000, regiao="Atlantida")


def test_issue_14_cep_invalido_levanta_erro():
    with pytest.raises(ValueError):
        calcular_frete(5000, cep="123")


def test_issue_15_cep_com_mascara_e_aceito():
    assert calcular_frete(5000, cep="01310-100") == 1500


def test_issue_16_peso_acima_de_cinco_adiciona_quinhentos_por_kg():
    assert calcular_frete(5000, peso_kg=7) == 2500


def test_issue_17_primeira_compra_gratis_ate_duzentos_e_cinquenta():
    assert calcular_frete(25000, primeira_compra=True) == 0


def test_issue_18_internacional_nunca_e_gratis():
    assert calcular_frete(20000, internacional=True) == 5000


def test_issue_19_resultado_deterministico():
    assert len({calcular_frete(5000) for _ in range(3)}) == 1


def test_issue_20_retirada_vence_expresso():
    assert calcular_frete(5000, retirada=True, expresso=True) == 0
