// today.ia.br — maquete v1: assinaturas geradas e mapa de atenção

function hash(str) {
  let h = 2166136261;
  for (const c of str) { h ^= c.codePointAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function rng(seed) {
  let s = seed || 1;
  return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 10000) / 10000; };
}

const NS = "http://www.w3.org/2000/svg";
const el = (tag, attrs) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); return n; };

// Assinatura de cada matéria: grade 7x7 espelhada, gerada a partir do título
function glyph(node) {
  const size = 7, cell = 10;
  const r = rng(hash(node.dataset.glyph));
  const svg = el("svg", { viewBox: `0 0 ${size * cell} ${size * cell}`, width: "100%", height: "100%" });
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < Math.ceil(size / 2); x++) {
      const v = r();
      const op = v > .72 ? 1 : v > .5 ? .5 : v > .36 ? .2 : 0;
      for (const xx of new Set([x, size - 1 - x])) {
        if (op) svg.append(el("rect", { x: xx * cell + 1, y: y * cell + 1, width: cell - 2, height: cell - 2, fill: "#c6ff3a", opacity: op }));
        else svg.append(el("rect", { x: xx * cell + 4.5, y: y * cell + 4.5, width: 1, height: 1, fill: "#6f7b87" }));
      }
    }
  }
  node.append(svg);
}

// Mapa de atenção: as palavras do título como tokens, ligadas por arcos com peso
function attention(node) {
  const tokens = node.dataset.tokens.split("|");
  const W = 640, H = 400, base = 316, pad = 70;
  const r = rng(hash(node.dataset.tokens));
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: "xMidYMid meet" });

  for (let i = 1; i < 8; i++) svg.append(el("line", { x1: 0, x2: W, y1: i * 44, y2: i * 44, stroke: "rgba(232,240,245,.05)" }));

  const step = (W - pad * 2) / (tokens.length - 1);
  const xs = tokens.map((_, i) => pad + i * step);

  const pairs = [];
  for (let i = 0; i < tokens.length; i++)
    for (let j = i + 1; j < tokens.length; j++) pairs.push({ i, j, w: Math.pow(r(), 2.2) });
  pairs.sort((a, b) => b.w - a.w);
  const top = pairs.slice(0, 22);

  top.forEach((p, k) => {
    const x1 = xs[p.i], x2 = xs[p.j], mid = (x1 + x2) / 2, h = Math.min(250, (x2 - x1) * .5 + 12);
    const path = el("path", {
      d: `M${x1} ${base} Q${mid} ${base - h * 2} ${x2} ${base}`,
      fill: "none", stroke: k < 3 ? "#c6ff3a" : "#6be4ff",
      "stroke-width": k < 3 ? 1.6 : .9, opacity: (k < 3 ? .95 : .18 + p.w * .5).toFixed(2)
    });
    const len = 900;
    path.style.strokeDasharray = len; path.style.strokeDashoffset = len;
    path.style.animation = `draw 1.6s ${(k * .06).toFixed(2)}s cubic-bezier(.2,.7,.2,1) forwards`;
    svg.append(path);
    if (k < 3) {
      const t = el("text", { x: mid, y: base - h - 8, "text-anchor": "middle", fill: "#c6ff3a", "font-family": "Martian Mono", "font-size": 11 });
      t.textContent = (0.5 + p.w * .49).toFixed(2);
      svg.append(t);
    }
  });

  tokens.forEach((tk, i) => {
    svg.append(el("rect", { x: xs[i] - 3, y: base - 3, width: 6, height: 6, fill: "#e9eef2" }));
    const t = el("text", { x: xs[i], y: base + 24, "text-anchor": "end", fill: "#b4bec8", "font-family": "Martian Mono", "font-size": 11.5, transform: `rotate(-38 ${xs[i]} ${base + 24})` });
    t.textContent = tk;
    svg.append(t);
  });

  const style = document.createElement("style");
  style.textContent = "@keyframes draw { to { stroke-dashoffset: 0; } }";
  document.head.append(style);
  node.append(svg);
}

document.querySelectorAll("[data-glyph]").forEach(glyph);
document.querySelectorAll("[data-tokens]").forEach(attention);
