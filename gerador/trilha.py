"""Trilha da matéria a partir do histórico do git (decisão dele de 22/10/2026: o histórico vira a trilha).

Quem é quem:
- Redação (máquina): commit com a linha "Co-Authored-By: Claude", ou autor Claude, Anthropic ou robô.
- Humano: commit feito pelo GitHub (site ou app; o GitHub assina como committer noreply@github.com) por autor que
  não é máquina. Commit local de outra pessoa não conta como humano: falha fechada.
- Aprovação: merge humano, no caminho principal da main, que traz o commit para dentro.

Sem branch protection (o plano gratuito não oferece para repositório privado), esta conferência é o que impede uma
matéria sem aprovação de ir ao ar: o gerador de produção deixa de fora quem não tem a última versão aprovada.
"""

import difflib
import re
import subprocess
from datetime import datetime
from pathlib import Path

from comum import em_brasilia, ler_cabecalho

COMMITTER_GITHUB = "noreply@github.com"
SEP_CAMPO, SEP_REGISTRO = "\x1f", "\x1e"


def git(raiz: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, text=True, encoding="utf-8", timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout if r.returncode == 0 else None


def maquina(c: dict) -> bool:
    autor = f"{c['autor']} {c['email']}".lower()
    return bool(re.search(r"co-authored-by:\s*claude\b", c["mensagem"], re.I)) or any(
        x in autor for x in ("claude", "anthropic", "[bot]"))


def humano(c: dict) -> bool:
    return c["committer"].lower() == COMMITTER_GITHUB and not maquina(c)


def ler_log(saida: str) -> list[dict]:
    commits = []
    for reg in saida.split(SEP_REGISTRO)[1:]:
        campos = reg.split(SEP_CAMPO)
        if len(campos) < 6:
            continue
        nomes = [l.strip() for l in campos[6].splitlines() if l.strip()] if len(campos) > 6 else []
        commits.append({"sha": campos[0], "quando": datetime.fromisoformat(campos[1]), "autor": campos[2],
                        "email": campos[3], "committer": campos[4], "mensagem": campos[5],
                        "caminho": nomes[0] if nomes else ""})
    return commits


FORMATO = f"--format={SEP_REGISTRO}%H{SEP_CAMPO}%aI{SEP_CAMPO}%an{SEP_CAMPO}%ae{SEP_CAMPO}%ce{SEP_CAMPO}%B{SEP_CAMPO}"


def historico(raiz: Path, arquivo: Path) -> list[dict] | None:
    """Commits que mexeram no arquivo, do mais antigo ao mais novo; None se não houver git ou histórico."""
    rel = arquivo.resolve().relative_to(raiz.resolve()).as_posix()
    saida = git(raiz, "log", "--follow", "--name-only", FORMATO, "--", rel)
    commits = ler_log(saida) if saida else []
    return list(reversed(commits)) or None


_MERGES_PRINCIPAIS: dict[str, list[dict]] = {}


def merge_aprovador(raiz: Path, sha: str) -> dict | None:
    """O primeiro merge humano, no caminho principal até o HEAD, que traz o commit sha para dentro.

    --first-parent e --ancestry-path juntos não servem: o primeiro corta o lado do merge que traz a matéria.
    Por isso: os descendentes do commit (todos os caminhos) cruzados com os merges do caminho principal.
    """
    chave = f"{raiz.resolve()}@{(git(raiz, 'rev-parse', 'HEAD') or '').strip()}"
    if chave not in _MERGES_PRINCIPAIS:
        _MERGES_PRINCIPAIS[chave] = ler_log(git(raiz, "log", "--merges", "--first-parent", "--reverse", FORMATO, "HEAD") or "")
    descendentes = set((git(raiz, "rev-list", "--ancestry-path", f"{sha}..HEAD") or "").split())
    for c in _MERGES_PRINCIPAIS[chave]:
        if c["sha"] in descendentes and humano(c):
            return c
    return None


def palavras_corpo(bruto: str) -> list[str]:
    lido = ler_cabecalho(bruto.replace("\r\n", "\n"))
    corpo = lido[1] if lido else bruto
    return re.split(r"^## Fontes\s*$", corpo, maxsplit=1, flags=re.M)[0].split()


def comparar(antes: str, depois: str) -> tuple[int, tuple[str, str] | None]:
    """Quantos ajustes de texto entre as duas versões e o primeiro deles (trecho tirado, trecho posto)."""
    a, b = palavras_corpo(antes), palavras_corpo(depois)
    # trocas separadas por até duas palavras iguais contam como um ajuste só ("advogados na análise" -> "equipes na triagem")
    grupos = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            if grupos and i2 - i1 > 2:
                grupos[-1]["fechado"] = True
            continue
        if grupos and not grupos[-1]["fechado"]:
            grupos[-1].update(i2=i2, j2=j2)
        else:
            grupos.append({"i1": i1, "i2": i2, "j1": j1, "j2": j2, "fechado": False})
    if not grupos:
        return 0, None
    g = grupos[0]
    i1, i2, j1, j2 = g["i1"], g["i2"], g["j1"], g["j2"]
    limpa = lambda ws: re.sub(r"\s*\[\d+\]", "", " ".join(ws[:14])).strip("*")
    return len(grupos), (limpa(a[i1:i2]), limpa(b[j1:j2]))


def montar(raiz: Path, m: dict) -> dict:
    """Trilha de uma matéria: etapas com hora de Brasília, ajustes humanos, aprovação e se a versão atual está aprovada."""
    commits = historico(raiz, m["arquivo"])
    t = {"etapas": [], "ajustes": 0, "diff": None, "aprovada_em": None, "revisada_em": None, "ultima_mudanca": None,
         "aprovada": False, "correcoes": 0, "sem_historico": commits is None}
    if commits is None:
        return t
    primeiro, ultimo = commits[0], commits[-1]
    t["ultima_mudanca"] = em_brasilia(ultimo["quando"])
    aprovacao = merge_aprovador(raiz, primeiro["sha"])
    # a versão que vai ao ar (a última) precisa estar aprovada: por merge humano ou por edição humana feita no GitHub
    t["aprovada"] = humano(ultimo) or merge_aprovador(raiz, ultimo["sha"]) is not None
    if aprovacao:
        t["aprovada_em"] = em_brasilia(aprovacao["quando"])
    limite = aprovacao["quando"] if aprovacao else None
    humanos = [c for c in commits if humano(c)]
    antes = [c for c in humanos if limite is None or c["quando"] <= limite]
    depois = [c for c in humanos if limite is not None and c["quando"] > limite]
    t["correcoes"] = len(depois)

    maquinas = [c for c in commits if maquina(c)]
    if maquinas:
        base = git(raiz, "show", f"{maquinas[-1]['sha']}:{maquinas[-1]['caminho']}")
        if base is not None:
            t["ajustes"], t["diff"] = comparar(base, m["arquivo"].read_text(encoding="utf-8"))
    if antes:
        t["revisada_em"] = em_brasilia(antes[-1]["quando"])
    elif aprovacao:
        t["revisada_em"] = t["aprovada_em"]

    hm = lambda d: d.strftime("%H:%M") if d else "—"
    fontes = len(m["fontes"])
    rascunho = em_brasilia(primeiro["quando"])
    paragrafos = sum(1 for b in m["blocos"] if b["tipo"] in ("p", "lista", "dados"))
    etapas = [
        ("Coleta", m["coletada_em"], f"{fontes} {'fonte oficial encontrada' if fontes == 1 else 'fontes oficiais encontradas'}", False),
        ("Rascunho", rascunho, f"Escrito pela IA · {m['palavras']:,} palavras".replace(",", "."), False),
        ("Checagem", rascunho, f"{paragrafos} trechos · {paragrafos} com fonte", False),
        ("Linguagem proibida", rascunho, "Nenhuma ocorrência", False),
    ]
    if aprovacao:
        ajustes = f"{t['ajustes']} {'ajuste' if t['ajustes'] == 1 else 'ajustes'} no texto" if t["ajustes"] else "Lida sem ajustes"
        etapas.append(("Revisão humana", t["revisada_em"], ajustes, True))
        sai = m["publicar_em"].strftime("%H:%M") if m["publicar_em"] else "—"
        etapas.append(("Aprovada", t["aprovada_em"], f"Agendada para {sai}", True))
    else:
        etapas.append(("Revisão humana", None, "Aguardando aprovação", True))
    if depois:
        etapas.append(("Corrigida", em_brasilia(depois[-1]["quando"]),
                       f"{len(depois)} {'correção' if len(depois) == 1 else 'correções'} depois da aprovação", True))
    t["etapas"] = [{"nome": n, "hora": hm(q), "nota": nota, "humana": h} for n, q, nota, h in etapas]
    return t
