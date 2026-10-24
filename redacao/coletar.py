"""Coletor de pautas da redação diária do today.ia.br: o que as fontes oficiais publicaram nas últimas horas.

Uso:
  python -I redacao/coletar.py               lista em texto, das últimas 48 horas
  python -I redacao/coletar.py --horas 24    outra janela
  python -I redacao/coletar.py --json        a mesma lista em JSON

Lê os feeds de redacao/fontes.json, deixa de fora o que não é domínio oficial (gerador/fontes_oficiais.json) e o que
já foi citado em alguma matéria de materias/, e acrescenta as movimentações recentes do PL 2338/2023 na Câmara.
Fonte que falha não derruba as outras: aparece no fim, com o motivo. Sai com código 1 só se todas falharem.
"""

import argparse
import gzip
import json
import sys
import zlib
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "gerador"))  # com python -I, as pastas do projeto não entram sozinhas

from comum import BRASILIA, carregar_json, carregar_materias  # noqa: E402
from travas import dominio_oficial  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"
AGENTE = "today.ia.br (coletor de pautas)"


def descompactar(bruto: bytes, codificacao: str = "") -> bytes:
    """Na nuvem, a rede pede compressão por conta própria e o feed chega compactado (DeepMind, 24/10/2026)."""
    codificacao = (codificacao or "").lower().strip()
    if codificacao == "gzip" or bruto[:2] == b"\x1f\x8b":
        return gzip.decompress(bruto)
    if codificacao == "deflate":
        try:
            return zlib.decompress(bruto)
        except zlib.error:
            return zlib.decompress(bruto, -zlib.MAX_WBITS)  # deflate sem cabeçalho
    return bruto


def buscar(url: str, aceita: str = "application/rss+xml, application/atom+xml, application/xml, */*") -> bytes:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": aceita, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(pedido, timeout=25) as r:
        return descompactar(r.read(), r.headers.get("Content-Encoding", ""))


def ler_data(texto: str) -> datetime | None:
    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        d = parsedate_to_datetime(texto)  # RSS: "Thu, 22 Oct 2026 16:00:00 GMT"
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(texto.replace("Z", "+00:00"))  # Atom e API: ISO 8601
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=BRASILIA)


def ler_feed(bruto: bytes) -> list[dict]:
    """Itens de um feed RSS 2.0 ou Atom: título, link e data."""
    raiz = ET.fromstring(bruto)
    itens = []
    for item in raiz.iter("item"):
        itens.append({"titulo": (item.findtext("title") or "").strip(), "link": (item.findtext("link") or "").strip(),
                      "data": ler_data(item.findtext("pubDate") or item.findtext("{http://purl.org/dc/elements/1.1/}date"))})
    for entrada in raiz.iter(ATOM + "entry"):
        link = entrada.find(ATOM + "link[@rel='alternate']")
        if link is None:
            link = entrada.find(ATOM + "link")
        itens.append({"titulo": (entrada.findtext(ATOM + "title") or "").strip(),
                      "link": (link.get("href") if link is not None else "").strip(),
                      "data": ler_data(entrada.findtext(ATOM + "published") or entrada.findtext(ATOM + "updated"))})
    return itens


def normalizar(url: str) -> str:
    return url.split("#")[0].split("?")[0].rstrip("/").lower()


def ja_citados(pasta: Path) -> set[str]:
    return {normalizar(f["url"]) for m in carregar_materias(pasta) for f in m["fontes"]}


def tramitacoes(cfg: dict, agora: datetime, busca) -> list[dict]:
    inicio = (agora - timedelta(days=cfg["dias"])).strftime("%Y-%m-%d")
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{cfg['id']}/tramitacoes?dataInicio={inicio}"
    dados = json.loads(busca(url, aceita="application/json").decode("utf-8"))["dados"]  # sem isso a API devolve XML
    return [{"titulo": f"{cfg['nome']}: {t.get('descricaoTramitacao') or ''} — {(t.get('despacho') or '').strip()}".strip(" —"),
             "link": cfg["pagina"], "data": ler_data(t.get("dataHora"))} for t in dados]


def coletar(fontes: dict, oficiais: dict, citados: set[str], agora: datetime, horas: int, busca=buscar) -> dict:
    limite = agora - timedelta(hours=horas)
    pautas, falhas, fora = [], [], []
    for f in fontes["rss"]:
        bruto = b""
        try:
            bruto = busca(f["url"])
            itens = ler_feed(bruto)
        except Exception as erro:  # rede, bloqueio do ambiente ou XML quebrado: segue com as outras fontes
            inicio = f" | início recebido: {bruto[:16]!r}" if bruto else ""  # para diagnosticar o que chegou no lugar do feed
            falhas.append({"quem": f["quem"], "url": f["url"], "motivo": f"{type(erro).__name__}: {erro}"[:200] + inicio})
            continue
        for i in itens:
            if not i["data"] or i["data"] < limite or not i["link"]:
                continue
            if not dominio_oficial(i["link"], oficiais):
                fora.append({"quem": f["quem"], **i})
                continue
            if normalizar(i["link"]) in citados:
                continue
            pautas.append({"quem": f["quem"], **i})
    if fontes.get("camara"):
        try:
            for t in tramitacoes(fontes["camara"], agora, busca):
                if t["data"] and t["data"] >= agora - timedelta(days=fontes["camara"]["dias"]):
                    pautas.append({"quem": "Câmara dos Deputados", **t})
        except Exception as erro:
            falhas.append({"quem": "Câmara dos Deputados", "url": "dadosabertos.camara.leg.br", "motivo": f"{type(erro).__name__}: {erro}"[:200]})
    pautas.sort(key=lambda p: p["data"], reverse=True)
    return {"agora": agora, "horas": horas, "pautas": pautas, "falhas": falhas, "fora_da_lista": fora,
            "visitar": fontes.get("pagina", []), "total_fontes": len(fontes["rss"]) + (1 if fontes.get("camara") else 0)}


def em_texto(r: dict) -> str:
    linhas = [f"Pautas das fontes oficiais nas últimas {r['horas']} horas (agora: {r['agora'].astimezone(BRASILIA):%d/%m/%Y %H:%M} de Brasília)", ""]
    if not r["pautas"]:
        linhas.append("Nenhum item novo nos feeds.")
    for p in r["pautas"]:
        linhas.append(f"- [{p['data'].astimezone(BRASILIA):%d/%m %H:%M}] {p['quem']}: {p['titulo']}\n  {p['link']}")
    linhas += ["", "Páginas sem feed, para visitar:"] + [f"- {p['quem']}: {p['url']}" for p in r["visitar"]]
    if r["fora_da_lista"]:
        linhas += ["", "Itens com link fora da lista de fontes oficiais (não usar):"]
        linhas += [f"- {p['quem']}: {p['link']}" for p in r["fora_da_lista"]]
    if r["falhas"]:
        linhas += ["", "Fontes que falharam:"] + [f"- {f['quem']} ({f['url']}): {f['motivo']}" for f in r["falhas"]]
    return "\n".join(linhas) + "\n"


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Pautas das fontes oficiais")
    p.add_argument("--horas", type=int, default=48)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    fontes = json.loads((RAIZ / "redacao" / "fontes.json").read_text(encoding="utf-8"))
    r = coletar(fontes, carregar_json("fontes_oficiais.json"), ja_citados(RAIZ / "materias"), datetime.now(timezone.utc), a.horas)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1, default=lambda d: d.isoformat()))
    else:
        print(em_texto(r))
    return 1 if len(r["falhas"]) == r["total_fontes"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
