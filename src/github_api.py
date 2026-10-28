"""Leitura de issue e abertura de pull request."""

from __future__ import annotations

import os
import subprocess

import requests

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPO", "")
BASE = "https://api.github.com"


def _cabecalhos() -> dict:
    return {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}


def ler_issue(numero: int) -> tuple[str, str]:
    r = requests.get(f"{BASE}/repos/{REPO}/issues/{numero}", headers=_cabecalhos(), timeout=30)
    r.raise_for_status()
    dados = r.json()
    return dados["title"], dados.get("body") or ""


def publicar(arquivos: dict, branch: str, titulo: str, corpo: str) -> str:
    """Grava os arquivos num clone, envia a branch e abre o pull request."""
    pasta = os.environ.get("CLONE_DIR", "/tmp/laboratorio")
    subprocess.run(["git", "clone", f"https://{TOKEN}@github.com/{REPO}.git", pasta], check=True)
    subprocess.run(["git", "checkout", "-B", branch], cwd=pasta, check=True)
    for nome, conteudo in arquivos.items():
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as f:
            f.write(conteudo)
    subprocess.run(["git", "add", "."], cwd=pasta, check=True)
    subprocess.run(["git", "-c", "user.name=agente", "-c", "user.email=agente@local",
                    "commit", "-m", titulo], cwd=pasta, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=pasta, check=True)

    r = requests.post(
        f"{BASE}/repos/{REPO}/pulls",
        headers=_cabecalhos(),
        json={"title": titulo, "head": branch, "base": "main", "body": corpo},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["html_url"]
