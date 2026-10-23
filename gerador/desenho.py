"""Desenhos gerados por matéria (maquete v3), feitos no gerador para a página não depender de script.

Mesmos cálculos do maquete/app.js (FNV-1a de 32 bits e xorshift), para o desenho sair igual ao da maquete.
"""

import html
import re

VERDE, CIANO, CINZA = "#c6ff3a", "#6be4ff", "#6f7b87"


def _i32(x: int) -> int:
    x &= 0xFFFFFFFF
    return x - 0x100000000 if x & 0x80000000 else x


def hash32(texto: str) -> int:
    h = 2166136261
    for c in texto:
        h = _i32(_i32(h) ^ ord(c))
        h = _i32((h & 0xFFFFFFFF) * 16777619)
    return h & 0xFFFFFFFF


def sorteio(semente: int):
    s = semente or 1

    def proximo() -> float:
        nonlocal s
        s = _i32(_i32(s) ^ _i32(_i32(s) << 13))
        s = _i32(s ^ ((s & 0xFFFFFFFF) >> 17))
        s = _i32(s ^ _i32(s << 5))
        return ((s & 0xFFFFFFFF) % 10000) / 10000
    return proximo


def codigo_assinatura(slug: str) -> str:
    """O código impresso ao lado da assinatura, ex.: #a7f3·0921."""
    h = hash32(slug)
    return f"#{h >> 16:04x}·{h % 10000:04d}"


def assinatura(slug: str) -> str:
    """Grade 7x7 espelhada, gerada a partir do endereço da matéria."""
    tam, cel = 7, 10
    r = sorteio(hash32(slug))
    partes = []
    for y in range(tam):
        for x in range(-(-tam // 2)):
            v = r()
            op = 1 if v > .72 else .5 if v > .5 else .2 if v > .36 else 0
            for xx in sorted({x, tam - 1 - x}):
                if op:
                    partes.append(f'<rect x="{xx * cel + 1}" y="{y * cel + 1}" width="{cel - 2}" height="{cel - 2}" fill="{VERDE}" opacity="{op}"/>')
                else:
                    partes.append(f'<rect x="{xx * cel + 4.5}" y="{y * cel + 4.5}" width="1" height="1" fill="{CINZA}"/>')
    return f'<svg viewBox="0 0 {tam * cel} {tam * cel}" width="100%" height="100%" aria-hidden="true">{"".join(partes)}</svg>'


def tokens_titulo(titulo_puro: str, maximo: int = 10) -> list[str]:
    """Palavras do título até o primeiro ponto, no máximo dez (o desenho perde a leitura com mais)."""
    frase = re.split(r"[.!?:]\s", titulo_puro + " ", maxsplit=1)[0]
    return [w for w in re.findall(r"[\w×-]+", frase)][:maximo]


def fmt(n: float) -> str:
    return f"{n:.2f}".rstrip("0").rstrip(".") if n != int(n) else str(int(n))


def mapa_atencao(tokens: list[str]) -> str:
    """As palavras do título ligadas por arcos de peso sorteado a partir do próprio título.

    É um desenho, não a atenção de um modelo: por isso sai sem números e com o selo "desenho do título"
    (decisão dele de 23/10/2026, no lugar do "● ao vivo" e dos pesos da maquete).
    """
    if len(tokens) < 2:
        return ""
    w, h, base, pad = 640, 400, 316, 70
    r = sorteio(hash32("|".join(tokens)))
    partes = [f'<line x1="0" x2="{w}" y1="{i * 44}" y2="{i * 44}" stroke="rgba(232,240,245,.05)"/>' for i in range(1, 8)]
    passo = (w - pad * 2) / (len(tokens) - 1)
    xs = [pad + i * passo for i in range(len(tokens))]
    pares = [{"i": i, "j": j, "w": r() ** 2.2} for i in range(len(tokens)) for j in range(i + 1, len(tokens))]
    pares.sort(key=lambda p: -p["w"])
    for k, p in enumerate(pares[:22]):
        x1, x2 = xs[p["i"]], xs[p["j"]]
        meio, alt = (x1 + x2) / 2, min(250, (x2 - x1) * .5 + 12)
        forte = k < 3
        partes.append(f'<path d="M{fmt(x1)} {base} Q{fmt(meio)} {fmt(base - alt * 2)} {fmt(x2)} {base}" fill="none" '
                      f'stroke="{VERDE if forte else CIANO}" stroke-width="{1.6 if forte else .9}" '
                      f'opacity="{.95 if forte else round(.18 + p["w"] * .5, 2):.2f}" style="animation-delay:{k * .06:.2f}s"/>')
    for i, tk in enumerate(tokens):
        x = fmt(xs[i])
        partes.append(f'<rect x="{fmt(xs[i] - 3)}" y="{base - 3}" width="6" height="6" fill="#e9eef2"/>')
        partes.append(f'<text x="{x}" y="{base + 24}" text-anchor="end" fill="#b4bec8" font-family="Martian Mono" '
                      f'font-size="11.5" transform="rotate(-38 {x} {base + 24})">{html.escape(tk)}</text>')
    return f'<svg class="mapa" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">{"".join(partes)}</svg>'
