# PROMPTS.md — Registro de uso de IA

Aqui a gente registra as conversas com IA que influenciaram o projeto: o que pedimos,
o que ela respondeu e o que a gente aceitou, corrigiu ou jogou fora.

## Integrantes

- Rodrigo — Backend e Infraestrutura
- Giovana — IA e Avaliação; também em Dados e Qualidade
- Daniel — Produto e Interface; também em Dados e Qualidade

Ferramentas usadas: Copilot e Perplexity.

---

## 1. Qual pergunta o trabalho responde

**Pedimos:** como transformar o desafio do Tema 7 em uma pergunta que dá para comparar
com algo?

**Ela respondeu:** comparar o grafo multiagente com limites contra uma chamada única ao
mesmo modelo, medindo quantas issues resolve e quanto custa.

**Decisão:** aceitamos com ajuste.

**Por quê:** a comparação só vale se o baseline usar o mesmo modelo, sem grafo e sem
limites. A gente deixou isso escrito.

## 2. Modelo de 3B ou 7B

**Pedimos:** temos notebook sem placa de vídeo. Vale usar o 7B?

**Ela respondeu:** sim, o 7B é melhor.

**Decisão:** corrigimos.

**Por quê:** ela olhou só a qualidade e esqueceu o tempo. Uma issue passa de 15 chamadas.
Em CPU, o 7B gera 2 a 5 tokens por segundo, e as 20 execuções não caberiam no prazo.
Ficamos com o 3B.

## 3. Função base do projeto

**Pedimos:** uma função de frete em Python que devolva 1500 centavos.

**Ela respondeu:** função simples, sem dependência.

**Decisão:** aceitamos.

**Por quê:** é uma regra só, fácil de testar, e serve de ponto de partida.

## 4. O erro do frete grátis

**Pedimos:** frete grátis a partir de R$ 100.

**Ela respondeu:** usou "maior que 10000".

**Decisão:** corrigimos.

**Por quê:** "a partir de" inclui os R$ 100. O certo é "maior ou igual". O teste no valor
exato de 10000 pegou o erro. Guardamos esse caso para a análise de falhas.

## 5. Testes escritos antes de rodar

**Pedimos:** testes para abaixo, no limite, acima e valor inválido.

**Ela respondeu:** quatro testes com assert.

**Decisão:** aceitamos.

**Por quê:** os critérios existiam antes dos agentes rodarem. Isso deixa a avaliação
honesta.

## 6. O que guardar de cada execução

**Pedimos:** quais informações precisamos salvar de cada issue.

**Ela respondeu:** issue, plano, diff, resultado dos testes, parecer, tentativas, passos
e tokens.

**Decisão:** aceitamos com ajuste.

**Por quê:** faltava o motivo da parada. Sem ele não dá para provar que o sistema parou
sozinho ao bater no limite, que é justamente o que o tema cobra.

## 7. Contar tokens direito

**Pedimos:** parar a execução quando o orçamento de tokens acabar.

**Ela respondeu:** comparou só os tokens de saída.

**Decisão:** corrigimos.

**Por quê:** a entrada também gasta, porque o prompt com o arquivo inteiro é reenviado a
cada tentativa. Passamos a reservar entrada mais saída antes de chamar e a corrigir pelo
número real que o Ollama devolve.

## 8. Como saber que travou

**Pedimos:** como detectar que o agente está repetindo sem sair do lugar.

**Ela respondeu:** comparar o hash do diff.

**Decisão:** descartamos.

**Por quê:** se o modelo só muda um espaço, o hash muda e a gente não percebe a repetição.
Trocamos por: mesma mensagem de erro e mesmos testes falhando.

## 9. Rodar código da IA sem risco

**Pedimos:** como rodar em Docker o código que a IA escreve, com o mínimo de acesso.

**Ela respondeu:** um contêiner com a pasta montada.

**Decisão:** aceitamos com ajuste.

**Por quê:** faltava o principal. Colocamos sem rede, disco somente leitura, sem
privilégios, com limite de memória e CPU, e os testes de aceitação travados para escrita.

## 10. Deixar a verificação automática verde

**Pedimos:** como fazer a CI ficar verde antes do sistema completo existir?

**Ela respondeu:** testar o orquestrador, que depende do Ollama e do GitHub.

**Decisão:** corrigimos.

**Por quê:** teste que depende de serviço externo falha na CI. Escrevemos testes da parte
de limites, que roda sem nada externo. A bolinha ficou verde desde o começo.

## 11. Normas ABNT e referências

**Pedimos:** quais são as versões atuais das normas e se dá para melhorar as referências.

**Ela respondeu:** citou NBR 14724 de 2011 e sugeriu blogs para reforçar.

**Decisão:** corrigimos os dois.

**Por quê:** as versões atuais são NBR 14724:2024 e NBR 6023:2025. E blog não vale como
fonte científica. Trocamos por artigos brasileiros publicados na SBC em 2025, além das
documentações oficiais.

## 12. A proposta passou de duas páginas

**Pedimos:** como reduzir a proposta sem perder conteúdo.

**Ela respondeu:** diminuir a fonte do texto.

**Decisão:** descartamos.

**Por quê:** a norma exige tamanho 12 no corpo. Resolvemos trocando a fonte para Times New
Roman, deixando tabelas e referências em 10 e encurtando o texto, sem cortar nada
obrigatório.

---

## O que a IA errou (e o que aprendemos)

- **Olhou só a qualidade e esqueceu o nosso computador:** recomendou o 7B sem pensar no
  tempo de execução.
- **Leu ao pé da letra:** usou "maior que" onde era "a partir de".
- **Solução preguiçosa para CI vermelha:** mandou apagar a verificação em vez de corrigir
  o código.
- **Normas desatualizadas:** citou versões que já foram substituídas.
- **Fonte fraca:** sugeriu blog onde precisávamos de artigo científico.
- **Não contou quantos somos:** propôs 20 funcionalidades diferentes para três pessoas em
  seis semanas.enhum número de token, tempo ou taxa de acerto foi colocado aqui, porque o sistema ainda
não rodou. Inventar número é falta grave.
