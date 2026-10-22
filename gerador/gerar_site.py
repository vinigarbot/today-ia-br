"""Gera o site estático do today.ia.br a partir deste repositório (maquete v3, aprovada em 22/10/2026).

Uso:
  python -I gerador/gerar_site.py               _saida/ com as matérias aprovadas cujo horário de publicação já passou
  python -I gerador/gerar_site.py --rascunhos   prévia: inclui as ainda não aprovadas, mostra os espaços de anúncio, sem indexação
  python -I gerador/gerar_site.py --producao    como o primeiro, e para se faltar item do lançamento ou houver mudança fora de commit

Opções: --agora "AAAA-MM-DD HH:MM" (hora de Brasília fixa), --raiz PASTA (repositório com materias/ e o git),
--saida PASTA, --offline (não consulta a Câmara), --atualizar-radar (grava a consulta da Câmara em dados/radar.json).

Códigos de saída: 0 pronto; 1 alguma matéria não passa nas travas (nada é gerado); 2 falta item do lançamento (--producao).
O gerador não publica: quem envia _saida/ à hospedagem é o GitHub Actions (.github/workflows/publicar.yml).
"""

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # com python -I, a pasta do script não entra sozinha

from comum import (BRASILIA, CODIGO, EDITORIAS, agora_brasilia, carregar_json, carregar_materias, em_brasilia, inline,
                   ler_blocos, ler_cabecalho, ler_hora, minutos_leitura, tira_marcas, titulo_html, toca_investimento)
from desenho import assinatura, codigo_assinatura, mapa_atencao, tokens_titulo
from travas import dominio_oficial, relatorio, verificar_todas
from trilha import git, montar

TEMA = CODIGO / "tema"
AVISO_IA = "Produzida com IA e revisada antes da publicação."
AVISO_INVESTIMENTO = "Não é recomendação de investimento. Esta matéria informa sobre o mercado e não indica compra ou venda de ativos."
DESCRICAO_EDITORIA = {
    "ia": "Modelos, empresas, ferramentas e pesquisa em inteligência artificial, a partir das fontes oficiais.",
    "ia-cripto": "Onde a inteligência artificial cruza com cripto e bitcoin. Conteúdo informativo, sem recomendação de investimento.",
    "ia-bolsa": "Inteligência artificial no mercado de capitais: empresas, regras e uso. Sem recomendação de investimento.",
    "ia-games": "Inteligência artificial nos jogos: estúdios, ferramentas e o que muda para quem joga e para quem faz.",
    "ia-futebol": "Inteligência artificial no futebol: clubes, arbitragem, dados e saúde dos atletas.",
    "regulacao": "Leis, normas e decisões públicas sobre inteligência artificial, com o andamento do marco legal no Congresso.",
}
PAGINAS = {"como-usamos-ia": "Como usamos IA", "privacidade": "Política de privacidade"}

SCRIPT_DIA = """<script>(function(){try{var t=document.querySelector('.timeline');if(!t)return;var d=new Date(),z='America/Sao_Paulo';
var dia=new Intl.DateTimeFormat('en-CA',{timeZone:z,year:'numeric',month:'2-digit',day:'2-digit'}).format(d),n=t.querySelector('.now'),p=t.querySelector('.past');
if(t.hasAttribute('data-fixo'))return;if(t.getAttribute('data-dia')!==dia){if(n)n.hidden=true;if(p)p.style.width='100%';return}
var h=new Intl.DateTimeFormat('pt-BR',{timeZone:z,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(d),q=h.split(':'),pc=((+q[0]*60+(+q[1]))/14.4).toFixed(2)+'%';
if(n){n.style.left=pc;n.querySelector('span').textContent='AGORA '+h}if(p)p.style.width=pc}catch(e){}})();</script>"""


def esc(texto: str) -> str:
    return html.escape(texto or "", quote=True)


def versao_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()[:10]


def dia_ponto(d: datetime) -> str:
    return d.strftime("%d.%m.%Y")


# ---------------------------------------------------------------- anúncios

def anuncio(ctx: dict, chave: str, classe: str, rotulo: str, codigo: str, extra: str = "") -> str:
    """Prévia: o espaço marcado como na maquete. Produção: o bloco do AdSense, só quando o bloco estiver configurado."""
    if ctx["previa"]:
        return f'<div class="ad {classe}" data-ad="{codigo}"{extra}>{rotulo}</div>'
    cliente, bloco = ctx["cfg"]["adsense"]["cliente"], ctx["cfg"]["adsense"]["blocos"].get(chave, "")
    if not (cliente and bloco):
        return ""
    formato = 'data-ad-format="autorelaxed"' if chave == "patrocinado" else 'data-ad-format="auto" data-full-width-responsive="true"'
    return (f'<div class="ad-slot {classe}"{extra}><ins class="adsbygoogle" style="display:block" data-ad-client="{esc(cliente)}" '
            f'data-ad-slot="{esc(bloco)}" {formato}></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')


def patrocinados(ctx: dict, codigo: str) -> str:
    if ctx["previa"]:
        miolo = f'<div class="mx" data-ad="{codigo}">' + '<div class="ad">Patrocinado</div>' * 4 + "</div>"
    else:
        miolo = anuncio(ctx, "patrocinado", "mx-slot", "", codigo)
    if not miolo:
        return ""
    return f'<section class="multiplex"><div class="wrap"><div class="label"><b>//</b> Conteúdo patrocinado</div>{miolo}</div></section>'


# ---------------------------------------------------------------- moldura

def pagina(ctx: dict, *, caminho: str, titulo: str, descricao: str, corpo: str, ativa: str = "",
           jsonld: dict | None = None, tipo_og: str = "website", ancora: str = "") -> str:
    cfg, base = ctx["cfg"], ctx["cfg"]["url"].rstrip("/")
    titulo_doc = cfg["nome"] if titulo == cfg["nome"] else f"{titulo} · {cfg['nome']}"
    marca = lambda chave: ' class="on"' if ativa == chave else ""
    menu = [f'<a{marca("hoje")} href="/">Hoje</a>']
    menu += [f'<a{marca(k)} href="/{k}/">{EDITORIAS[k]["menu"]}</a>' for k in ctx["editorias_no_ar"]]
    ferramentas = '<a class="btn-ghost" href="/como-usamos-ia/">Como usamos IA</a>' if "como-usamos-ia" in ctx["paginas"] else ""
    rodape_links = []
    if "privacidade" in ctx["paginas"]:
        rodape_links.append('<a href="/privacidade/">Privacidade</a>')
    if cfg["email_redacao"]:
        rodape_links.append(f'<a href="mailto:{esc(cfg["email_redacao"])}">Relatar erro</a>')
    ld = ""
    if jsonld:  # "<" escapado: texto da matéria nunca abre nem fecha tag dentro do <script>
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
    adsense = ""
    if not ctx["previa"] and cfg["adsense"]["cliente"]:
        adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(cfg["adsense"]["cliente"])}" '
                   'crossorigin="anonymous"></script>')
    analise = ""
    if not ctx["previa"] and cfg.get("cloudflare_analytics_token"):
        analise = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                   f"data-cf-beacon='{{\"token\": \"{esc(cfg['cloudflare_analytics_token'])}\"}}'></script>")
    previa = '<span class="mock">Prévia · não publicada</span>' if ctx["previa"] else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo_doc)}</title>
<meta name="description" content="{esc(descricao)}">
{'<meta name="robots" content="noindex">' if ctx["previa"] else ""}
<meta name="versao" content="{ctx["versao"][:12]}">
<link rel="canonical" href="{base}{caminho}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{esc(cfg["nome"])}" href="/feed.xml">
<meta property="og:site_name" content="{esc(cfg["nome"])}">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="{tipo_og}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{base}{caminho}">
<link rel="preload" href="/assets/fontes/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/estilo.css?v={ctx["versao_css"]}">
{ld}
{adsense}
</head>
<body>
<header class="head">
  <div class="wrap">
    <a class="logo" href="/" aria-label="today.ia.br, página inicial">today<span class="cur"></span><span class="tld">.ia<em>.br</em></span></a>
    <nav class="nav">{"".join(menu)}</nav>
    <div class="tools">{ferramentas}</div>
  </div>
</header>
{corpo}
<footer class="wrap legal">
  <span>© {ctx["agora"].year} today.ia.br · Produzido com IA e revisado antes da publicação</span>
  <span>Conteúdo informativo, sem recomendação de investimento{"".join(" · " + l for l in rodape_links)}</span>
</footer>
{ancora}
{previa}
{SCRIPT_DIA if ativa == "hoje" else ""}
{analise}
</body>
</html>
"""


# ---------------------------------------------------------------- peças

def tag(m: dict) -> str:
    ed = EDITORIAS[m["editoria"]]
    if ed["cruza"]:
        return f'<span class="tag cross">{esc(m["editoria"].replace("-", "×"))}</span>'
    return f'<span class="tag">{esc(m["editoria"])}/{esc(m["assunto"])}</span>'


def medidor(m: dict, longo: bool = False) -> str:
    """Cinco barras = cinco etapas da trilha (coleta, rascunho, checagem, revisão, aprovação); a última acende com o merge."""
    etapas = 5 if m["trilha"]["aprovada_em"] else 4
    barras = "<i></i>" * etapas + '<i class="off"></i>' * (5 - etapas)
    fontes = len(m["fontes"])
    texto = f"{fontes} {'fonte' if fontes == 1 else 'fontes'}"
    if longo:
        texto = f"trilha {etapas}/5 · {fontes} {'fonte oficial' if fontes == 1 else 'fontes oficiais'}"
    return f'<span class="meter">{barras}<em>{texto}</em></span>'


def quando_curto(m: dict, agora: datetime) -> str:
    dia = m["publicar_em"].date()
    if dia == agora.date():
        return "hoje"
    if dia == (agora - timedelta(days=1)).date():
        return "ontem"
    return m["publicar_em"].strftime("%d.%m")


def cartao(m: dict, ctx: dict, span: int) -> str:
    grande = span >= 6
    fina = f'<p>{esc(m["linha_fina"])}</p>' if grande else ""
    estilo = f'style="--span:{span}"'
    if m["publicar_em"] > ctx["agora"]:
        sai = m["publicar_em"].strftime("%H:%M")
        t = m["trilha"]
        situacao = f'Revisada {t["revisada_em"].strftime("%H:%M")} · sai às {sai}' if t["aprovada_em"] else f"Aguardando aprovação · sai às {sai}"
        return (f'<div class="card sched{" big" if grande else ""}" {estilo}><div class="top">{tag(m)}'
                f'<span class="idx">hoje · {sai} · agendada</span></div><h3>{esc(m["titulo_puro"])}</h3>{fina}'
                f'<div class="foot"><span class="chip">{situacao}</span></div></div>')
    return (f'<a class="card{" big" if grande else ""}" {estilo} href="/{m["slug"]}/"><div class="top">{tag(m)}'
            f'<span class="idx">{quando_curto(m, ctx["agora"])}</span></div><h3>{esc(m["titulo_puro"])}</h3>{fina}'
            f'<div class="foot">{medidor(m)}<span class="chip">{minutos_leitura(m)} min</span>'
            f'<span class="glyph">{assinatura(m["slug"])}</span></div></a>')


def grade(itens: list[tuple[str, object]], ctx: dict) -> str:
    """Cartões em 12 colunas, no ritmo da maquete (8+4, depois 4+4+4 e 6+6); a última linha estica para não sobrar buraco."""
    ritmo = [8, 4] + [4, 4, 4, 6, 6] * 20
    larguras = ritmo[:len(itens)]
    sobra = sum(larguras) % 12
    if sobra and larguras:
        larguras[-1] += 12 - sobra
    partes = []
    for (tipo, valor), span in zip(itens, larguras):
        if tipo == "anuncio":
            partes.append(valor(span))
        else:
            partes.append(cartao(valor, ctx, span))
    return f'<div class="cards">{"".join(partes)}</div>' if partes else ""


def anuncio_feed(ctx: dict):
    def montar(span: int) -> str:
        return anuncio(ctx, "feed", "infeed card", "Anúncio no feed · nativo", "A2", f' style="--span:{span}"')
    return montar if anuncio(ctx, "feed", "infeed card", "", "A2") else None


def linha_do_dia(ctx: dict, do_dia: list[dict]) -> str:
    agora = ctx["agora"]
    minutos = agora.hour * 60 + agora.minute
    pc = lambda mins: f"{mins / 14.4:.2f}%"
    horas = "".join(f'<div class="hr" style="left:{h / 24 * 100:g}%"><span>{h:02d}h</span></div>' for h in range(0, 24, 3))
    pinos = []
    for n, m in enumerate(sorted(do_dia, key=lambda x: x["publicar_em"]), start=1):
        p = m["publicar_em"]
        classes = "pin" + (" sched" if p > agora else "") + (" cross" if EDITORIAS[m["editoria"]]["cruza"] else "")
        rotulo = m["editoria"].replace("-", "×") if EDITORIAS[m["editoria"]]["cruza"] else m["assunto"] or m["editoria"]
        pinos.append(f'<div class="{classes}" style="left:{pc(p.hour * 60 + p.minute)}"><i></i>'
                     f'<span>{p.strftime("%H:%M")}<br><em>{n:02d} · {esc(rotulo)}</em></span></div>')
    qtd = len(do_dia)
    rotulo = f"{qtd} {'matéria' if qtd == 1 else 'matérias'}" if qtd else "nenhuma matéria ainda"
    return (f'<section class="day"><div class="wrap"><div class="label"><b>//</b> Linha do dia · {agora.strftime("%d.%m")} · {rotulo}</div>'
            f'<div class="timeline" data-dia="{agora.strftime("%Y-%m-%d")}"{" data-fixo" if ctx["hora_fixa"] else ""}><div class="past" style="width:{pc(minutos)}"></div>{horas}'
            f'{"".join(pinos)}<div class="now" style="left:{pc(minutos)}"><span>AGORA {agora.strftime("%H:%M")}</span></div></div></div></section>')


def radar_html(radar: dict | None, cfg: dict) -> str:
    if not radar:
        return ""
    st = radar["status"]
    situacao = st.get("descricaoSituacao") or ""
    if "Transformad" in situacao or "Norma Jurídica" in situacao:
        etapa = 5
    elif "Sanção" in situacao:
        etapa = 4
    elif "Pronta para Pauta" in situacao:
        etapa = 3
    else:
        etapa = 2
    chegou = datetime.fromisoformat(radar["apresentacao"]).strftime("%d/%m/%Y")
    ultima = datetime.fromisoformat(st["dataHora"]).strftime("%d/%m/%Y")
    consulta = datetime.fromisoformat(radar["consultado_em"]).astimezone(BRASILIA).strftime("%d/%m/%Y %H:%M")
    passos = [("Senado", f"Aprovado e enviado à Câmara em {chegou}"), ("Câmara", situacao or "Em análise"),
              ("Plenário", "Votação na Câmara"), ("Sanção", "Presidência da República")]
    blocos = []
    for i, (nome, texto) in enumerate(passos, start=1):
        classe = "done" if i < etapa else "cur" if i == etapa else ""
        numero = f"{i:02d} · agora" if i == etapa else f"{i:02d}"
        blocos.append(f'<div class="step {classe}"><span class="bar"></span><span class="n">{numero}</span>'
                      f'<h4>{nome}</h4><p>{esc(texto)}</p></div>')
    return (f'<section class="reg"><div class="wrap"><div class="label"><b>//</b> Radar regulatório · dados abertos da Câmara</div>'
            f'<div class="box"><div class="left"><span class="tag">regulacao/pl-2338-2023</span><h3>Marco legal da inteligência artificial</h3>'
            f'<p>Andamento acompanhado automaticamente. Última movimentação registrada pela Câmara em {ultima}: '
            f'{esc(st.get("descricaoTramitacao") or "")}.</p>'
            f'<p class="fonte">Consulta em {consulta} · <a href="{esc(cfg["pl_2338"]["pagina"])}" rel="noopener">ver na Câmara</a></p></div>'
            f'<div class="steps">{"".join(blocos)}</div></div></div></section>')


COMO_E_FEITO = """<section class="how"><div class="wrap"><div class="label"><b>//</b> Do comunicado oficial à sua tela</div><div class="pipe">
<div><span class="n">01</span><h4>Coleta</h4><p>Somente fontes oficiais: empresas de IA, órgãos públicos e dados abertos.</p></div>
<div><span class="n">02</span><h4>Redação por IA</h4><p>O texto é escrito a partir da fonte original, sem copiar outros veículos.</p></div>
<div><span class="n">03</span><h4>Checagem</h4><p>Cada afirmação precisa de link. Sem fonte, a matéria não entra na fila.</p></div>
<div><span class="n">04</span><h4>Revisão humana</h4><p>Toda matéria é lida e aprovada por uma pessoa antes de ir ao ar.</p></div>
<div><span class="n">05</span><h4>Publicação</h4><p>Uma ou duas matérias por dia, com a trilha completa visível ao leitor.</p></div>
</div></div></section>"""


# ---------------------------------------------------------------- páginas

def inicial(ctx: dict, publicadas: list[dict], agendadas: list[dict]) -> str:
    agora = ctx["agora"]
    partes = [f'<div class="wrap">{anuncio(ctx, "topo", "billboard", "Topo · 970 × 250", "A1")}</div>', "<main>"]
    destaque = publicadas[0] if publicadas else None
    if destaque:
        m, t = destaque, destaque["trilha"]
        fontes = len(m["fontes"])
        trechos = sum(1 for b in m["blocos"] if b["tipo"] in ("p", "lista", "dados"))
        quando = m["publicar_em"].strftime("%H:%M") if m["publicar_em"].date() == agora.date() else dia_ponto(m["publicar_em"])
        partes.append(f"""<section class="hero"><div class="wrap grid"><div>
{tag(m)}
<h1><a href="/{m["slug"]}/">{titulo_html(m["titulo"])}</a></h1>
<p class="dek">{esc(m["linha_fina"])}</p>
<div class="meta-row">{medidor(m, longo=True)}
<span class="chip">{minutos_leitura(m)} min de leitura</span><span class="chip">Publicada {quando}</span></div>
</div>
<aside class="attn"><span class="corner tl"></span><span class="corner br"></span>
<header><span>Mapa de atenção · título</span><b>● ao vivo</b></header>
<div class="viz">{mapa_atencao(tokens_titulo(m["titulo_puro"]))}</div>
<footer><div>Fontes<b>{fontes} {"oficial" if fontes == 1 else "oficiais"}</b></div><div>Trechos com fonte<b>{trechos}/{trechos}</b></div><div>Ajustes humanos<b>{t["ajustes"]}</b></div></footer>
</aside></div></section>""")
    hoje = [m for m in publicadas + agendadas if m["publicar_em"].date() == agora.date()]
    partes.append(linha_do_dia(ctx, hoje))
    itens = [("materia", m) for m in agendadas] + [("materia", m) for m in publicadas[1:13]]
    feed = anuncio_feed(ctx)
    if feed and itens:
        itens.insert(1, ("anuncio", feed))
    if itens:
        partes.append(f'<section class="feed"><div class="wrap"><div class="label"><b>//</b> Hoje e nos últimos dias</div>{grade(itens, ctx)}</div></section>')
    elif not destaque:
        partes.append('<section class="feed"><div class="wrap"><p class="vazio">Nenhuma matéria publicada ainda.</p></div></section>')
    meio = anuncio(ctx, "meio", "wide", "Meio da página · 970 × 90", "A3")
    if meio:
        partes.append(f'<div class="wrap">{meio}</div>')
    partes += [radar_html(ctx["radar"], ctx["cfg"]), patrocinados(ctx, "A4"), COMO_E_FEITO, "</main>"]
    ancora = anuncio(ctx, "ancora", "anchor", "Âncora celular · 320 × 50", "A5") if ctx["previa"] else ""
    return pagina(ctx, caminho="/", titulo=ctx["cfg"]["nome"], descricao=ctx["cfg"]["descricao"], corpo="\n".join(partes),
                  ativa="hoje", ancora=ancora, jsonld={"@context": "https://schema.org", "@type": "WebSite",
                                                        "name": ctx["cfg"]["nome"], "url": ctx["cfg"]["url"].rstrip("/") + "/"})


def corpo_materia(m: dict, ctx: dict) -> str:
    blocos = m["blocos"]
    paragrafos = [i for i, b in enumerate(blocos) if b["tipo"] == "p"]
    # anúncios no texto (Better Ads: densidade no celular abaixo de 30%): o 1º depois do 2º parágrafo, só com 4 ou mais;
    # o 2º perto dos dois terços, só com 8 ou mais
    pos_b2 = paragrafos[1] if len(paragrafos) >= 4 else None
    pos_b3 = paragrafos[max(3, (2 * len(paragrafos)) // 3)] if len(paragrafos) >= 8 else None
    pos_destaque = pos_b2 if pos_b2 is not None else (paragrafos[1] if len(paragrafos) >= 2 else None)
    destaque_refs = ""
    if m["destaque"]:
        for b in blocos:
            if tira_marcas(m["destaque"]).lower() in tira_marcas(b["texto"]).lower():
                destaque_refs = " ".join(f"[{n}]" for n in dict.fromkeys(re.findall(r"\[(\d+)\]", b["texto"])))
                break
    avisos = f'<div class="aviso">{AVISO_IA}</div>'  # div, não p: a capitular fica no primeiro parágrafo do texto
    if m["investimento"]:
        avisos += f'<div class="notice">{AVISO_INVESTIMENTO}</div>'
    saida = [avisos]
    for i, b in enumerate(blocos):
        if b["tipo"] == "h2":
            saida.append(f"<h2>{inline(b['texto'])}</h2>")
        elif b["tipo"] == "p":
            saida.append(f"<p>{inline(b['texto'])}</p>")
        elif b["tipo"] == "lista":
            saida.append('<ul class="lista">' + "".join(f"<li>{inline(x)}</li>" for x in b["itens"]) + "</ul>")
        elif b["tipo"] == "dados":
            titulo = re.sub(r"\s*\[\d+\]", "", b["texto"])
            refs = inline(" ".join(f"[{n}]" for n in re.findall(r"\[(\d+)\]", b["texto"])))
            maior = max(float(l["valor"].replace(",", ".")) for l in b["linhas"]) or 1
            linhas = "".join(
                f'<div class="row{" alt" if k % 2 else ""}"><span>{esc(l["rotulo"])}</span><span class="b"><i style="width:{float(l["valor"].replace(",", ".")) / maior * 100:.0f}%"></i></span><span>{esc(l["valor"])}</span></div>'
                for k, l in enumerate(b["linhas"]))
            saida.append(f'<div class="data"><header><span>{esc(titulo)}</span><span>{refs}</span></header><div class="rows">{linhas}</div></div>')
        if i == pos_b2:
            saida.append(anuncio(ctx, "texto", "inart", "No texto · 336 × 280", "B2"))
        if i == pos_destaque and m["destaque"]:
            saida.append(f'<div class="pull">{esc(tira_marcas(m["destaque"]))}<cite>— Desta matéria · fontes {esc(destaque_refs)}</cite></div>')
        if i == pos_b3:
            saida.append(anuncio(ctx, "texto", "inart", "No texto · 336 × 280", "B3"))
    if ctx["cfg"]["email_redacao"]:
        assunto = f"Erro na matéria {m['slug']}"
        saida.append(f'<div class="report"><span>Encontrou um erro nesta matéria?</span>'
                     f'<a href="mailto:{esc(ctx["cfg"]["email_redacao"])}?subject={esc(assunto.replace(" ", "%20"))}">Relatar erro</a></div>')
    return "\n".join(saida)


def materia(m: dict, ctx: dict) -> str:
    t, agora, cfg = m["trilha"], ctx["agora"], ctx["cfg"]
    ed = EDITORIAS[m["editoria"]]
    caminho = [ed["nome"]] + ([m["assunto"].replace("-", " ").capitalize()] if m["assunto"] else []) + [dia_ponto(m["publicar_em"])]
    crumb = '<b>//</b>' + '<span>/</span>'.join(f"<span>{esc(c)}</span>" for c in caminho)
    chips = ['<span class="chip">Redação today.ia.br</span>', '<span class="chip">Produzida com IA</span>']
    if t["revisada_em"]:
        chips.append(f'<span class="chip">Revisada por humano {t["revisada_em"].strftime("%H:%M")}</span>')
    publicada = m["publicar_em"] <= agora
    chips.append(f'<span class="chip">{"Publicada" if publicada else "Agendada para"} {dia_ponto(m["publicar_em"])} {m["publicar_em"].strftime("%H:%M")}</span>')
    chips.append(f'<span class="chip">{minutos_leitura(m)} min de leitura</span>')
    etapas = list(t["etapas"])
    if publicada and t["aprovada_em"]:
        etapas.append({"nome": "Publicada", "hora": m["publicar_em"].strftime("%H:%M"), "nota": "", "humana": False})
    linhas = []
    for e in etapas:
        classe = ' class="hum"' if e["humana"] else ""
        nota = f"<small>{esc(e['nota'])}</small>" if e["nota"] else ""
        linhas.append(f'<li{classe}><time>{esc(e["hora"])}</time><i></i><span>{esc(e["nome"])}{nota}</span></li>')
    trilha = "".join(linhas)
    diff = ""
    if t["diff"]:  # o primeiro ajuste humano, como na maquete: o trecho tirado riscado e o posto em verde
        tirado, posto = t["diff"]
        diff = ('<div class="diff">' + (f'<span class="del">{esc(tirado)}</span>' if tirado else "")
                + (f'<span class="add">{esc(posto)}</span>' if posto else "") + "</div>")
    if t["sem_historico"]:
        trilha, diff = '<li><time>—</time><i></i><span>Sem histórico no git</span></li>', ""
    consultada = m["coletada_em"].strftime("%H:%M") if m["coletada_em"] else "—"
    fontes = "".join(f'<li id="f{f["n"]}"><span><a href="{esc(f["url"])}" rel="noopener">{esc(f["titulo"])}</a>'
                     f'<small>{esc(f["quem"])} · consultada {consultada}</small></span></li>' for f in m["fontes"])
    qtd = len(m["fontes"])
    corpo = f"""<div class="wrap">{anuncio(ctx, "topo", "billboard", "Topo · 970 × 250", "B1")}</div>
<main>
  <section class="art-head"><div class="wrap">
    <div class="crumb">{crumb}</div>
    <h1>{titulo_html(m["titulo"])}</h1>
    <p class="dek">{esc(m["linha_fina"])}</p>
    <div class="byline">{"".join(chips)}</div>
  </div></section>
  <div class="wrap art">
    <aside class="side l"><div class="stick"><div class="panel">
      <header><span>Trilha da matéria</span><b>{len(etapas)} etapas</b></header>
      <ol class="trail">{trilha}</ol>{diff}
    </div></div></aside>
    <article class="body">
{corpo_materia(m, ctx)}
    </article>
    <aside class="side r"><div class="stick">
      <div class="panel"><div class="idcard"><span class="glyph-g">{assinatura(m["slug"])}</span><span>Assinatura<br><b>{codigo_assinatura(m["slug"])}</b><br>única por matéria</span></div></div>
      <div class="panel"><header><span>Fontes</span><b>{qtd} {"oficial" if qtd == 1 else "oficiais"}</b></header><ol class="sources">{fontes}</ol></div>
      {anuncio(ctx, "lateral", "side", "Lateral fixa · 300 × 600", "B4")}
    </div></aside>
  </div>
  {patrocinados(ctx, "B5")}
</main>"""
    base = cfg["url"].rstrip("/")
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": m["titulo_puro"][:110],
          "description": m["linha_fina"], "datePublished": m["publicar_em"].isoformat(),
          "dateModified": max(t["ultima_mudanca"] or m["publicar_em"], m["publicar_em"]).isoformat(), "inLanguage": "pt-BR",
          "mainEntityOfPage": f"{base}/{m['slug']}/", "articleSection": ed["nome"],
          "author": {"@type": "Organization", "name": "Redação today.ia.br", "url": base + "/"},
          "publisher": {"@type": "Organization", "name": cfg["nome"], "url": base + "/"}}
    ancora = anuncio(ctx, "ancora", "anchor", "Âncora celular · 320 × 50", "B6") if ctx["previa"] else ""
    return pagina(ctx, caminho=f"/{m['slug']}/", titulo=m["titulo_puro"], descricao=m["linha_fina"], corpo=corpo,
                  ativa=m["editoria"], jsonld=ld, tipo_og="article", ancora=ancora)


def pagina_editoria(chave: str, lista: list[dict], ctx: dict) -> str:
    ed = EDITORIAS[chave]
    itens = [("materia", m) for m in lista]
    corpo = (f'<main><section class="art-head"><div class="wrap"><div class="crumb"><b>//</b><span>Editoria</span></div>'
             f'<h1>{esc(ed["nome"])}</h1><p class="dek">{esc(DESCRICAO_EDITORIA[chave])}</p></div></section>'
             f'<section class="feed"><div class="wrap">{grade(itens, ctx) or "<p class=vazio>Nenhuma matéria publicada ainda.</p>"}</div></section>'
             f'{radar_html(ctx["radar"], ctx["cfg"]) if chave == "regulacao" else ""}</main>')
    return pagina(ctx, caminho=f"/{chave}/", titulo=ed["nome"], descricao=DESCRICAO_EDITORIA[chave], corpo=corpo, ativa=chave)


def pagina_texto(nome: str, arq: Path, ctx: dict) -> str:
    lido = ler_cabecalho(arq.read_text(encoding="utf-8").replace("\r\n", "\n"))
    meta, texto = lido if lido else ({}, arq.read_text(encoding="utf-8"))
    partes = []
    for b in ler_blocos(texto):
        if b["tipo"] == "h2":
            partes.append(f"<h2>{inline(b['texto'])}</h2>")
        elif b["tipo"] == "lista":
            partes.append('<ul class="lista">' + "".join(f"<li>{inline(x)}</li>" for x in b["itens"]) + "</ul>")
        else:
            partes.append(f"<p>{inline(b['texto'])}</p>")
    titulo = meta.get("titulo", PAGINAS[nome])
    corpo = (f'<main><section class="art-head"><div class="wrap"><div class="crumb"><b>//</b><span>{esc(ctx["cfg"]["nome"])}</span></div>'
             f'<h1>{esc(titulo)}</h1></div></section><div class="wrap texto"><article class="body">{"".join(partes)}</article></div></main>')
    return pagina(ctx, caminho=f"/{nome}/", titulo=titulo, descricao=meta.get("descricao", titulo), corpo=corpo)


def pagina_404(ctx: dict) -> str:
    corpo = ('<main><section class="art-head"><div class="wrap"><div class="crumb"><b>//</b><span>404</span></div>'
             '<h1>Página não encontrada</h1><p class="dek">O endereço pode ter mudado ou a matéria ainda não foi publicada.</p>'
             '<p class="dek"><a class="btn-ghost" href="/">Ir para a página inicial</a></p></div></section></main>')
    return pagina(ctx, caminho="/404.html", titulo="Página não encontrada", descricao="Página não encontrada", corpo=corpo)


# ---------------------------------------------------------------- arquivos do site

def rss(publicadas: list[dict], cfg: dict) -> str:
    base = cfg["url"].rstrip("/")
    itens = "".join(
        f"<item><title>{esc(m['titulo_puro'])}</title><link>{base}/{m['slug']}/</link><guid>{base}/{m['slug']}/</guid>"
        f"<pubDate>{m['publicar_em'].strftime('%a, %d %b %Y %H:%M:%S -0300')}</pubDate><description>{esc(m['linha_fina'])}</description></item>"
        for m in publicadas[:20])
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(cfg["nome"])}</title><link>{base}/</link>'
            f"<description>{esc(cfg['descricao'])}</description><language>pt-BR</language>{itens}</channel></rss>\n")


def sitemap(enderecos: list[tuple[str, datetime | None]], cfg: dict) -> str:
    base = cfg["url"].rstrip("/")
    urls = "".join(f"<url><loc>{base}{e}</loc>" + (f"<lastmod>{q.strftime('%Y-%m-%d')}</lastmod>" if q else "") + "</url>"
                   for e, q in enderecos)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#05070a"/>'
           '<rect x="11" y="6" width="10" height="20" fill="#c6ff3a"/></svg>\n')
CABECALHOS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
/assets/*
  Cache-Control: public, max-age=604800
"""


def escrever(saida: Path, caminho: str, conteudo: str) -> None:
    """Caminho terminado em "/" vira página (pasta/index.html); o resto é arquivo com o nome dado (_headers, feed.xml)."""
    destino = saida / caminho.strip("/") / "index.html" if caminho.endswith("/") else saida / caminho.strip("/")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- radar (dados abertos da Câmara)

def consultar_radar(cfg: dict) -> dict:
    base = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{cfg['pl_2338']['id_camara']}"
    pedido = urllib.request.Request(base, headers={"Accept": "application/json", "User-Agent": "today.ia.br (gerador do site)"})
    with urllib.request.urlopen(pedido, timeout=20) as r:
        dados = json.loads(r.read().decode("utf-8"))["dados"]
    return {"consultado_em": datetime.now(BRASILIA).isoformat(timespec="minutes"), "apresentacao": dados["dataApresentacao"],
            "status": {k: dados["statusProposicao"].get(k) for k in ("dataHora", "siglaOrgao", "descricaoTramitacao", "descricaoSituacao")}}


def carregar_radar(raiz: Path, cfg: dict, offline: bool, atualizar: bool) -> dict | None:
    """Consulta a Câmara; se falhar (ou com --offline), usa a última consulta guardada em dados/radar.json."""
    guardado = raiz / "dados" / "radar.json"
    if not offline:
        try:
            radar = consultar_radar(cfg)
            if atualizar:
                guardado.parent.mkdir(exist_ok=True)
                guardado.write_text(json.dumps(radar, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
            return radar
        except Exception as erro:  # rede, formato ou API fora do ar: o site sai com a última consulta guardada
            print(f"Aviso: consulta à Câmara falhou ({erro}); usando dados/radar.json")
    return json.loads(guardado.read_text(encoding="utf-8")) if guardado.exists() else None


# ---------------------------------------------------------------- montagem

def pendencias_lancamento(raiz: Path, cfg: dict, publicadas: list[dict], paginas: dict) -> list[str]:
    falta = []
    if not publicadas:
        falta.append("Nenhuma matéria aprovada com horário de publicação já passado")
    for nome, titulo in PAGINAS.items():
        if nome not in paginas:
            falta.append(f"Página '{titulo}' (paginas/{nome}.md)")
    if not cfg["email_redacao"]:
        falta.append("E-mail da redação em gerador/config.json (para 'Relatar erro' e para a política de privacidade)")
    return falta


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Gera o site do today.ia.br")
    p.add_argument("--rascunhos", action="store_true")
    p.add_argument("--producao", action="store_true")
    p.add_argument("--agora")
    p.add_argument("--raiz")
    p.add_argument("--saida")
    p.add_argument("--offline", action="store_true")
    p.add_argument("--atualizar-radar", action="store_true")
    a = p.parse_args(argv)
    if a.rascunhos and a.producao:
        p.error("--rascunhos e --producao não andam juntos")
    raiz = Path(a.raiz).resolve() if a.raiz else CODIGO
    saida = Path(a.saida).resolve() if a.saida else raiz / "_saida"
    agora = ler_hora(a.agora) if a.agora else agora_brasilia().replace(second=0, microsecond=0)
    if agora is None:
        p.error("--agora fora do formato AAAA-MM-DD HH:MM")
    cfg, oficiais = carregar_json("config.json"), carregar_json("fontes_oficiais.json")

    sujo = git(raiz, "status", "--porcelain")
    if a.producao and sujo is None:
        print("Produção exige o repositório git com o histórico completo (a trilha e a aprovação saem dele).")
        return 2
    if a.producao and sujo.strip():
        print("Produção só sai de árvore limpa: há mudança fora de commit.\n" + sujo)
        return 2

    materias = carregar_materias(raiz / "materias")
    resultado = verificar_todas(materias, cfg, oficiais)
    com_erro = {k: v for k, v in resultado.items() if v[0]}
    if com_erro:
        print("Nada foi gerado: há matéria que não passa nas travas.\n\n" + relatorio(com_erro))
        return 1
    for m in materias:
        m["trilha"] = montar(raiz, m)
        m["investimento"] = toca_investimento(m, cfg["termos_investimento"])
        for f in m["fontes"]:
            f["quem"] = dominio_oficial(f["url"], oficiais)
    fora = [] if a.rascunhos else [m for m in materias if not m["trilha"]["aprovada"]]
    candidatas = [m for m in materias if m not in fora]
    publicadas = [m for m in candidatas if m["publicar_em"] <= agora]
    agendadas = [m for m in candidatas if m["publicar_em"] > agora and m["publicar_em"].date() == agora.date()]
    com_pagina = candidatas if a.rascunhos else publicadas
    paginas = {n: raiz / "paginas" / f"{n}.md" for n in PAGINAS if (raiz / "paginas" / f"{n}.md").exists()}

    ctx = {"cfg": cfg, "agora": agora, "previa": a.rascunhos, "paginas": paginas, "hora_fixa": bool(a.agora),
           "radar": carregar_radar(raiz, cfg, a.offline, a.atualizar_radar),
           "versao": (git(raiz, "rev-parse", "HEAD") or "sem-git").strip(),
           "versao_css": versao_arquivo(TEMA / "estilo.css"),
           "editorias_no_ar": [k for k in EDITORIAS if any(m["editoria"] == k for m in com_pagina)]}

    if saida.exists():
        shutil.rmtree(saida)
    (saida / "assets" / "fontes").mkdir(parents=True)
    shutil.copy(TEMA / "estilo.css", saida / "assets" / "estilo.css")
    for f in (TEMA / "fontes").iterdir():
        shutil.copy(f, saida / "assets" / "fontes" / f.name)
    (saida / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8", newline="\n")

    escrever(saida, "/", inicial(ctx, publicadas, agendadas))
    for m in com_pagina:
        escrever(saida, f"/{m['slug']}/", materia(m, ctx))
    for chave in ctx["editorias_no_ar"]:
        escrever(saida, f"/{chave}/", pagina_editoria(chave, [m for m in publicadas if m["editoria"] == chave], ctx))
    for nome, arq in paginas.items():
        escrever(saida, f"/{nome}/", pagina_texto(nome, arq, ctx))
    escrever(saida, "/404.html", pagina_404(ctx))
    enderecos = [("/", None)] + [(f"/{k}/", None) for k in ctx["editorias_no_ar"]] + \
                [(f"/{m['slug']}/", m["publicar_em"]) for m in publicadas] + [(f"/{n}/", None) for n in paginas]
    escrever(saida, "/sitemap.xml", sitemap(enderecos, cfg))
    escrever(saida, "/feed.xml", rss(publicadas, cfg))
    escrever(saida, "/robots.txt", "User-agent: *\nDisallow: /\n" if a.rascunhos else f"User-agent: *\nAllow: /\nSitemap: {cfg['url'].rstrip('/')}/sitemap.xml\n")
    escrever(saida, "/_headers", CABECALHOS + ("/*\n  X-Robots-Tag: noindex\n" if a.rascunhos else ""))
    if cfg["adsense"]["cliente"] and not a.rascunhos:
        escrever(saida, "/ads.txt", f"google.com, {cfg['adsense']['cliente'].replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    if ctx["radar"]:
        escrever(saida, "/dados/radar.json", json.dumps(ctx["radar"], ensure_ascii=False, indent=1) + "\n")
    escrever(saida, "/versao.txt", f"{ctx['versao']}\ngerado em {agora.strftime('%Y-%m-%d %H:%M')} (Brasília)"
                                    f"{' · prévia' if a.rascunhos else ''}\n")

    print(f"Site gerado em {saida} ({'prévia' if a.rascunhos else 'produção' if a.producao else 'conferência'}, "
          f"agora = {agora.strftime('%d/%m/%Y %H:%M')} de Brasília)")
    print(f"- {len(publicadas)} publicada(s), {len(agendadas)} agendada(s) para hoje, {len(materias) - len(candidatas)} fora por falta de aprovação")
    for m in fora:
        print(f"  fora (sem aprovação na versão atual): {m['arquivo'].name}")
    alertas = {k: v for k, v in resultado.items() if v[1]}
    if alertas:
        print("\nAlertas das travas (não impedem):\n" + relatorio(alertas))
    falta = pendencias_lancamento(raiz, cfg, publicadas, paginas)
    if falta:
        print("\nFalta para o lançamento:\n" + "\n".join(f"- {f}" for f in falta))
        if a.producao:
            return 2
    else:
        print("\nPronto para publicar.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
