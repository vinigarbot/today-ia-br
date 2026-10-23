"""Travas das matérias do today.ia.br (decisões dele de 22/10/2026).

Uso:
  python -I gerador/travas.py                     confere todas as matérias de materias/
  python -I gerador/travas.py materias/arq.md     confere só os arquivos indicados

Sai com código 1 se alguma matéria tiver erro. Erro impede a publicação; alerta só pede o olho dele no pull request.
Com GITHUB_STEP_SUMMARY definido (GitHub Actions), o relatório também vai para o resumo da verificação.

O que a máquina não consegue conferir fica na lista de leitura do pull request: o título afirmar só o que a fonte
diz, não esconder o assunto real e o texto entregar o que o título promete.
"""

import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))  # com python -I, a pasta do script não entra sozinha

from comum import CODIGO, EDITORIAS, PADRAO_ASSUNTO, carregar_json, carregar_materias, ler_materia, tira_marcas, toca_investimento

# títulos: gancho com trava. As três primeiras são dele; as demais são irmãs delas (régua 13), sujeitas ao veto dele.
PROIBIDAS_TITULO = ["você não vai acreditar", "chocante", "urgente",
                    "inacreditável", "bombástic", "imperdível", "ninguém esperava", "você precisa ver", "última hora"]
# linguagem de recomendação de investimento: bloqueia
PROIBIDAS_INVESTIMENTO = [
    r"\bcomprem?\b", r"\bvale a pena investir\b", r"\bpreço[- ]alvo\b", r"\bvenda (já|agora)\b",
    r"\bhora de (comprar|vender)\b", r"\b(recomendamos|recomenda-se|recomendação de) (a )?(compra|venda)\b",
    r"\boportunidade de (compra|venda)\b", r"\binvista (já|agora|em)\b", r"\bvale a pena (comprar|vender)\b",
]
# "venda" e "comprar" são palavras comuns no noticiário ("a venda da divisão"), e "pode subir" vale para custo e uso;
# em matéria que toca investimento, viram alerta para ele olhar, não bloqueio
ALERTA_INVESTIMENTO = [r"\bvenda\b", r"\bvender\b", r"\bcomprar\b", r"\b(deve|devem|pode|podem) (subir|disparar|valorizar)\b"]
TRECHO_LITERAL_MAX = 25  # palavras entre aspas; acima disso é cópia, não citação
PALAVRAS_MINIMO = 300    # abaixo disso, alerta de matéria rasa (política do Google e do AdSense)


def dominio_oficial(url: str, oficiais: dict) -> str | None:
    """Quem publica a URL, se o domínio estiver na lista de fontes oficiais; None se não estiver (falha fechada)."""
    host = (urlparse(url).hostname or "").lower()
    for d in oficiais["dominios"]:
        if host == d["dominio"] or host.endswith("." + d["dominio"]):
            return d["quem"]
    for s in oficiais["sufixos_publicos"]:
        if host.endswith(s["sufixo"]):
            return s["quem"]
    return None


def tem_emoji(texto: str) -> bool:
    return any(unicodedata.category(c) == "So" or 0x1F000 <= ord(c) <= 0x1FAFF or ord(c) == 0xFE0F for c in texto)


def verificar(m: dict, cfg: dict, oficiais: dict, slugs_repetidos: set[str] = frozenset()) -> tuple[list[str], list[str]]:
    """Devolve (erros, alertas) de uma matéria."""
    erros, alertas = list(m["problemas"]), []
    meta = m["meta"]

    # cabeçalho
    for campo in ("titulo", "linha_fina", "editoria", "publicar_em", "coletada_em"):
        if not meta.get(campo):
            erros.append(f"Falta o campo '{campo}' no cabeçalho")
    if m["editoria"] and m["editoria"] not in EDITORIAS:
        erros.append(f"Editoria '{m['editoria']}' não existe (use: {', '.join(EDITORIAS)})")
    if m["editoria"] in ("ia", "regulacao") and not m["assunto"]:
        erros.append("Falta o campo 'assunto' (vira o caminho ~/ia/assunto)")
    if m["assunto"] and not PADRAO_ASSUNTO.match(m["assunto"]):
        erros.append("O 'assunto' deve ser em minúsculas, sem acento, com hífen no lugar de espaço")
    if meta.get("publicar_em") and not m["publicar_em"]:
        erros.append("'publicar_em' fora do formato AAAA-MM-DD HH:MM (horário de Brasília)")
    if meta.get("coletada_em") and not m["coletada_em"]:
        erros.append("'coletada_em' fora do formato AAAA-MM-DD HH:MM (horário de Brasília)")
    if m["publicar_em"] and m["data_arquivo"] and m["publicar_em"].strftime("%Y-%m-%d") != m["data_arquivo"]:
        erros.append("A data do nome do arquivo deve ser a mesma de 'publicar_em'")
    if m["publicar_em"] and m["coletada_em"] and m["coletada_em"] > m["publicar_em"]:
        erros.append("'coletada_em' não pode ser depois de 'publicar_em'")
    if m["slug"] in slugs_repetidos:
        erros.append(f"Já existe outra matéria com o endereço '{m['slug']}'")

    # título e linha fina
    manchete = f"{m['titulo_puro']} {m['linha_fina']}".lower()
    for p in PROIBIDAS_TITULO:
        if p in manchete:
            erros.append(f"Título ou linha fina com expressão proibida: '{p}'")
    if tem_emoji(m["titulo"] + m["linha_fina"]):
        erros.append("Título ou linha fina com emoji")
    siglas = {s.upper() for s in cfg["siglas_permitidas"]}
    letras = [c for c in m["titulo_puro"] if c.isalpha()]
    gritadas = [w for w in re.findall(r"[^\W\d_]+", m["titulo_puro"]) if len(w) >= 5 and w.isupper() and w not in siglas]
    if gritadas or (letras and sum(c.isupper() for c in letras) / len(letras) > 0.5):
        erros.append(f"Título em maiúsculas: {', '.join(gritadas) or m['titulo_puro']}")
    corpo_puro = tira_marcas(m["texto"])
    for numero in re.findall(r"\d+(?:[.,]\d+)?", m["titulo_puro"]):
        if not re.search(rf"(?<![\d.,]){re.escape(numero)}(?![\d]|[.,]\d)", corpo_puro):
            erros.append(f"O número {numero} do título não aparece no texto")

    # linguagem de investimento (título, linha fina, destaque e texto)
    tudo = f"{m['titulo_puro']} {m['linha_fina']} {m['destaque']} {corpo_puro}".lower()
    for p in PROIBIDAS_INVESTIMENTO:
        achado = re.search(p, tudo)
        if achado:
            erros.append(f"Linguagem de recomendação de investimento: '{achado.group(0)}'")
    if toca_investimento(m, cfg["termos_investimento"]):
        for p in ALERTA_INVESTIMENTO:
            achado = re.search(p, tudo)
            if achado:
                alertas.append(f"Matéria que toca cripto ou bolsa usa '{achado.group(0)}': conferir que não soa como recomendação")
                break

    # fontes: só oficiais, com link, todas citadas, toda chamada com fonte
    fontes = m["fontes"]
    if not fontes:
        erros.append("Sem a seção '## Fontes' com pelo menos um link da fonte original")
    if [f["n"] for f in fontes] != list(range(1, len(fontes) + 1)):
        erros.append("As fontes devem ser numeradas 1, 2, 3... sem pular número")
    for f in fontes:
        if not f["url"].startswith("https://"):
            erros.append(f"Fonte [{f['n']}] sem https: {f['url']}")
        elif not dominio_oficial(f["url"], oficiais):
            erros.append(f"Fonte [{f['n']}] fora da lista de fontes oficiais: {urlparse(f['url']).hostname}")
    citadas = {int(n) for b in m["blocos"] for n in re.findall(r"\[(\d+)\]", b["texto"])}
    for n in sorted(citadas - {f["n"] for f in fontes}):
        erros.append(f"Chamada [{n}] sem fonte correspondente")
    for f in fontes:
        if f["n"] not in citadas:
            erros.append(f"Fonte [{f['n']}] listada e não citada no texto")
    sem_fonte = [b for b in m["blocos"] if b["tipo"] in ("p", "lista", "dados") and not re.search(r"\[\d+\]", b["texto"])]
    for b in sem_fonte:
        erros.append(f"Trecho sem fonte: \"{tira_marcas(b['texto'])[:70]}...\"")
    if re.search(r"\]\(", m["texto"]):
        erros.append("Link solto no texto: todo link vai na seção Fontes e é chamado por [n]")
    for b in m["blocos"]:
        if b["tipo"] == "dados":
            if not b["fechado"]:
                erros.append("Quadro de dados sem a linha ':::' de fechamento")
            if not b["linhas"] or any(not re.fullmatch(r"\d+(?:[.,]\d+)?", l["valor"]) for l in b["linhas"]):
                erros.append("Quadro de dados com valor que não é número (formato: rótulo | 74)")

    # cópia: trecho literal longo entre aspas
    for trecho in re.findall(r"[\"“]([^\"”]+)[\"”]", corpo_puro):
        if len(trecho.split()) > TRECHO_LITERAL_MAX:
            erros.append(f"Trecho entre aspas com mais de {TRECHO_LITERAL_MAX} palavras: \"{trecho[:60]}...\"")
    if m["destaque"] and tira_marcas(m["destaque"]).lower() not in " ".join(tira_marcas(b["texto"]) for b in m["blocos"]).lower():
        erros.append("O 'destaque' deve ser uma frase igual à do próprio texto")
    if m["palavras"] < PALAVRAS_MINIMO:
        alertas.append(f"Matéria curta ({m['palavras']} palavras; referência: {PALAVRAS_MINIMO})")
    return erros, alertas


def verificar_todas(materias: list[dict], cfg: dict | None = None, oficiais: dict | None = None) -> dict[str, tuple[list[str], list[str]]]:
    cfg = cfg or carregar_json("config.json")
    oficiais = oficiais or carregar_json("fontes_oficiais.json")
    contagem = {}
    for m in materias:
        contagem[m["slug"]] = contagem.get(m["slug"], 0) + 1
    repetidos = {s for s, n in contagem.items() if n > 1}
    return {m["arquivo"].name: verificar(m, cfg, oficiais, repetidos) for m in materias}


def relatorio(resultado: dict[str, tuple[list[str], list[str]]]) -> str:
    linhas = []
    for nome, (erros, alertas) in sorted(resultado.items()):
        situacao = "não passa" if erros else ("passa, com alerta" if alertas else "passa")
        linhas.append(f"### {nome}: {situacao}")
        linhas += [f"- Erro: {e}" for e in erros] + [f"- Alerta: {a}" for a in alertas]
        linhas.append("")
    return "\n".join(linhas) if linhas else "Nenhuma matéria para conferir.\n"


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    todas =carregar_materias(CODIGO / "materias")
    pedidas = {Path(a).resolve() for a in argv}
    de_fora = [ler_materia(p) for p in pedidas if p not in {m["arquivo"].resolve() for m in todas}]
    resultado = verificar_todas(todas + de_fora)  # todas entram, para achar endereço repetido
    if pedidas:
        resultado = {k: v for k, v in resultado.items() if k in {p.name for p in pedidas}}
    texto = relatorio(resultado)
    print(texto)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("## Travas das matérias\n\n" + texto + "\n")
    return 1 if any(erros for erros, _ in resultado.values()) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
