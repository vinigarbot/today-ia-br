"""Partes comuns do gerador do today.ia.br: configuração, hora de Brasília, leitura das matérias e Markdown simples."""

import html
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

CODIGO = Path(__file__).resolve().parents[1]  # raiz deste repositório (gerador, tema, testes)
# Brasília sem horário de verão desde 2019. Se o horário de verão voltar, trocar por zoneinfo (no Windows exige o pacote tzdata).
BRASILIA = timezone(timedelta(hours=-3), "BRT")
FORMATO_HORA = "%Y-%m-%d %H:%M"
PADRAO_ARQUIVO = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
PADRAO_ASSUNTO = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PALAVRAS_POR_MINUTO = 200

# editorias do menu (maquete v3): "cruza" marca os cruzamentos, que levam o ciano
EDITORIAS = {
    "ia": {"nome": "IA", "menu": "IA", "cruza": False},
    "ia-cripto": {"nome": "IA×Cripto", "menu": 'IA<span class="x">×</span>Cripto', "cruza": True},
    "ia-bolsa": {"nome": "IA×Bolsa", "menu": 'IA<span class="x">×</span>Bolsa', "cruza": True},
    "ia-games": {"nome": "IA×Games", "menu": 'IA<span class="x">×</span>Games', "cruza": True},
    "ia-futebol": {"nome": "IA×Futebol", "menu": 'IA<span class="x">×</span>Futebol', "cruza": True},
    "regulacao": {"nome": "Regulação", "menu": "Regulação", "cruza": False},
}


def carregar_json(nome: str) -> dict:
    return json.loads((CODIGO / "gerador" / nome).read_text(encoding="utf-8"))


def agora_brasilia() -> datetime:
    return datetime.now(BRASILIA)


def ler_hora(texto: str) -> datetime | None:
    """'2026-10-23 08:00' (horário de Brasília) -> datetime com fuso; None se fora do formato."""
    try:
        return datetime.strptime((texto or "").strip(), FORMATO_HORA).replace(tzinfo=BRASILIA)
    except ValueError:
        return None


def em_brasilia(quando: datetime) -> datetime:
    return quando.astimezone(BRASILIA)


# ---------------------------------------------------------------- texto

def tira_marcas(texto: str) -> str:
    """Texto sem as referências [n] e sem as marcas de negrito e itálico."""
    texto = re.sub(r"\s*\[\d+\]", "", texto)
    return re.sub(r"\*+", "", texto).strip()


def inline(texto: str) -> str:
    """Markdown de linha: escapa, converte negrito e itálico e transforma [n] em chamada para a fonte n."""
    texto = html.escape(texto, quote=False)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"(?<![*\w])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![*\w])", r"<em>\1</em>", texto)
    return re.sub(r"\s*\[(\d+)\]", r'<sup><a href="#f\1">\1</a></sup>', texto)


def titulo_html(titulo: str) -> str:
    """No título, *palavra* vira o itálico serifado verde da maquete."""
    texto = html.escape(titulo, quote=False)
    return re.sub(r"\*([^*]+)\*", r'<span class="it">\1</span>', texto)


def palavras(texto: str) -> int:
    return len(tira_marcas(texto).split())


# ---------------------------------------------------------------- matérias

def ler_cabecalho(bruto: str) -> tuple[dict, str] | None:
    m = re.match(r"---\n(.*?)\n---\n?(.*)", bruto, re.DOTALL)
    if not m:
        return None
    meta = {}
    for linha in m.group(1).splitlines():
        if ":" in linha and not linha.lstrip().startswith("#"):
            chave, valor = linha.split(":", 1)
            meta[chave.strip()] = re.sub(r"\s+#\s.*$", "", valor).strip()
    return meta, re.sub(r"<!--.*?-->", "", m.group(2), flags=re.DOTALL)


def ler_blocos(texto: str) -> list[dict]:
    """Corpo da matéria em blocos: parágrafo, intertítulo, lista e quadro de dados."""
    blocos = []
    for bruto in re.split(r"\n\s*\n", texto.strip()):
        linhas = [l.rstrip() for l in bruto.strip().splitlines() if l.strip()]
        if not linhas:
            continue
        primeira = linhas[0]
        if primeira.startswith("## "):
            blocos.append({"tipo": "h2", "texto": primeira[3:].strip()})
            linhas = linhas[1:]
            if not linhas:
                continue
            primeira = linhas[0]
        if primeira.startswith(":::dados"):
            titulo = primeira[len(":::dados"):].strip()
            linhas_dados, fechado = [], False
            for l in linhas[1:]:
                if l.strip() == ":::":
                    fechado = True
                    break
                rotulo, _, valor = l.partition("|")
                linhas_dados.append({"rotulo": rotulo.strip(), "valor": valor.strip()})
            blocos.append({"tipo": "dados", "texto": titulo, "linhas": linhas_dados, "fechado": fechado})
        elif primeira.startswith("- "):
            itens = [l[2:].strip() for l in linhas if l.startswith("- ")]
            blocos.append({"tipo": "lista", "texto": " ".join(itens), "itens": itens})
        else:
            blocos.append({"tipo": "p", "texto": " ".join(l.strip() for l in linhas)})
    return blocos


def ler_materia(arq: Path) -> dict:
    """Lê uma matéria de materias/. Erros de formato vão para 'problemas'; quem decide se para é a trava."""
    problemas = []
    nome = PADRAO_ARQUIVO.match(arq.name)
    if not nome:
        problemas.append("Nome do arquivo fora do formato AAAA-MM-DD-assunto-em-minusculas.md")
    lido = ler_cabecalho(arq.read_text(encoding="utf-8").replace("\r\n", "\n"))
    if lido is None:
        problemas.append("Cabeçalho (entre as linhas ---) não encontrado")
        meta, corpo = {}, ""
    else:
        meta, corpo = lido
    partes = re.split(r"^## Fontes\s*$", corpo, maxsplit=1, flags=re.M)
    texto, fontes_txt = partes[0], (partes[1] if len(partes) > 1 else "")
    fontes = []
    for linha in fontes_txt.splitlines():
        f = re.match(r"^\s*(\d+)\.\s*\[([^\]]+)\]\((\S+?)\)\s*$", linha)
        if f:
            fontes.append({"n": int(f.group(1)), "titulo": f.group(2).strip(), "url": f.group(3)})
        elif linha.strip():
            problemas.append(f"Linha da seção Fontes fora do formato '1. [Título](https://...)': {linha.strip()}")
    blocos = ler_blocos(texto)
    publicar_em = ler_hora(meta.get("publicar_em", ""))
    return {
        "arquivo": arq, "meta": meta, "problemas": problemas,
        "data_arquivo": nome.group(1) if nome else "", "slug": nome.group(2) if nome else arq.stem,
        "titulo": meta.get("titulo", ""), "titulo_puro": tira_marcas(meta.get("titulo", "")),
        "linha_fina": meta.get("linha_fina", ""), "editoria": meta.get("editoria", ""),
        "assunto": meta.get("assunto", ""), "destaque": meta.get("destaque", ""),
        "publicar_em": publicar_em, "coletada_em": ler_hora(meta.get("coletada_em", "")),
        "blocos": blocos, "fontes": fontes, "texto": texto,
        "palavras": sum(palavras(b["texto"]) for b in blocos if b["tipo"] in ("p", "lista", "h2")),
    }


def carregar_materias(pasta: Path) -> list[dict]:
    """Todas as matérias da pasta (o LEIA-ME.md e outros arquivos sem data ficam de fora), da mais nova para a mais antiga."""
    lista = [ler_materia(a) for a in sorted(pasta.glob("*.md")) if re.match(r"^\d{4}-", a.name)]
    return sorted(lista, key=lambda m: (m["publicar_em"] or datetime.min.replace(tzinfo=BRASILIA), m["slug"]), reverse=True)


def toca_investimento(m: dict, termos: list[str]) -> bool:
    """A matéria fala de cripto ou bolsa? Pela editoria ou por algum termo do texto, título ou linha fina."""
    if m["editoria"] in ("ia-cripto", "ia-bolsa"):
        return True
    tudo = " ".join([m["titulo"], m["linha_fina"], m["texto"]]).lower()
    return any(re.search(t, tudo) for t in termos)


def minutos_leitura(m: dict) -> int:
    return max(1, -(-m["palavras"] // PALAVRAS_POR_MINUTO))
