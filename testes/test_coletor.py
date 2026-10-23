"""Coletor de pautas: lê RSS e Atom, respeita a janela, a lista de fontes oficiais e o que já foi publicado."""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "gerador"))
sys.path.insert(0, str(RAIZ / "redacao"))

from comum import carregar_json  # noqa: E402
from coletar import coletar, em_texto, ja_citados, ler_data, ler_feed  # noqa: E402

AGORA = datetime(2026, 10, 23, 9, 0, tzinfo=timezone.utc)  # 06:00 em Brasília, hora da tarefa
OFICIAIS = carregar_json("fontes_oficiais.json")

RSS = b"""<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Exemplo</title>
<item><title>Novo modelo</title><link>https://openai.com/exemplo/novo-modelo</link><pubDate>Thu, 22 Oct 2026 16:00:00 GMT</pubDate></item>
<item><title>Antigo</title><link>https://openai.com/exemplo/antigo</link><pubDate>Mon, 19 Oct 2026 16:00:00 GMT</pubDate></item>
<item><title>Link de terceiro</title><link>https://www.jornal-qualquer.com.br/x</link><pubDate>Thu, 22 Oct 2026 17:00:00 GMT</pubDate></item>
<item><title>Ja publicado</title><link>https://openai.com/exemplo/agentes-no-navegador/</link><pubDate>Thu, 22 Oct 2026 18:00:00 GMT</pubDate></item>
<item><title>Sem data</title><link>https://openai.com/exemplo/sem-data</link></item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Exemplo</title>
<entry><title>Pesquisa nova</title><link rel="alternate" href="https://deepmind.google/exemplo/pesquisa"/><published>2026-10-22T20:00:00Z</published></entry>
</feed>"""

CAMARA = json.dumps({"dados": [
    {"dataHora": "2026-10-21T15:06", "descricaoTramitacao": "Designação de relator", "despacho": "Designado relator."},
    {"dataHora": "2026-09-02T15:06", "descricaoTramitacao": "Notificação de Apensação", "despacho": "Antiga."},
]}).encode("utf-8")

FONTES = {
    "rss": [{"quem": "OpenAI", "url": "https://openai.com/rss"}, {"quem": "Google DeepMind", "url": "https://deepmind.google/atom"},
            {"quem": "Quebrada", "url": "https://mistral.ai/rss"}],
    "pagina": [{"quem": "Anthropic", "url": "https://www.anthropic.com/news"}],
    "camara": {"id": 2487262, "nome": "PL 2338/2023", "pagina": "https://www.camara.leg.br/propostas-legislativas/2487262", "dias": 7},
}


def busca_falsa(url: str, aceita: str = "") -> bytes:
    if url == "https://openai.com/rss":
        return RSS
    if url == "https://deepmind.google/atom":
        return ATOM
    if "dadosabertos.camara.leg.br" in url:
        assert aceita == "application/json"
        return CAMARA
    raise OSError("bloqueado pela rede do ambiente")


class Coletor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        pasta = Path(cls.tmp.name)
        exemplo = RAIZ / "testes" / "exemplos" / "2026-10-23-agentes-usam-computador.md"
        (pasta / exemplo.name).write_text(exemplo.read_text(encoding="utf-8"), encoding="utf-8")
        cls.citados = ja_citados(pasta)
        cls.r = coletar(FONTES, OFICIAIS, cls.citados, AGORA, 48, busca=busca_falsa)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def titulos(self):
        return [p["titulo"] for p in self.r["pautas"]]

    def test_le_rss_e_atom(self):
        self.assertEqual([i["titulo"] for i in ler_feed(RSS)][:2], ["Novo modelo", "Antigo"])
        atom = ler_feed(ATOM)
        self.assertEqual((atom[0]["link"], atom[0]["data"]), ("https://deepmind.google/exemplo/pesquisa", datetime(2026, 10, 22, 20, 0, tzinfo=timezone.utc)))

    def test_janela_de_horas(self):
        self.assertIn("Novo modelo", self.titulos())
        self.assertNotIn("Antigo", self.titulos())
        self.assertNotIn("Sem data", self.titulos())

    def test_link_fora_da_lista_vai_para_o_aviso(self):
        self.assertNotIn("Link de terceiro", self.titulos())
        self.assertEqual([p["link"] for p in self.r["fora_da_lista"]], ["https://www.jornal-qualquer.com.br/x"])

    def test_o_que_ja_foi_citado_fica_de_fora(self):
        self.assertIn("https://openai.com/exemplo/agentes-no-navegador", self.citados)
        self.assertNotIn("Ja publicado", self.titulos())

    def test_fonte_que_falha_nao_derruba_as_outras(self):
        self.assertEqual([f["quem"] for f in self.r["falhas"]], ["Quebrada"])
        self.assertIn("Pesquisa nova", self.titulos())

    def test_camara_so_movimentacao_recente(self):
        camara = [p for p in self.r["pautas"] if p["quem"] == "Câmara dos Deputados"]
        self.assertEqual(len(camara), 1)
        self.assertIn("Designação de relator", camara[0]["titulo"])

    def test_ordem_da_mais_nova_para_a_mais_antiga(self):
        datas = [p["data"] for p in self.r["pautas"]]
        self.assertEqual(datas, sorted(datas, reverse=True))

    def test_texto_lista_paginas_e_falhas(self):
        texto = em_texto(self.r)
        self.assertIn("Anthropic: https://www.anthropic.com/news", texto)
        self.assertIn("Quebrada", texto)
        self.assertIn("06:00 de Brasília", texto)

    def test_datas_dos_formatos_usados(self):
        self.assertEqual(ler_data("Thu, 22 Oct 2026 16:00:00 GMT"), datetime(2026, 10, 22, 16, 0, tzinfo=timezone.utc))
        self.assertEqual(ler_data("2026-10-22T13:00").utcoffset().total_seconds(), -3 * 3600)  # API da Câmara: hora de Brasília
        self.assertIsNone(ler_data("ontem"))

    def test_todas_as_fontes_do_coletor_sao_oficiais(self):
        from travas import dominio_oficial
        fontes = json.loads((RAIZ / "redacao" / "fontes.json").read_text(encoding="utf-8"))
        for f in fontes["rss"] + fontes["pagina"] + [{"url": fontes["camara"]["pagina"]}]:
            with self.subTest(f["url"]):
                self.assertIsNotNone(dominio_oficial(f["url"], OFICIAIS))


if __name__ == "__main__":
    unittest.main()
