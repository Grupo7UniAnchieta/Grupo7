# Catálogo das 20 issues

Cada linha vira uma issue no repositório de teste. O teste de aceitação já existe e
não pode ser alterado pelo agente.

| # | Título | Regra | Categoria de falha esperada |
|---|---|---|---|
| 1 | Frete grátis no limite exato | Subtotal 10000 devolve 0 | interpretação de fronteira |
| 2 | Frete cobrado abaixo do limite | Subtotal 9999 devolve 1500 | regressão da regra base |
| 3 | Valor negativo é inválido | Subtotal negativo levanta ValueError | validação de entrada |
| 4 | Valor fracionário é truncado | 9999.9 vira 9999 | tipo de dado |
| 5 | Cupom de frete grátis | Cupom FRETEGRATIS devolve 0 | nova regra sem quebrar a antiga |
| 6 | Cupom de 10 por cento | FRETE10 aplica 10 por cento sobre o frete | cálculo proporcional |
| 7 | Retirada na loja | Retirada devolve 0 | prioridade entre regras |
| 8 | Frete expresso | Expresso soma 2000 | adicional fixo |
| 9 | Expresso sobre frete grátis | Cobra 2000 mesmo com frete base zero | conflito entre regras |
| 10 | Região Centro-Oeste | Soma 1000 | tabela de valores |
| 11 | Região Nordeste | Soma 2000 | tabela de valores |
| 12 | Região Norte | Soma 2000 | tabela de valores |
| 13 | Região inválida | Levanta ValueError | validação |
| 14 | CEP inválido | Menos de 8 dígitos levanta ValueError | validação |
| 15 | CEP com máscara | Aceita 01310-100 | normalização |
| 16 | Peso acima de 5 kg | Soma 500 por kg excedente | cálculo com faixa |
| 17 | Primeira compra | Grátis até 25000 | regra promocional |
| 18 | Frete internacional | Cobra 5000 e nunca é grátis | prioridade entre regras |
| 19 | Determinismo | Mesma entrada, mesma saída | estabilidade |
| 20 | Retirada vence expresso | Retirada zera mesmo com expresso | ordem de prioridade |

## Prioridade entre regras

Quando duas regras se cruzam, vale esta ordem, da mais forte para a mais fraca:
retirada na loja, frete internacional, cupom, frete grátis por valor, regras normais.

## Como usar

Cada issue é executada individualmente pelo seletor do pytest:

    python -m pytest aceitacao/testes_aceitacao.py::test_issue_05_cupom_frete_gratis_zera
