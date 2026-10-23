"""Monta um repositório de exemplo com o fluxo da redação simulado, para testes e fotos.

Uso:  python -I testes/montar_exemplo.py PASTA_NOVA

Para cada matéria de testes/exemplos/: ramo próprio, commit da redação (com "Co-Authored-By: Claude"),
ajuste humano feito "pelo GitHub" (committer noreply@github.com) na matéria de raciocínio, e merge de aprovação
humano às 07:52 do dia da publicação. As datas são fixas, para o resultado ser sempre o mesmo.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

CODIGO = Path(__file__).resolve().parents[1]
EXEMPLOS = CODIGO / "testes" / "exemplos"
REDACAO = ("Claude", "noreply@anthropic.com")
REVISOR = ("Revisor Exemplo", "revisor@example.com")  # pessoa inventada
GITHUB = ("GitHub", "noreply@github.com")
TRAILER = "\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
AJUSTE = ("já substituem advogados na análise", "auxiliam equipes jurídicas na triagem")


def git(pasta: Path, *args: str, autor=REDACAO, committer=REDACAO, quando: str = "2026-10-18T09:00:00-03:00") -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME=autor[0], GIT_AUTHOR_EMAIL=autor[1], GIT_COMMITTER_NAME=committer[0],
               GIT_COMMITTER_EMAIL=committer[1], GIT_AUTHOR_DATE=quando, GIT_COMMITTER_DATE=quando)
    subprocess.run(["git", "-C", str(pasta), "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
                   check=True, env=env, capture_output=True)


def montar(destino: Path, so: list[str] | None = None, aprovar: bool = True) -> Path:
    destino.mkdir(parents=True, exist_ok=False)
    git(destino, "init", "-q", "-b", "main")
    (destino / "materias").mkdir()
    (destino / "materias" / "LEIA-ME.md").write_text("Repositório de exemplo.\n", encoding="utf-8")
    if (CODIGO / "dados" / "radar.json").exists():
        (destino / "dados").mkdir()
        shutil.copy(CODIGO / "dados" / "radar.json", destino / "dados" / "radar.json")
    git(destino, "add", "-A")
    git(destino, "commit", "-q", "-m", "Início" + TRAILER)
    for n, arq in enumerate(sorted(EXEMPLOS.glob("2*.md")), start=1):
        if so and arq.name not in so:
            continue
        dia = arq.name[:10]
        ramo = "materia/" + arq.stem
        git(destino, "switch", "-q", "-c", ramo, "main")
        shutil.copy(arq, destino / "materias" / arq.name)
        git(destino, "add", "-A")
        git(destino, "commit", "-q", "-m", f"Matéria {arq.stem}" + TRAILER, quando=f"{dia}T06:03:00-03:00")
        if AJUSTE[0] in arq.read_text(encoding="utf-8"):
            alvo = destino / "materias" / arq.name
            alvo.write_text(alvo.read_text(encoding="utf-8").replace(AJUSTE[0], AJUSTE[1]), encoding="utf-8")
            git(destino, "commit", "-q", "-am", "Ajuste no texto", autor=REVISOR, committer=GITHUB, quando=f"{dia}T07:49:00-03:00")
        git(destino, "switch", "-q", "main")
        if aprovar:
            git(destino, "merge", "-q", "--no-ff", ramo, "-m", f"Merge pull request #{n} from {ramo}",
                autor=REVISOR, committer=GITHUB, quando=f"{dia}T07:52:00-03:00")
    return destino


if __name__ == "__main__":
    print(montar(Path(sys.argv[1]).resolve()))
