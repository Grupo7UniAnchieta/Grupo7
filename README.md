# Tema 7 — Do ticket ao pull request: agente de engenharia de software

Projeto da disciplina **Projetos de IA na Programação**.

Sistema multiagente que lê uma issue, planeja a solução, escreve código e testes,
executa a integração contínua e abre um pull request

## Integrantes e papéis

- **Rodrigo Forcinito Cruz** — Backend e Infraestrutura
- **Giovana de Jesus Oliveira** — IA e Avaliação; co-responsável por Dados e Qualidade
- **Daniel Cosme de Santana** — Produto e Interface; co-responsável por Dados e Qualidade

## Problema

Agentes de IA que resolvem issues de software de forma autônoma falham por três motivos:
não sabem quando parar e pedir ajuda humana, entram em loops de correção sem progresso e
consomem tokens sem limite. Um pull request gerado nessas condições gera mais trabalho de
revisão do que economia de tempo.

**Pergunta de pesquisa:** um grafo multiagente com limites explícitos resolve mais issues,
com menor custo por issue, do que uma única chamada ao mesmo modelo?

**Objetivo:** receber uma issue, planejar a solução, escrever código e testes, executar a
CI e abrir o PR, sem intervenção humana nos casos dentro do escopo.

**Escopo:** issues pequenas em Python, com testes de aceitação escritos antes da execução,
em repositório de teste do grupo.

**Fora do escopo:** repositórios grandes, issues ambíguas e qualquer serviço pago.

## Arquitetura

Grafo com estado em LangGraph, executado sobre uma cópia isolada do repositório.

|
 Nó 
|
 Responsabilidade 
|
|
---
|
---
|
|
 Planejador 
|
 Lê a issue e produz o plano. Não grava arquivos. 
|
|
 Programador 
|
 Gera o diff no contêiner Docker, restrito aos caminhos permitidos. 
|
|
 Testador 
|
 Executa o pytest e devolve o erro ao programador. 
|
|
 Revisor 
|
 Confere escopo e estilo antes de abrir o PR. 
|
|
 Escalonamento humano 
|
 Recebe a issue quando um limite é atingido. 
|

Fluxo:

    Issue (GitHub API)
        |
        v
    Planejador --> Programador --> Testador
                        ^              |
                        |              | falha + orcamento disponivel
                        +--------------+
                                       |
                                       | aprovado
                                       v
                                   Revisor --> PR (GitHub API)
                                       |
                                       | limite atingido
                                       v
                              Escalonamento humano

Controles contra loops e custo:

- Máximo de 5 iterações do laço programador–testador.
- Orçamento de tokens e de tempo por issue, verificado antes de cada chamada.
- Detecção de repetição: erro idêntico entre duas iterações escala o caso.
- Detecção de escopo: diffs fora do plano são rejeitados.

## Stack

Python 3.12 · LangGraph · Ollama · Docker e Docker Compose · GitHub API · pytest ·
GitHub Actions.

## Modelo de referência

Qwen2.5-Coder 3B em quantização Q4_K_M, executado localmente via Ollama. Ocupa cerca de
2 GB em disco e exige aproximadamente 4 GB de memória livre, permitindo execução em
notebook doméstico sem GPU dedicada.

Hardware de referência: Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz e RAM 8,0GB DDR3 sem GPU.

## Pré-requisitos

- Python 3.12
- Docker e Docker Compose
- Ollama com o modelo baixado
- Git e uma conta no GitHub

## Testes e integração contínua

- Testes automatizados em tests/, executados com pytest.
- CI em .github/workflows/ci.yml: roda os testes a cada push e pull request.
- Código gerado por IA só entra na branch principal com teste que passa na CI.
- Os testes de aceitação das 20 issues são escritos antes da execução dos agentes e
  mantidos em origem protegida. O agente testador não pode alterá-los.

## Estrutura do repositório

    .
    ├── README.md
    ├── PROMPTS.md
    ├── LICENSE
    ├── docker-compose.yml
    ├── .github/workflows/
    ├── src/
    ├── tests/
    ├── eval/
    ├── evidencias/
    └── docs/

## Uso de IA

As ferramentas de IA utilizadas pelo grupo foram o Copilot e Perflexity.

## Contribuição dos integrantes

| Integrante | Papel | Principais contribuições |
|
---
|
---
|
---
|
|
 Rodrigo 
|
 Backend e Infraestrutura 
|
 Docker, CI e integração com a API do GitHub 
|
|
 Giovana 
|
 IA e Avaliação; co-responsável por Dados e Qualidade 
|
 Grafo LangGraph, agentes, métricas e testes automatizados 
|
|
 Daniel 
|
 Produto e Interface; co-responsável por Dados e Qualidade 
|
 Documentação, pesquisa ABNT, catálogo de issues e datasets 
|

## Licença

Distribuído sob a licença MIT. Veja o arquivo LICENSE.
