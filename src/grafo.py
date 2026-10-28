"""Monta o fluxo: planejador -> programador -> testador -> revisor ou volta."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from .agentes import planejador, programador, revisor, testador
from .estado import Estado


def decidir(estado: dict) -> str:
    if estado.get("motivo_parada"):
        return "fim"
    if estado.get("aprovado"):
        return "revisor"
    return "programador"


def montar():
    g = StateGraph(Estado)
    g.add_node("planejador", planejador.executar)
    g.add_node("programador", programador.executar)
    g.add_node("testador", testador.executar)
    g.add_node("revisor", revisor.executar)

    g.set_entry_point("planejador")
    g.add_edge("planejador", "programador")
    g.add_edge("programador", "testador")
    g.add_conditional_edges(
        "testador", decidir, {"programador": "programador", "revisor": "revisor", "fim": END}
    )
    g.add_edge("revisor", END)
    return g.compile()
