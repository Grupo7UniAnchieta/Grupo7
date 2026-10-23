from frete import calcular_frete


def test_abaixo_do_limite_paga_frete():
    assert calcular_frete(9999) == 1500


def test_no_limite_tem_frete_gratis():
    assert calcular_frete(10000) == 0


def test_acima_do_limite_tem_frete_gratis():
    assert calcular_frete(10001) == 0
